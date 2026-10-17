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
