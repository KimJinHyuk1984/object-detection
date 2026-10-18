"""Streamlit video input and per-session result display."""
import json
import streamlit as st
from core import InferenceFailure, infer_image, png_bytes, valid_model_id, visible_predictions
from video import (analyze_frames, display_frame, encode_video, export_record,
                   sample_frames, sample_plan, video_context, video_info)


def clear_video_result():
    for key in ("video_batch","video_export","video_export_context"):
        st.session_state.pop(key,None)


def run_video_ui(mode, model_id, api_key, threshold, selected, opacity):
    check_only = mode == "영상 업로드 확인"
    if check_only:
        st.info("모델 없이 영상 업로드·구간 추출·재생을 확인합니다. 객체와 도로 영역은 예측하지 않습니다.")
    else:
        st.info("영상 분석 실행을 누르면 선택 구간에서 추출한 프레임들이 Roboflow로 전송됩니다.")
    uploaded = st.file_uploader("주행영상 업로드",type=["mp4","mov","avi"],key="video_upload")
    st.caption("최대 200MB. source.mp4 파일을 선택하세요. YouTube 주소는 강의 시청용입니다.")
    if uploaded is None:
        clear_video_result()
        return
    data = uploaded.getvalue()
    try:
        info = video_info(data)
    except ValueError as error:
        clear_video_result()
        st.error(str(error))
        return
    st.video(data)
    st.caption(f'원본: {info["width"]} × {info["height"]}px · {info["duration"]:.2f}초')
    left,middle,right = st.columns(3)
    start = left.number_input("시작 시각(초)",min_value=0.0,value=0.0,step=1.0,key="video_start")
    seconds = middle.number_input("분석 길이(초)",min_value=1,max_value=20,value=10,step=1,key="video_seconds")
    rate = right.selectbox("초당 분석 프레임",[1,2,5],index=1,key="video_rate")
    identity = video_context(data,mode,model_id,api_key,start,seconds,rate)
    if st.session_state.get("video_context") != identity:
        clear_video_result()
        st.session_state.video_context = identity
    try:
        end, expected = sample_plan(info,start,seconds,rate)
    except ValueError as error:
        clear_video_result()
        st.error(str(error))
        return
    st.caption(f"{start:.2f}~{end:.2f}초 · 최대 {expected}프레임 · "
               + ("API 호출 0회" if check_only else f"프레임별 API 요청 최대 {expected}회"))
    st.caption("첫 확인은 10초·2fps(최대 20프레임)로 시작합니다. 한 번에 최대 20초·60프레임, 긴 변 960px입니다.")
    ready = check_only or bool(api_key) and valid_model_id(model_id)
    if not check_only and model_id and not valid_model_id(model_id):
        st.warning("모델 ID는 프로젝트이름/버전번호 형식입니다.")
    if st.button("프레임 추출 확인" if check_only else "영상 분석 실행",
                 type="primary",disabled=not ready,key="analyze_video"):
        clear_video_result()
        progress = st.progress(0.0,text="프레임을 추출하고 있습니다.")
        try:
            batch = sample_frames(data,start,seconds,rate)
            if not check_only:
                batch = analyze_frames(batch,lambda image:infer_image(image,model_id,api_key),
                    lambda done,total:progress.progress(done/total,text=f"프레임 분석 {done}/{total}"))
            st.session_state.video_batch = batch
        except (ValueError,InferenceFailure) as error:
            st.error(str(error))
        finally:
            progress.empty()
    batch = st.session_state.get("video_batch")
    if batch is None:
        return
    st.subheader("추출 프레임" if check_only else "프레임별 분석 결과")
    frames = batch["frames"]
    # Options can change when a new, shorter video is uploaded.
    if st.session_state.get("frame_index",0) >= len(frames):
        st.session_state.frame_index = 0
    index = st.select_slider("확인할 프레임",options=list(range(len(frames))),
        format_func=lambda i:f'{i+1} / 원본 {frames[i]["timestamp"]:.2f}초',key="frame_index") if len(frames)>1 else 0
    item = frames[index]
    rendered = display_frame(item,threshold,selected,opacity)
    st.image(rendered,width=rendered.width)
    for message in item.get("messages",[]):
        st.warning(message)
    if "result" in item:
        visible = visible_predictions(item["result"],threshold,selected)
        objects = sum(p["class"]!="line" for p in visible)
        roads = len(visible)-objects
        st.caption(f"선택 프레임: 객체 {objects}개 · 도로 영역 {roads}개")
        if not roads:
            st.info("표시할 line 영역이 없습니다. 임계값·선택 클래스·분할 모델의 points를 확인하세요.")
    else:
        st.caption("미분석 프레임입니다. 검출 개수나 모델 정확도로 해석하지 않습니다.")
    st.download_button("선택 프레임 PNG 받기",png_bytes(rendered),"video-frame.png","image/png")
    st.caption("표시 조건과 확인 프레임을 바꿀 때는 API를 다시 호출하지 않습니다.")
    export_context = json.dumps([identity,threshold,selected,opacity])
    if st.session_state.get("video_export_context") != export_context:
        st.session_state.pop("video_export",None)
    if st.button("결과 영상 만들기",key="make_video"):
        st.session_state.pop("video_export",None)
        try:
            with st.spinner("현재 표시 조건으로 MP4를 만들고 있습니다."):
                st.session_state.video_export = encode_video(batch,threshold,selected,opacity)
                st.session_state.video_export_context = export_context
        except ValueError as error:
            st.error(str(error))
    output = st.session_state.get("video_export")
    if output:
        st.video(output)
        st.download_button("결과 MP4 받기",output,"upload-check.mp4" if check_only else "prediction-video.mp4","video/mp4")
    st.caption("MP4는 추출한 프레임을 선택한 fps로 이어 붙인 무음 확인 영상입니다. "
               "원본 전체 프레임을 분석하거나 실시간 추적한 결과가 아닙니다. 표시 변경 후 MP4를 다시 만들 수 있습니다.")
    record = export_record(batch,model_id if not check_only else "",threshold,selected,opacity)
    st.download_button("영상 분석 기록 JSON 받기",json.dumps(record,ensure_ascii=False,indent=2).encode("utf-8"),
                       "video-analysis.json","application/json")
