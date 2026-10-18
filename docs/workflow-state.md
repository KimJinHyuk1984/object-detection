# 작업 상태

## 사용자 결정과 이번 범위

- 강의: 자율주행 자동차 모델 만들기(by Object Detection), 50분 × 4차시.
- 모델 하나로 9개 클래스를 인식하고 Roboflow API·Streamlit으로 배포하는 계획.
- 라벨: car, motor, people, sign, lampg, lampr, lampy, lamp, line.
- lampg/lampr/lampy는 초록/빨강/노랑, lamp는 색 구분이 어려운 신호등. sign은 표지판.
- line은 차선 사이의 주행 가능한 도로 영역. 원본은 source.mp4.
- 2026-10-17: 1차시 제작 요청에 따라 기존 1차시·캡처·YouTube 연결을 작성.
- 2026-10-17: 사용자 “이제 다음 작업하자”에 따라 다음 순서인 2차시를 제작. 이어 “아직 어노테이션 하고 있어”라고 현재 상태를 확인했으므로 학습 완료를 전제하지 않음.

2026-10-17 사용자 “다음작업하자”에 따라 이번 범위는 3차시 강의·Streamlit 영상 테스트 앱·실습 ZIP·PDF 활동지·교사용 안내와 검사입니다. 사용자 “아직 어노테이션 중” 답변을 반영해 처음에는 예제 모드를 기본으로 구성했고, 영상 업로드 테스트 요청을 반영해 “영상 업로드 확인”을 기본으로 변경했습니다. 승인된 4차시 구성에 맞춰 루트는 강의 목록, 1차시와 2차시는 하위 페이지로 구성했습니다. 3차시 초안을 추가했고 4차시는 준비 중입니다. WORKFLOW의 특정 단계 번호 실행 요청은 아닙니다.

## 최신 상태 · 2026-10-18

captures/lesson-03/1.png~12.png로 201장 어노테이션·정답 2,972개와 RF-DETR Object Detection (Small) v1 학습 완료를 확인했습니다. Test 20장: mAP@50 47.3%, Precision 53.0%, Recall 41.2%, F1 45.9%. 공개 가능한 설정·데이터·평가 화면 8장을 2차시 자료에 반영했습니다. 현재 모델은 박스 출력이므로 Instance Segmentation 복제·정답 보존 확인·분할 학습이 다음 단계입니다. 실제 도로 마스크 예측과 API 요청 코드는 아직 없습니다. [캡처 검토](training-capture-review.md)를 참고합니다. 이전 2026-10-17 기록의 “어노테이션 진행 중”은 당시 상태입니다.

## 산출물

- index.html: 4차시 목록. 1·2·3차시 링크, 4차시 준비 중.
- road-perception/index.html: 기존 1차시 5개 섹션·21개 발표 조각. 영상과 캡처 유지.
- model-training/index.html: 2차시 5개 섹션·20개 발표 조각, 8+10+8+10+14=50분.
- data/site.js: 4차시 메타데이터. 기존 1차시 slug와 instructor 데이터 유지.
- assets/css/lecture.css: 차시 링크·분리 비율·표·IoU 도식 스타일.
- files/lesson-02-workbook.pdf: 데이터·버전·학습·오류 분석용 A4 4쪽 활동지. TXT 원문도 보존.
- scripts/create_lesson02_workbook.py: PDF 생성 원본. ReportLab과 한글 글꼴 사용.
- docs/lesson-02-capture-guide.md, lesson-02-teacher-guide.md: 캡처 시점과 50분 진행안.
- docs/lesson-02-verification.md 및 정적·HTTP JSON: 실제 수행 범위와 제한.
- docs/protected-baseline.json: 최초 보호 파일·영상 기준 유지.

완료된 초안 섹션: 1차시 road-mission / vision-concepts / annotation-ready / annotation-practice / annotation-review. 2차시 training-ready / dataset-split / dataset-version / model-training / model-evaluation.

## 미해결 항목

- Q01: 해결 — 10.png에서 RF-DETR Object Detection (Small) 확정. 남은 작업은 Instance Segmentation 프로젝트 복제·분할 학습과 line 마스크 확인.
- Q02: 일반 객체의 저장 정답 형식·분할 학습 호환성. car 캡처에는 박스가 보이며 모든 저장 형식은 아직 확인하지 못함.
- Q03: sign의 포함 범위·지지대, line의 차로·차량/장애물·가림 처리 기준.
- Q04: v1 학습과 Test 20장 평가를 9~12.png에서 확인. v1은 증강 후 483장·88/8/4 비율, 전처리 2개·증강 3개. 최종 세부 설정과 장면 누출 여부는 별도 확인. lampy 정답 4개로 분리별 수·보강 필요.
- Q05: 연결된 브라우저 없음. 실제 발표 모드·모바일·테마·입력·YouTube 재생 검증 미실행.
- Q06: 12장 수신·검토 완료. 데이터·모델 종류·지표 확인. 남은 것은 분할 프로젝트의 정답 유지·실제 예측·Deploy 요청 코드. 표시 Model URL을 API model_id로 추정하지 않음.

## 다음 실행 조건

현재 프로젝트·v1 모델을 보존하면서 Instance Segmentation으로 복제하고 line 폴리곤·객체 정답·클래스·분리 보존을 먼저 확인합니다. 분할 모델 학습 후 실제 line 마스크와 Deploy 요청 코드를 확인하고 학습에 쓰지 않은 블랙박스 영상의 짧은 구간으로 3차시 앱을 테스트합니다.

Roboflow 데이터 이동·프로젝트 변경·학습·커밋·푸시·외부 배포는 수행하지 않았습니다. 보호 파일·원본은 수정하지 않았으며 해시 검사 결과는 2차시 검증 기록에 남깁니다.

## 3차시 추가 산출물

- api-app/index.html: 5개 섹션·18개 발표 조각, 8+10+10+14+8=50분.
- files/lesson-03/: Streamlit 앱과 설정 예시·실행 안내. 실제 비밀키 없음.
- files/lesson-03.zip: 공개 실습 파일 12개만 포함.
- files/lesson-03-workbook.pdf: A4 2쪽. 두 페이지를 렌더링해 확인.
- tests/test_lesson03.py 및 test_lesson03_video.py: 이미지·영상 처리·SDK 호출 경계·세션 재실행 총 12개 테스트.
- docs/lesson-03-teacher-guide.md, lesson-03-capture-guide.md, lesson-03-verification.md: 운영·확인 기록.

실제 Roboflow 추론은 수행하지 않았습니다. SDK 호출 검사는 대체 응답을 사용했고, 앱 조작은 Streamlit AppTest로 검증했습니다. 실제 브라우저 검사와 구분합니다. 분할 모델을 준비한 뒤 실제 model_id·Serverless 지원·line points를 확인하면 연결을 검증할 수 있습니다.

## 영상 업로드 테스트 반영 (2026-10-17)

사용자 “테스트는 영상을 업로드 해서 확인할꺼야”에 따라 3차시 제목·앱·실습 ZIP·PDF·캡처 안내를 수정했습니다. 기본 입력은 영상 업로드이며 모델 없이 확인하는 모드를 제공합니다. 실제 모드에서는 프레임마다 같은 단일 모델을 호출합니다. 0초부터 10초·2fps를 기본값으로 사용하고, 한 번에 최대 20초·60프레임을 처리합니다.

source.mp4에서 20프레임을 추출해 960×540·10초 H.264 MP4로 인코딩·디코딩했습니다. API 실제 호출은 0회입니다. 12개 테스트 통과, PDF 2쪽 렌더링 육안 확인 완료. 실제 모델의 인식 성능과 브라우저 재생은 아직 확인 전입니다. 4차시 페이지는 준비 중이며 다음 범위는 배포와 실제 모델 결과 점검입니다. 최신 검사 근거는 lesson-03-video-checks.json과 lesson-03-verification.md의 영상 업로드 반영 항목입니다.

## CMD 실행 안내 추가

사용자 요청에 따라 3차시 실행 명령 옆에 CMD 안내를 추가했습니다. PowerShell·CMD 중 사용하는 터미널 한 가지를 선택하며 두 방식 모두 가상환경 Python을 직접 실행합니다. CMD 원문 run-local-cmd.txt를 공개 ZIP에 포함해 총 12개 파일입니다. 발표 조각 수와 앱 동작은 그대로입니다.

## 분할 모델 재학습 시작·Streamlit 표시 오류 수정 (2026-10-18)

사용자가 Instance Segmentation 안내 이후 재학습을 시작했다고 알렸습니다. 새 모델의 완료·예측은 아직 확인하지 않았습니다. 기다리는 동안 발생한 Streamlit 이미지 폭 TypeError를 수정하고 실습 ZIP을 다시 만들었습니다.

입력·결과·영상 프레임에는 정수 폭을 사용하고 표는 자동 폭으로 표시합니다. 현재 기준 환경에서 12개 테스트가 통과했습니다. 영상 실습은 Python 3.12·Streamlit 1.66.0 가상환경으로 실행합니다. 구버전의 최소 이미지 오류 재현·수정은 확인했지만 구버전 전체 앱 검증은 통과하지 못했습니다. 상세 결과는 lesson-03-verification.md의 최신 항목을 참고합니다.

## Python 3.11·3.12 공통 실습 지원 (2026-10-18)

사용자의 Python 3.11 지원 요청을 반영했습니다. 최신 requirements는 Streamlit 1.66.0, inference-sdk 1.8.0, Pillow 12.3.0, PyAV 18.1.0입니다. 실행 안내는 3.11 기준이며 3.12도 지원합니다.

실제 Python 3.11.9와 3.12.14에서 각각 12개 테스트가 통과했습니다. 3.11에서는 source.mp4 10초·20프레임 추출과 960×540 H.264 MP4 인코딩·디코딩도 확인했습니다. 최신 ZIP·검증 정보는 lesson-03-python-compatibility-checks.json 및 lesson-03-verification.md를 참고합니다. 이전 기록의 “3.12 필수”는 PyAV 19.0.1을 사용하던 시점의 안내입니다.

## 1차시 박스·마스크 비교 안내 보강 (2026-10-18)

사용자 요청에 따라 기존 개념 10분 안에서 같은 도로의 박스·인스턴스 마스크 도식, 비교표, 단일 분할 모델에서 객체 박스와 line 도로 마스크를 표시하는 과정을 보강했습니다. 1차시 21개·50분, 전체 59개 발표 조각을 유지합니다. 2차시 학습 전 점검에 비교 안내 링크를 연결했습니다. 교사용 진행안과 동일 프레임의 실제 예측 캡처 안내를 추가했습니다. 새 분할 모델의 학습 완료·실제 출력은 아직 확인 전이며 추가 캡처는 완료 후 준비합니다.
