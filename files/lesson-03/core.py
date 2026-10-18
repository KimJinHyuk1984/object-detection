"""Class labels and validated polygon/box coordinates for the dashboard."""
import math

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
