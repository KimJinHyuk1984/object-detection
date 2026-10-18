"""Run from this folder: python -m streamlit run app.py"""
import json
import os
import streamlit as st

from core import (
    CLASSES, MIN_CONFIDENCE, InferenceFailure, context_id, infer_image,
    normalize_response, png_bytes, prepare_image, render_predictions,
    valid_model_id, visible_predictions,
)
from demo import make_demo

st.set_page_config(page_title="도로 영상 분석", page_icon="🚦", layout="wide")
st.title("도로 영상 분석")
st.caption("한 모델의 결과를 객체 박스와 주행 가능 도로 영역으로 표시합니다.")


def setting(name):
    value = os.environ.get(name)
    if value:
        return value.strip()
    try:
        return str(st.secrets.get(name, "")).strip()
    except (FileNotFoundError, st.errors.StreamlitSecretNotFoundError):
        return ""


with st.sidebar:
    st.header("분석 설정")
    mode = st.radio("실행 모드", ["영상 업로드 확인", "예제 결과로 연습", "내 모델로 분석"], key="mode")
    threshold = st.slider("표시 confidence 임계값", MIN_CONFIDENCE, 1.0, 0.40, 0.05, key="threshold")
    opacity = st.slider("도로 영역 불투명도", 0.0, 0.8, 0.3, 0.05, key="opacity")
    selected = st.multiselect("표시할 클래스", list(CLASSES), default=list(CLASSES), key="classes")
    st.caption("슬라이더와 클래스 선택은 이미 받은 결과의 표시만 바꿉니다.")
    with st.expander("클래스 의미"):
        for label, meaning in CLASSES.items():
            st.write(f"**{label}** · {meaning}")

demo_mode = mode == "예제 결과로 연습"
model_id = ""
api_key = ""
image = None
sample = None

if mode == "영상 업로드 확인":
    st.session_state.pop("prediction_result",None)
    st.session_state.pop("analysis_context",None)
    from video_ui import run_video_ui
    run_video_ui(mode,"","",threshold,selected,opacity)
    st.stop()

if demo_mode:
    from video_ui import clear_video_result
    clear_video_result()
    st.info("수업용 가상 도로와 미리 작성한 결과입니다. 실제 모델의 예측·성능이 아닙니다.")
    image, sample = make_demo()
else:
    model_id = st.text_input("모델 ID", value=setting("ROBOFLOW_MODEL_ID"),
                             placeholder="프로젝트이름/1", key="model_id").strip()
    api_key = setting("ROBOFLOW_API_KEY")
    if not api_key:
        st.warning("API 키가 설정되지 않았습니다. 실습 README의 secrets.toml 설정을 확인하세요.")
    input_type = st.radio("입력 방식",["영상 업로드","이미지 한 장"],key="input_type")
    from video_ui import clear_video_result, run_video_ui
    if input_type == "영상 업로드":
        st.session_state.pop("prediction_result",None)
        st.session_state.pop("analysis_context",None)
        run_video_ui(mode,model_id,api_key,threshold,selected,opacity)
        st.stop()
    clear_video_result()
    st.info("분석 실행을 누르면 선택한 이미지 한 장이 Roboflow로 전송됩니다.")
    uploaded = st.file_uploader("도로 이미지 한 장", type=["jpg", "jpeg", "png", "webp"], key="upload")
    if uploaded is not None:
        try:
            image = prepare_image(uploaded.getvalue())
        except ValueError as error:
            st.error(str(error))
    st.caption("최대 10MB·1,600만 화소. 방향을 보정하고 긴 변을 최대 1,600px로 줄여 분석합니다.")

identity = context_id(image, mode, model_id, api_key) if image is not None else None
if st.session_state.get("analysis_context") != identity:
    st.session_state.analysis_context = identity
    st.session_state.pop("prediction_result", None)
    st.session_state.pop("prediction_messages", None)

ready = image is not None and (demo_mode or (bool(api_key) and valid_model_id(model_id)))
if not demo_mode and model_id and not valid_model_id(model_id):
    st.warning("모델 ID는 프로젝트이름/버전번호 형식입니다.")
if st.button("예제 결과 보기" if demo_mode else "분석 실행", type="primary", disabled=not ready, key="analyze"):
    st.session_state.pop("prediction_result", None)
    st.session_state.pop("prediction_messages", None)
    try:
        with st.spinner("결과를 준비하고 있습니다."):
            raw = sample if demo_mode else infer_image(image, model_id, api_key)
            result, messages = normalize_response(raw, image.size)
            st.session_state.prediction_result = result
            st.session_state.prediction_messages = messages
    except (InferenceFailure, ValueError) as error:
        st.error(str(error))

result = st.session_state.get("prediction_result")
if image is not None:
    left, right = st.columns(2)
    with left:
        st.subheader("입력 이미지")
        st.image(image, width=image.width)
        st.caption(f"분석 좌표 기준: {image.width} × {image.height}px")
    with right:
        st.subheader("표시 결과")
        if result is None:
            st.info("위 버튼을 눌러 결과를 확인하세요.")
        else:
            for message in st.session_state.get("prediction_messages", []):
                st.warning(message)
            visible = visible_predictions(result, threshold, selected)
            rendered = render_predictions(image, visible, opacity, demo=demo_mode)
            st.image(rendered, width=rendered.width)
            objects = sum(p["class"] != "line" for p in visible)
            regions = sum(p["class"] == "line" for p in visible)
            st.caption(f"표시된 객체 {objects}개 · 도로 영역 {regions}개")
            if not visible:
                st.info("현재 조건에 맞는 결과가 없습니다. 임계값과 클래스 선택을 확인하세요.")
            elif not regions:
                st.info("표시할 line 영역이 없습니다. 임계값·클래스 선택과 분할 모델의 예측을 확인하세요.")
            rows = [{"클래스":p["class"],"의미":CLASSES[p["class"]],
                     "confidence":round(p["confidence"],3),
                     "표시":"도로 마스크" if p["class"]=="line" else "객체 박스"}
                    for p in visible]
            if rows:
                st.dataframe(rows, hide_index=True)
            prefix = "demo" if demo_mode else "prediction"
            st.download_button("결과 이미지 PNG 받기", png_bytes(rendered),
                               f"{prefix}-result.png", "image/png")
            export = {"source":"hand-written demo" if demo_mode else "Roboflow model",
                      "model_id":model_id if not demo_mode else None,
                      "display_threshold":threshold,"selected_classes":selected,
                      **result}
            st.download_button("분석 기록 JSON 받기",
                               json.dumps(export,ensure_ascii=False,indent=2).encode("utf-8"),
                               f"{prefix}-result.json","application/json")
            with st.expander("좌표가 정리된 전체 응답 보기"):
                st.json(result)
            st.caption("JSON에는 표시 필터 적용 전 결과도 포함됩니다. API 키는 저장하지 않습니다.")

st.divider()
st.caption("line은 도색된 차선이 아닌 차선 사이의 주행 가능한 도로 영역입니다. 모델 하나의 결과를 두 방식으로 표시합니다.")
