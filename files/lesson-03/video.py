"""Sample an uploaded video locally and encode a silent H.264 result clip."""
import hashlib
import io
import json
import math
from PIL import Image, ImageDraw, ImageFont
import av
from core import InferenceFailure, normalize_response, render_predictions, visible_predictions

MAX_VIDEO_BYTES = 200 * 1024 * 1024
MAX_FRAMES = 60
MAX_SECONDS = 20
VIDEO_SIDE = 960


def video_info(data):
    if not data or len(data) > MAX_VIDEO_BYTES:
        raise ValueError("200MB 이하의 MP4·MOV·AVI 영상을 선택하세요.")
    try:
        with av.open(io.BytesIO(data)) as container:
            if not container.streams.video:
                raise ValueError("영상 트랙이 없습니다.")
            stream = container.streams.video[0]
            duration = (float(stream.duration * stream.time_base) if stream.duration is not None
                        else float(container.duration / av.time_base) if container.duration else 0)
            if not math.isfinite(duration) or duration <= 0:
                raise ValueError("영상 길이를 읽을 수 없습니다. MP4(H.264)로 변환해 주세요.")
            if not 0 < stream.width * stream.height <= 16_000_000:
                raise ValueError("영상 해상도를 1,600만 화소 이하로 줄여 주세요.")
            return {"duration": duration, "width": stream.width, "height": stream.height,
                    "fps": float(stream.average_rate or 0)}
    except av.FFmpegError:
        raise ValueError("영상을 열 수 없습니다. MP4(H.264) 파일로 다시 확인하세요.") from None


def sample_plan(info, start, seconds, rate):
    if not all(math.isfinite(v) for v in (start, seconds, rate)):
        raise ValueError("분석 구간을 숫자로 입력하세요.")
    if start < 0 or start >= info["duration"] or not 0 < seconds <= MAX_SECONDS or rate not in (1, 2, 5):
        raise ValueError("시작 시각·구간 길이(최대 20초)·초당 프레임 수를 확인하세요.")
    end = min(info["duration"], start + seconds)
    count = math.ceil((end-start)*rate-1e-9)
    if count > MAX_FRAMES:
        raise ValueError("한 번에 최대 60프레임입니다. 구간 길이나 초당 프레임 수를 줄여 주세요.")
    return end, count


def video_context(data, mode, model_id, api_key, start, seconds, rate):
    digest = hashlib.sha256(data)
    digest.update(json.dumps([mode,model_id,start,seconds,rate]).encode())
    digest.update(hashlib.sha256(api_key.encode()).digest())
    return digest.hexdigest()


def sample_frames(data, start, seconds, rate):
    info = video_info(data)
    end, count = sample_plan(info, start, seconds, rate)
    frames = []
    try:
        with av.open(io.BytesIO(data)) as container:
            stream = container.streams.video[0]
            origin = float((stream.start_time or 0)*stream.time_base)
            container.seek(int((origin+start)/stream.time_base), stream=stream, backward=True)
            target = start
            for frame in container.decode(stream):
                if frame.pts is None:
                    continue
                timestamp = float(frame.pts*frame.time_base)-origin
                if timestamp >= end-1e-7:
                    break
                if timestamp+1e-7 < target:
                    continue
                image = frame.to_image().convert("RGB")
                image.thumbnail((VIDEO_SIDE,VIDEO_SIDE), Image.Resampling.LANCZOS)
                output = io.BytesIO()
                image.save(output,"JPEG",quality=92)
                frames.append({"timestamp":timestamp,"jpeg":output.getvalue()})
                # Skip missing sampling slots without duplicating a source frame.
                target = start + (math.floor((timestamp-start)*rate+1e-7)+1)/rate
                if len(frames) >= count:
                    break
    except av.FFmpegError:
        raise ValueError("영상 구간을 읽지 못했습니다. 다른 구간이나 MP4(H.264) 파일을 확인하세요.") from None
    if not frames:
        raise ValueError("선택한 구간에서 프레임을 읽지 못했습니다.")
    return {"info":info,"start":start,"end":end,"rate":rate,"frames":frames}


def frame_image(item):
    with Image.open(io.BytesIO(item["jpeg"])) as image:
        return image.convert("RGB")


def analyze_frames(batch, infer, progress=None):
    analyzed = []
    total = len(batch["frames"])
    for index, item in enumerate(batch["frames"]):
        image = frame_image(item)
        try:
            raw = infer(image)
            result, messages = normalize_response(raw,image.size)
        except (InferenceFailure, ValueError):
            raise InferenceFailure(
                f"{index+1}/{total}번째 프레임 분석을 완료하지 못했습니다. "
                "모델·키 권한·응답 형식·네트워크를 확인하세요. 완료 전 결과는 저장하지 않았습니다."
            ) from None
        analyzed.append({**item,"result":result,"messages":messages})
        if progress:
            progress(index+1,total)
    return {**batch,"frames":analyzed}


def display_frame(item, threshold, selected, opacity):
    image = frame_image(item)
    result = item.get("result")
    if result is not None:
        image = render_predictions(image,visible_predictions(result,threshold,selected),opacity)
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default(size=15)
    label = ("MODEL RESULT" if result is not None else "UPLOAD CHECK / NO MODEL")
    label += f' / source {item["timestamp"]:.2f}s'
    draw.rectangle((0,0,image.width,28),fill="#182B36")
    draw.text((8,5),label,font=font,fill="white")
    return image


def encode_video(batch, threshold, selected, opacity):
    output = io.BytesIO()
    try:
        with av.open(output,mode="w",format="mp4") as container:
            stream = container.add_stream("libx264",rate=batch["rate"])
            first = frame_image(batch["frames"][0])
            # yuv420p requires even dimensions; pad without changing prediction coordinates.
            stream.width = first.width + first.width%2
            stream.height = first.height + first.height%2
            stream.pix_fmt = "yuv420p"
            stream.options = {"crf":"23","preset":"veryfast"}
            for item in batch["frames"]:
                image = display_frame(item,threshold,selected,opacity)
                canvas = Image.new("RGB",(stream.width,stream.height))
                canvas.paste(image,(0,0))
                for packet in stream.encode(av.VideoFrame.from_image(canvas)):
                    container.mux(packet)
            for packet in stream.encode():
                container.mux(packet)
    except av.FFmpegError:
        raise ValueError("결과 영상을 만들지 못했습니다. 패키지 설치와 H.264 인코더를 확인하세요.") from None
    return output.getvalue()


def export_record(batch, model_id, threshold, selected, opacity):
    return {"source":"Roboflow model" if model_id else "upload check - no inference",
            "model_id":model_id or None,"input_video":batch["info"],
            "start_seconds":batch["start"],"end_seconds":batch["end"],
            "sample_fps":batch["rate"],"display_threshold":threshold,
            "selected_classes":selected,"opacity":opacity,
            "frames":[{k:v for k,v in item.items() if k!="jpeg"} for item in batch["frames"]]}
