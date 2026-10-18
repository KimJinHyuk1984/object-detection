"""Roboflow Workflow batch adapter, based on gamza-lab's video template."""
import base64
import io
import re
from PIL import Image, UnidentifiedImageError
import requests
from core import normalize_response

API_URL = "https://serverless.roboflow.com"
ID_PATTERN = re.compile(r"[A-Za-z0-9_-]{1,160}")


class WorkflowError(Exception):
    pass


def image_size(encoded):
    try:
        raw = base64.b64decode(encoded, validate=True)
        if not raw or len(raw) > 1_000_000:
            raise ValueError()
        with Image.open(io.BytesIO(raw)) as image:
            if image.format != "JPEG" or not (1 <= image.width <= 1280 and 1 <= image.height <= 1280):
                raise ValueError()
            size = image.size
            image.verify()
        return size
    except (ValueError, OSError, UnidentifiedImageError):
        raise WorkflowError("분석 이미지가 올바른 JPEG 형식이 아닙니다.") from None


def request_predictions(frames, workspace, workflow, api_key,
                        input_name="image", output_name="predictions"):
    for value in (workspace, workflow, input_name, output_name):
        if not ID_PATTERN.fullmatch(value):
            raise WorkflowError("Workspace·Workflow ID와 입출력 이름을 확인하세요.")
    if not api_key.strip():
        raise WorkflowError("Roboflow Private API 키를 입력하세요.")
    sizes = [image_size(frame["jpeg"]) for frame in frames]
    try:
        response = requests.post(
            f"{API_URL}/{workspace}/workflows/{workflow}",
            headers={"Authorization": f"Bearer {api_key.strip()}"},
            json={"inputs": {input_name: [
                {"type": "base64", "value": frame["jpeg"]} for frame in frames
            ]}},
            timeout=(10, 90),
        )
        if not response.ok:
            explanations = {
                401: "API 키와 Workspace 권한을 확인하세요.",
                403: "Workflow 접근 권한과 API 사용 권한을 확인하세요.",
                404: "Deploy Workflow의 Workspace·Workflow ID를 확인하세요.",
                413: "설정에서 요청 묶음 크기를 줄여 주세요.",
                429: "API 사용량 제한입니다. 잠시 후 분석을 다시 시작하세요.",
            }
            raise WorkflowError(f"Roboflow HTTP {response.status_code}. "
                                + explanations.get(response.status_code, "Workflow 설정과 Serverless 지원을 확인하세요."))
        payload = response.json()
    except requests.Timeout:
        raise WorkflowError("응답 시간이 초과되었습니다. 묶음 크기를 줄인 뒤 다시 시도하세요.") from None
    except (requests.RequestException, ValueError):
        raise WorkflowError("Roboflow 연결 또는 응답을 확인하세요.") from None
    outputs = payload.get("outputs") if isinstance(payload, dict) else None
    if not isinstance(outputs, list) or len(outputs) != len(frames):
        raise WorkflowError("분석 이미지 수와 Workflow outputs 수가 다릅니다. 묶음 크기 1로 확인하세요.")
    results = []
    for frame, size, output in zip(frames, sizes, outputs):
        detection = output.get(output_name) if isinstance(output, dict) else None
        if not isinstance(detection, dict) or not isinstance(detection.get("predictions"), list):
            raise WorkflowError("Workflow 출력 이름과 Predictions 출력을 확인하세요. 시각화 이미지는 사용할 수 없습니다.")
        detection = {**detection, "image": detection.get("image") or {"width": size[0], "height": size[1]}}
        try:
            result, messages = normalize_response(detection, size)
        except ValueError:
            raise WorkflowError("예측 좌표 또는 이미지 크기가 잘못되었습니다.") from None
        results.append({"index": frame["index"], "timestamp": frame["timestamp"],
                        **result, "messages": messages})
    return results
