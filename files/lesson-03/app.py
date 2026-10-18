"""Local dashboard: native browser video + Roboflow Workflow predictions."""
import os
from pathlib import Path
from urllib.parse import urlsplit

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, ConfigDict, Field, SecretStr, ValidationError
from starlette.concurrency import run_in_threadpool
from starlette.middleware.trustedhost import TrustedHostMiddleware

from workflow import WorkflowError, request_predictions

ROOT = Path(__file__).resolve().parent
MAX_BODY = 12 * 1024 * 1024
app = FastAPI(title="Drive Vision", docs_url=None, redoc_url=None)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["127.0.0.1", "localhost", "testserver"])
app.mount("/assets", StaticFiles(directory=ROOT / "web"), name="assets")


class Frame(BaseModel):
    model_config = ConfigDict(extra="forbid", allow_inf_nan=False)
    index: int = Field(ge=0)
    timestamp: float = Field(ge=0)
    jpeg: str = Field(min_length=8, max_length=1_400_000)


class Batch(BaseModel):
    model_config = ConfigDict(extra="forbid")
    workspace: str = Field(pattern=r"^[A-Za-z0-9_-]{1,160}$")
    workflow: str = Field(pattern=r"^[A-Za-z0-9_-]{1,160}$")
    api_key: SecretStr = Field(default=SecretStr(""))
    input_name: str = Field(default="image", pattern=r"^[A-Za-z0-9_-]{1,160}$")
    output_name: str = Field(default="predictions", pattern=r"^[A-Za-z0-9_-]{1,160}$")
    frames: list[Frame] = Field(min_length=1, max_length=16)


@app.get("/")
def home():
    return FileResponse(ROOT / "web/index.html", headers={"Cache-Control": "no-store"})


@app.get("/api/config")
def config():
    return {
        "workspace": os.getenv("ROBOFLOW_WORKSPACE", ""),
        "workflow": os.getenv("ROBOFLOW_WORKFLOW", ""),
        "has_key": bool(os.getenv("ROBOFLOW_API_KEY", "")),
        "input_name": os.getenv("ROBOFLOW_INPUT", "image"),
        "output_name": os.getenv("ROBOFLOW_OUTPUT", "predictions"),
    }


@app.post("/api/infer")
async def infer(request: Request):
    origin = request.headers.get("origin")
    if origin and urlsplit(origin).netloc != request.headers.get("host"):
        raise HTTPException(403, "이 앱의 화면에서 분석을 시작하세요.")
    chunks, size = [], 0
    async for chunk in request.stream():
        size += len(chunk)
        if size > MAX_BODY:
            raise HTTPException(413, "한 번에 보내는 이미지 묶음이 너무 큽니다.")
        chunks.append(chunk)
    try:
        batch = Batch.model_validate_json(b"".join(chunks))
    except ValidationError:
        raise HTTPException(422, "입력 설정·이미지 묶음 형식을 확인하세요.") from None
    frames = [frame.model_dump() for frame in batch.frames]
    if len({f["index"] for f in frames}) != len(frames):
        raise HTTPException(422, "분석 이미지 번호가 중복되었습니다.")
    try:
        results = await run_in_threadpool(
            request_predictions, frames, batch.workspace, batch.workflow,
            batch.api_key.get_secret_value().strip() or os.getenv("ROBOFLOW_API_KEY", ""),
            batch.input_name, batch.output_name,
        )
    except WorkflowError as error:
        return JSONResponse({"detail": str(error)}, status_code=502,
                            headers={"Cache-Control": "no-store"})
    return JSONResponse({"results": results}, headers={"Cache-Control": "no-store"})


if __name__ == "__main__":
    import uvicorn
    print("Drive Vision → http://127.0.0.1:7862")
    uvicorn.run(app, host="127.0.0.1", port=7862, access_log=False)
