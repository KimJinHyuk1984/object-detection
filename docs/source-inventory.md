# 자료 목록

| 자료 ID | 위치 | 유형 | 크기·수량 | 확인 범위 | 본문 사용 |
| --- | --- | --- | --- | --- | --- |
| source-001 | source.mp4 | MP4 영상 | 158,322,490바이트 | MP4 메타데이터: 약 301.49초, 1920×1080, 30fps, 영상 9,043프레임. SHA-256은 protected-baseline.json에 기록. 전체 장면 검토·개인정보 전수 검사는 미실행. | 메타데이터만 인용. 원본 영상 링크·복사·업로드 없음. |
| source-002 | img_data/ | 교재 사진 | JPG 17장 | 기존 직캠 교재 사진. 이번 차시 재사용·변환·OCR 없음. 새 내용의 출처로 사용하지 않음. | 사용 안 함 |
| source-003 | Roboflow 공식 Annotate an Image 문서 | 웹 문서 | 1개 | 2026-10-17 확인: 박스·폴리곤·마스크 도구, 다각형 닫기, 라벨 선택·검수 | 일반적인 도구 설명과 출처 링크 |
| source-004 | captures/lesson-01/ | 사용자 제공 캡처 | PNG 6장 | 6장 시각 확인. 프로젝트 Object Detection, car 박스, line 폴리곤, 작업 목록. 원본 메타·해시는 lesson-01-capture-checks.json 참조. | 앞 4장 원본과 동일한 PNG 복사. 계정 정보가 있는 04.png·04(1).png는 비공개 원본 보관. |
| source-005 | Roboflow 공식 Polygons for Object Detection 설명 | 웹 문서 | 1개 | 2026-10-17 확인: 폴리곤 어노테이션을 사용해도 탐지 모델은 박스를 출력함. | 모델 유형 확인 안내·출처 링크 |
| source-006 | https://www.youtube.com/watch?v=ihokShSN51Y | 사용자 지정 YouTube 영상 | 영상 ID ihokShSN51Y | 표준 임베드 주소·정적 마크업 확인. 브라우저 연결 없음, 실제 재생·임베드 허용 여부 미확인. | SOURCE VIDEO 플레이어와 YouTube에서 열기 링크 |

원본 자료는 이동·삭제·수정하지 않았습니다. source.mp4는 작업 전후 해시가 같습니다.
원본 영상·사진·캡처는 .gitignore에서 제외하고, git ls-files로 현재 미추적 상태를 확인했습니다.
캡처 4장의 공개용 복사본을 assets/img/lesson-01/에 만들었습니다. PNG 글자·경계를 보존하기 위해 파일 형식을 유지했으며 원본과 SHA-256이 같습니다. 실습 코드 파일은 없습니다.
공식 문서: https://docs.roboflow.com/annotate/use-roboflow-annotate

폴리곤과 탐지 출력 근거: https://blog.roboflow.com/polygons-object-detection/

YouTube 임베드 방식 근거: https://developers.google.com/youtube/player_parameters

## 2차시 추가 자료

2026-10-17에 Roboflow의 공식 자료를 확인했습니다. 설명용 표·격자와 가상 오류는 새로 작성한 교육용 예시이며 실제 사용자 모델 결과가 아닙니다.

| 자료 ID | 위치 | 확인 내용 | 본문 사용 |
| --- | --- | --- | --- |
| source-007 | https://roboflow.com/blog/train-test-split | Train·Valid·Test 역할, 분리 후 학습 데이터 증강 | 분리 개념과 설명용 비율 |
| source-008 | https://roboflow.com/blog/robotics-training-data | 촬영 회차·영상 단위 분리와 인접 프레임 누출 | 현재 단일 영상의 분리 한계 설명 |
| source-009 | https://roboflow.com/blog/best-practices-for-training-yolo | 데이터 버전·기준 실험·작은 대상의 입력 크기 | 첫 버전과 비교 계획 |
| source-010 | https://roboflow.com/blog/instance-segmentation | 분할 데이터·버전·모델 학습·미리보기 흐름 | 계정 제공 옵션을 확인하는 학습 절차 |
| source-011 | https://roboflow.com/blog/mean-average-precision | Precision·Recall·AP·mAP와 IoU 기준 | 지표 해석과 자체 계산 예시 |
| source-012 | https://roboflow.com/blog/roboflow-training-graphs | Box·Mask IoU, mAP 기준과 학습 그래프 | 평가 값의 정확한 이름 기록 |

2차시 사용자 캡처는 아직 없습니다. API 키·실제 모델 식별자·성능 수치를 수집하거나 가정하지 않았습니다. 다운로드 활동지는 이 수업용으로 새로 작성했으며 실행 코드가 아닙니다.

## 3차시 추가 자료

2026-10-17 확인. 사용자 상태는 어노테이션 진행 중이며 실제 API 키·모델 ID·응답은 받지 않았습니다.

| 자료 ID | 위치 | 확인·사용 |
| --- | --- | --- |
| source-013 | https://inference.roboflow.com/quickstart/roboflow_ecosystem/ | InferenceHTTPClient와 hosted Serverless의 단일 모델 요청 |
| source-014 | https://github.com/roboflow/computer-vision-skills/blob/main/skills/roboflow-api-reference/inference.md | 중심 박스 좌표·instance segmentation points 응답 |
| source-015 | https://docs.streamlit.io/develop/concepts/connections/secrets-management | secrets.toml의 비밀 설정 |
| source-016 | https://docs.streamlit.io/develop/api-reference/caching-and-state/st.session_state | 사용자 세션의 결과 보관과 재실행 |
| source-017 | https://docs.streamlit.io/develop/api-reference/app-testing/st.testing.v1.apptest | 브라우저와 구분하는 AppTest 자동 검사 |
| source-018 | files/lesson-03/demo.py | 직접 그린 가상 도로와 손으로 작성한 9개 예제 결과. 실제 모델 예측 아님 |

공식 PyPI에서 Streamlit 1.66.0·inference-sdk 1.8.0·Pillow 12.3.0을 설치해 테스트했습니다. SDK의 설치된 코드·서명에서 polygon 응답·header 키 전송 설정을 확인했습니다.
assets/img/lesson-03/demo-result.png는 앱의 그리기 함수로 만든 예제 결과이며 DEMO 표시를 포함합니다. 사용자 원본 영상·캡처를 새로 복사하지 않았습니다.

## 영상 업로드 테스트 추가 근거

| 자료 ID | 위치 | 확인·사용 |
| --- | --- | --- |
| source-019 | 사용자 요청: 테스트는 영상 업로드로 확인 | 기본 입력을 영상으로 변경, 3차시 앱·강의·PDF 반영 |
| source-020 | https://docs.streamlit.io/develop/api-reference/media/st.video | 브라우저 영상 표시·H.264 출력 안내 |
| source-021 | https://pyav.basswood.io/docs/stable/cookbook/basics.html | 프레임 디코딩·H.264 인코딩 |
| source-022 | https://pyav.basswood.io/docs/stable/api/container.html | stream time_base·seek·decode |

기존 source-001에서 로컬로 첫 10초·20프레임을 추출하고 MP4 인코딩·디코딩을 검사했습니다. 해당 테스트 산출물은 Git에서 제외된 work-temp/에만 저장했으며 외부로 전송하지 않았습니다. 원본 SHA-256은 변하지 않았습니다. PyAV가 읽은 영상 트랙 길이는 301.433초이며 앞서 기록한 약 301.49초는 컨테이너 메타데이터입니다.

## 어노테이션·학습 완료 후 추가 자료 (2026-10-18)

| 자료 ID | 위치 | 확인·반영 |
| --- | --- | --- |
| source-023 | captures/lesson-03/1.png~6.png | 6장 시각 확인. 201장 완료·분리·전처리·증강·생성 선택. 2·3·5·6번만 계정 정보 없는 공개 복사본으로 2차시 안내에 반영 |
| source-024 | 사용자 “모델학습도 완료” | 학습 완료 상태 반영. 모델 유형·지표·예측·API 정보는 별도 확인 |

이전에 기록한 “어노테이션 진행 중”, “2차시 캡처 없음”은 당시 상태입니다. 최신 자료의 해석·확인할 점은 [캡처 검토](training-capture-review.md)에 기록합니다. 캡처에 보이는 설정과 실제 학습된 모델의 최종 구성을 구분하며, 성능 수치나 line 출력 성공을 추정하지 않습니다.

## 학습 결과·클래스 통계 추가 자료 (2026-10-18)

| 자료 ID | 위치 | 확인·반영 |
| --- | --- | --- |
| source-025 | captures/lesson-03/7.png~12.png | 6장 추가 시각 확인. 201장·2,972개 정답, 9개 사용 클래스, lampy 4개, 빈 이름 2개, v1 RF-DETR Object Detection (Small), Test 20장 평가. 7·8·11·12번 공개 복사 |
| source-026 | https://discuss.roboflow.com/t/roboflow-missing-yolov8-instance-segmentation-weight-pt-segmentation-version-to-download-how-to-train-and-deploy-with-segmentation-masks/8942 | Roboflow 담당자 답변: Object Detection 프로젝트를 Duplicate Project에서 Instance Segmentation으로 복제하는 순서 |
| source-027 | https://rfdetr.roboflow.com/latest/learn/run/segmentation/ | RF-DETR의 분할 모델과 마스크 출력 확인. 현재 탐지 모델과 구분 |

현재 학습 결과는 박스 평가로 반영했습니다. 도로 마스크 성공, API model_id, 실제 API 호출 성공은 추정하지 않았습니다. 9번의 계정 식별 정보와 10번의 사용량·결제 관련 영역은 공개 이미지로 복사하지 않았습니다. 원본 12장·공개 복사본 8장의 해시·정적 검사는 training-result-checks.json을 참고합니다.

## Python 3.11 호환성 추가 근거 (2026-10-18)

| 자료 ID | 위치 | 확인·사용 |
| --- | --- | --- |
| source-028 | https://pypi.org/project/av/18.1.0/ | Requires-Python >=3.11, cp311-abi3 Windows x86-64 wheel. 두 Python 버전의 공통 의존성으로 적용·실행 검사 |
| source-029 | https://www.python.org/downloads/release/python-3119/ | 공식 64비트 embeddable 패키지·체크섬. work-temp의 실제 Python 3.11 테스트에만 사용 |

## 바운딩 박스·인스턴스 세그멘테이션 비교 보강 (2026-10-18)

| 자료 ID | 위치 | 확인·사용 |
| --- | --- | --- |
| source-030 | https://roboflow.com/blog/instance-segmentation | 객체 탐지의 박스와 인스턴스 분할의 객체별 마스크·출력 비교. 동일 장면 개념도·표를 직접 작성 |

폴리곤과 탐지 출력의 관계는 기존 Polygons for Object Detection 근거를 유지했습니다. 해당 링크는 이번 웹 도구 재조회에서 접근 오류가 났으며 새로 검증한 것으로 기록하지 않습니다. 개념도는 실제 학습 모델의 결과가 아니며 별도 영상 추적 기능을 뜻하지 않습니다.

## 영상 결과 자동 재생 요청 (2026-10-18)

| 자료 ID | 위치 | 확인·사용 |
| --- | --- | --- |
| source-031 | 사용자 제공 Gradio·Roboflow Workflow 얼굴 탐지 코드 | 분석 후 결과를 반복 재생하는 사용 흐름 참고. 사용자가 작동한다고 설명했으며 여기서 해당 코드를 실행하거나 Workflow를 호출하지 않음 |
| source-020 재확인 | https://docs.streamlit.io/develop/api-reference/media/st.video | Streamlit 1.66.0의 autoplay·loop·muted 옵션과 브라우저 자동 재생 조건 확인 |

기존 단일 모델 추론 방식을 유지했고 Gradio·마이크로비트·소리 재생 의존성은 추가하지 않았습니다. 재생 검사는 로컬 영상과 대체 API 응답으로 수행했습니다.

## 원본 영상 재생과 분석 빈도 분리 (2026-10-18)

| 자료 ID | 위치 | 확인·사용 |
| --- | --- | --- |
| source-032 | 사용자 “프레임 추출이 아니고 … 재생되는 영상에 나오도록” | 영상 플레이어 중심 UI, 원본 영상 장면·재생 시간 간격 유지 요청 |
| source-033 | https://pyav.basswood.io/docs/stable/api/time.html | PTS·time_base와 인코더 타임스탬프 처리 확인. 실제 설치된 PyAV 18.1.0에서 동작 검사 |

source.mp4의 실제 30fps 영상으로 10초·300프레임 출력과 길이를 확인했습니다. 저빈도 분석 사이의 표시는 가장 최근 결과를 유지하는 방식이며, 객체 추적이나 새 추론 결과로 간주하지 않습니다.


## 전체 길이 영상 사용 요청 (2026-10-18)

| 자료 ID | 위치 | 확인·사용 |
| --- | --- | --- |
| source-034 | 사용자 “3분짜리 영상을 … 그냥 쓰면 안되?” | 전체 영상 기본 선택, 고정 길이·분석 장면 수 상한 제거, 실제 길이에 따른 API 요청 수와 처리 진행률 표시 |

기존 source-001을 로컬에서만 사용해 180초 구간 검사를 수행합니다. 최신 결과는 [전체 영상 검사](lesson-03-full-video-checks.json)에 기록합니다. 외부 API 호출이나 원본 업로드는 하지 않았습니다.


## Drive Vision 전면 개편 근거 (2026-10-18)

| 자료 ID | 위치 | 확인·사용 |
| --- | --- | --- |
| source-035 | https://github.com/gamza-lab/object-detection-with-microbit | 사용자 지정 템플릿. main 9fe43f91b726531ff20c171628f1297db7241873의 app.py·README 확인. Workflow base64 이미지 배열과 Bearer 헤더 요청 구조 참고. 참조 저장소는 수정·실행하지 않음 |
| source-036 | https://developer.mozilla.org/en-US/docs/Web/API/HTMLVideoElement/requestVideoFrameCallback | 원본 영상과 별도 Canvas 표시 구조 검토. 최종 구현은 현재 video.currentTime과 requestAnimationFrame으로 표시 갱신 |
| source-037 | https://pypi.org/project/fastapi/ · https://pypi.org/project/uvicorn/ · https://pypi.org/project/requests/ | Python 지원 메타데이터 확인 및 FastAPI 0.143.3·Uvicorn 0.54.0·requests 2.34.2 실제 설치 검사 |

새 화면 예제는 직접 작성한 Canvas 가상 도로이며 실제 모델 결과·사용자 원본 영상이 아닙니다. 테슬라 로고·제품 이미지는 사용하지 않았습니다. 모델 API·원본 영상의 외부 전송은 수행하지 않았습니다.
