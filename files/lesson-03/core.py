"""Image preparation, Roboflow inference and drawing for lesson 3."""
from __future__ import annotations

import hashlib
import io
import math
import re
import warnings
from PIL import Image, ImageDraw, ImageFont, ImageOps

CLASSES = {
    "car": "자동차", "motor": "오토바이", "people": "사람", "sign": "표지판",
    "lampg": "초록 신호등", "lampr": "빨간 신호등", "lampy": "노란 신호등",
    "lamp": "색 구분이 어려운 신호등", "line": "주행 가능 도로 영역",
}
COLORS = {
    "car": "#2673D9", "motor": "#A855B5", "people": "#E76F33", "sign": "#B97812",
    "lampg": "#168654", "lampr": "#CC334C", "lampy": "#A78500",
    "lamp": "#526274", "line": "#00AFA2",
}
MIN_CONFIDENCE = 0.05
MAX_FILE_BYTES = 10 * 1024 * 1024
MAX_IMAGE_PIXELS = 16_000_000
MAX_SIDE = 1600


class InferenceFailure(RuntimeError):
    """A message that is safe to display; never contains a request URL or key."""


def prepare_image(data: bytes) -> Image.Image:
    if not data or len(data) > MAX_FILE_BYTES:
        raise ValueError("10MB 이하의 JPG·PNG·WebP 이미지 한 장을 선택하세요.")
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("error", Image.DecompressionBombWarning)
            with Image.open(io.BytesIO(data)) as source:
                if source.format not in {"JPEG", "PNG", "WEBP"}:
                    raise ValueError("JPG·PNG·WebP 형식만 사용할 수 있습니다.")
                if source.width * source.height > MAX_IMAGE_PIXELS:
                    raise ValueError("이미지를 1,600만 화소 이하로 줄여 주세요.")
                source.load()
                oriented = ImageOps.exif_transpose(source).convert("RGBA")
                background = Image.new("RGBA", oriented.size, "white")
                image = Image.alpha_composite(background, oriented).convert("RGB")
    except (OSError, Image.DecompressionBombError, Image.DecompressionBombWarning):
        raise ValueError("읽을 수 없는 이미지입니다. 다른 JPG·PNG·WebP 파일을 선택하세요.") from None
    image.thumbnail((MAX_SIDE, MAX_SIDE), Image.Resampling.LANCZOS)
    return image


def png_bytes(image: Image.Image) -> bytes:
    output = io.BytesIO()
    image.save(output, format="PNG")
    return output.getvalue()


def context_id(image: Image.Image, mode: str, model_id: str, api_key: str = "") -> str:
    """Per-session identity. Display sliders deliberately do not affect identity."""
    digest = hashlib.sha256()
    digest.update(f"{mode}|{model_id}|{image.size}|".encode())
    digest.update(image.tobytes())
    digest.update(hashlib.sha256(api_key.encode()).digest())
    return digest.hexdigest()


def valid_model_id(model_id: str) -> bool:
    return bool(re.fullmatch(r"[A-Za-z0-9_-]+/[1-9][0-9]*", model_id))


def infer_image(image: Image.Image, model_id: str, api_key: str) -> dict:
    if not valid_model_id(model_id):
        raise InferenceFailure("모델 ID를 프로젝트이름/버전번호 형식으로 확인하세요.")
    if not api_key.strip():
        raise InferenceFailure("Roboflow API 키를 secrets.toml 또는 환경 변수에 설정하세요.")
    try:
        from inference_sdk import InferenceHTTPClient, InferenceConfiguration
    except ImportError:
        raise InferenceFailure("실습 폴더에서 requirements.txt의 패키지를 설치하세요.") from None
    try:
        client = InferenceHTTPClient(
            api_url="https://serverless.roboflow.com",
            api_key=api_key,
        )
        client.configure(InferenceConfiguration(
            confidence_threshold=MIN_CONFIDENCE, response_mask_format="polygon",
            api_key_transport="header", disable_active_learning=True,
        ))
        return client.infer(image, model_id=model_id)
    except Exception:
        # SDK errors may contain authenticated URLs. Do not expose raw exceptions.
        raise InferenceFailure(
            "분석 요청을 완료하지 못했습니다. 모델 ID·키 권한·Serverless 지원 여부와 "
            "네트워크를 확인한 뒤 다시 시도하세요."
        ) from None


def _number(value) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError("숫자가 아닌 좌표입니다.")
    result = float(value)
    if not math.isfinite(result):
        raise ValueError("유한한 숫자가 아닌 좌표입니다.")
    return result


def _area(points: list[tuple[float, float]]) -> float:
    return abs(sum(
        x1*y2-x2*y1
        for (x1,y1),(x2,y2) in zip(points, points[1:]+points[:1])
    )) / 2


def normalize_response(payload, image_size: tuple[int, int]) -> tuple[dict, list[str]]:
    """Map response coordinates onto the processed input image; skip bad entries."""
    if isinstance(payload, list) and len(payload) == 1:
        payload = payload[0]
    if not isinstance(payload, dict) or not isinstance(payload.get("predictions"), list):
        raise ValueError("예상한 predictions 목록이 없습니다. 단일 분할 모델 응답인지 확인하세요.")
    meta = payload.get("image")
    if not isinstance(meta, dict):
        raise ValueError("응답의 이미지 크기가 없습니다. 응답 형식을 확인하세요.")
    try:
        rw, rh = _number(meta.get("width")), _number(meta.get("height"))
        if rw <= 0 or rh <= 0:
            raise ValueError()
    except ValueError:
        raise ValueError("응답 이미지의 가로·세로 크기를 확인하세요.") from None
    width, height = image_size
    sx, sy = width/rw, height/rh
    predictions, messages = [], []
    for item in payload["predictions"]:
        try:
            if not isinstance(item, dict) or item.get("class") not in CLASSES:
                raise ValueError()
            label = item["class"]
            confidence = _number(item.get("confidence"))
            if not 0 <= confidence <= 1:
                raise ValueError()
            x, y = _number(item.get("x"))*sx, _number(item.get("y"))*sy
            bw, bh = _number(item.get("width"))*sx, _number(item.get("height"))*sy
            if bw <= 0 or bh <= 0:
                raise ValueError()
            box = (
                max(0, min(width-1, x-bw/2)), max(0, min(height-1, y-bh/2)),
                max(0, min(width-1, x+bw/2)), max(0, min(height-1, y+bh/2)),
            )
            if box[2] <= box[0] or box[3] <= box[1]:
                raise ValueError()
            points = []
            if label == "line":
                raw_points = item.get("points")
                if not isinstance(raw_points, list) or len(raw_points) < 3:
                    messages.append("line에 유효한 폴리곤이 없어 표시하지 않았습니다. 분할 모델과 응답을 확인하세요.")
                    continue
                for p in raw_points:
                    px, py = _number(p["x"])*sx, _number(p["y"])*sy
                    points.append((max(0,min(width-1,px)), max(0,min(height-1,py))))
                if len(set(points)) < 3 or _area(points) < 1:
                    messages.append("면적이 없는 line 폴리곤을 제외했습니다.")
                    continue
            predictions.append({"class": label, "confidence": confidence,
                                "box": list(box), "points": [list(p) for p in points]})
        except (ValueError, TypeError, KeyError):
            messages.append("지원하지 않는 클래스 또는 잘못된 좌표·점수를 가진 결과를 제외했습니다.")
    return {"image": {"width": width, "height": height}, "predictions": predictions}, list(dict.fromkeys(messages))


def visible_predictions(result: dict, threshold: float, selected: list[str]) -> list[dict]:
    return [p for p in result["predictions"]
            if p["confidence"] >= threshold and p["class"] in selected]


def render_predictions(image: Image.Image, predictions: list[dict], opacity: float = 0.3,
                       demo: bool = False) -> Image.Image:
    base = image.convert("RGBA")
    mask = Image.new("L", image.size)
    brush = ImageDraw.Draw(mask)
    for prediction in predictions:
        if prediction["class"] == "line":
            brush.polygon([tuple(p) for p in prediction["points"]], fill=255)
    overlay = Image.new("RGBA", image.size, COLORS["line"])
    overlay.putalpha(mask.point(lambda value: round(value * max(0, min(0.8, opacity)))))
    result = Image.alpha_composite(base, overlay).convert("RGB")
    draw = ImageDraw.Draw(result)
    font_size = max(12, min(22, round(image.width/55)))
    font = ImageFont.load_default(size=font_size)
    stroke = max(2, round(image.width/400))
    for prediction in predictions:
        label = prediction["class"]
        color = COLORS[label]
        if label == "line":
            points = [tuple(p) for p in prediction["points"]]
            draw.line(points + points[:1], fill=color, width=stroke)
            x, y = points[0]
        else:
            draw.rectangle(prediction["box"], outline=color, width=stroke)
            x, y = prediction["box"][:2]
        caption = f'{label} {prediction["confidence"]:.2f}'
        bounds = draw.textbbox((0, 0), caption, font=font)
        tw, th = bounds[2]-bounds[0]+10, bounds[3]-bounds[1]+8
        x = max(0, min(image.width-tw, x))
        y = max(0, min(image.height-th, y-th))
        draw.rectangle((x,y,x+tw,y+th), fill=color)
        draw.text((x+5,y+4-bounds[1]), caption, font=font, fill="white")
    if demo:
        draw.rectangle((0,0,image.width,32), fill="#182B36")
        draw.text((12,7), "DEMO / HAND-WRITTEN SAMPLE RESULT", font=ImageFont.load_default(size=17), fill="white")
    return result
