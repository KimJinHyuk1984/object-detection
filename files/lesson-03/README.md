# Drive Vision · 주행 인식 대시보드

원본 영상을 브라우저에서 재생하면서 자동차·사람·신호등 등의 박스와 line 도로 마스크, 예측 신뢰도(%)를 겹쳐 표시합니다. 신호등 색에 따라 주행·감속·정지·확인 안내를 보여 줍니다. line은 차선 사이의 주행 가능한 도로 영역입니다.

기존 Streamlit·MP4 재인코딩 버전을 교체했습니다. Python 3.11 또는 3.12에서 실행하며, 이제 실행 명령은 **python app.py**입니다.

## 실행

ZIP을 새 폴더에 풀고 app.py가 있는 폴더에서 실행합니다.

PowerShell:

~~~powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe app.py
~~~

CMD:

~~~cmd
py -3.11 -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe app.py
~~~

Python 3.12를 쓰면 첫 줄만 -3.12로 바꿉니다. 브라우저에서 **http://127.0.0.1:7862**를 엽니다. 종료는 터미널에서 Ctrl+C입니다. 다른 Python으로 만든 기존 가상환경에 덮어 설치하지 말고 새 폴더에서 시작하세요.

이 앱은 Python 서버가 필요합니다. GitHub Pages는 강의·ZIP 다운로드를 제공하며, 다운로드한 앱의 API 서버를 실행하지는 않습니다. Streamlit Community Cloud용 앱이 아닙니다.

## Workflow 연결

1. Roboflow에서 **Instance Segmentation** 모델을 사용하는 Workflow를 준비합니다.
2. 이미지 입력 이름을 확인합니다. 기본 이름은 image입니다.
3. 모델 블록의 **Predictions**를 Workflow Outputs에 연결합니다. 기본 출력 이름은 predictions입니다.
4. Deploy Workflow → Cloud API의 **Workspace ID와 Workflow ID**를 복사합니다. 모델 표시 이름이나 Model URL은 Workflow ID가 아닙니다.
5. 앱의 **연결 설정**에서 두 ID와 Private API Key를 입력하고 설정 적용을 누릅니다.
6. 입출력 이름이 다르면 연결 설정의 펼침 메뉴에서 맞춥니다.

API 응답은 outputs 배열의 각 항목에 predictions.predictions와 이미지 크기가 있는 구조를 사용합니다. 모델 하나에서 car, motor, people, sign, lampg, lampr, lampy, lamp, line을 출력해야 합니다. line에는 points가 필요합니다. 폴리곤 없는 line은 박스로 대신 채우지 않고 안내를 표시합니다.

키는 입력창·요청 처리 메모리에서만 사용하며 파일, 브라우저 저장소, JSON 다운로드, 로그에 넣지 않습니다. 서버 환경 변수 ROBOFLOW_API_KEY, ROBOFLOW_WORKSPACE, ROBOFLOW_WORKFLOW도 지원합니다. 선택 변수는 ROBOFLOW_INPUT, ROBOFLOW_OUTPUT입니다. 이전 secrets.toml은 읽지 않습니다.

## 영상 재생과 분석

- **영상 선택**: 로컬 영상 파일을 선택하면 즉시 원본 재생을 사용할 수 있습니다. 브라우저가 지원하는 MP4(H.264)를 권장합니다. MOV는 내부 코덱에 따라 재생되지 않을 수 있습니다.
- **분석 시작**: 화면 뒤에서 장면을 긴 변 640px JPEG로 준비하고 기본 8장씩 Workflow에 보냅니다. 완료된 구간부터 박스·도로 마스크가 표시됩니다. 원본 영상 전체나 새 MP4를 서버에 올리거나 만들지 않습니다.
- 기본은 **초당 2회 분석**입니다. 3분이면 360장, 묶음 8장이면 정상 완료 시 약 45개 HTTP 요청입니다. 재생 자체는 원본 영상 속도를 유지합니다. 분석 중 탐색하면 묶음 구성이 달라질 수 있습니다.
- **묶음 요청 1회가 이미지 1장 사용량을 뜻하지 않습니다.** 처리 이미지 수와 Roboflow 정책에 따라 사용량이 발생합니다.
- **분석 결과에 맞춰 재생**이 기본입니다. 현재 구간의 결과가 아직 없으면 잠시 대기하고 준비되면 자동으로 이어집니다. 끄면 원본은 계속 재생하고 미분석 구간의 박스·마스크·신호 안내는 지웁니다.
- 현재 분석 시점의 결과를 다음 분석 시점 전까지 표시합니다. 객체 추적·좌표 보간은 하지 않습니다. 신호등·차량의 빠른 변화는 분석 빈도와 모델 정확도에 영향을 받습니다.
- **분석 중지**는 새 요청과 재생을 중지합니다. 완료된 결과는 보관하고 분석 이어하기로 재사용합니다. 이미 서버로 보낸 요청은 처리될 수 있습니다.
- 재생·일시정지·탐색·반복·임계값·불투명도·클래스 변경에는 추가 API 요청이 없습니다. 다만 분석 실행 중에는 아직 분석하지 않은 구간의 작업이 계속됩니다.
- 영상 또는 연결 설정·분석 빈도·묶음 크기를 바꾸면 이전 결과를 지웁니다. 새로고침하면 브라우저 메모리의 결과와 입력 키는 사라집니다.
- **현재 화면 저장**은 영상·겹쳐 그린 결과·신호 안내를 PNG로 저장합니다. **분석 기록 JSON**에는 시각별 좌표와 점수를 저장합니다. 결과 MP4 재인코딩·다운로드는 이 버전에 없습니다.
- **화면 예제 보기**는 직접 만든 가상 도로입니다. API 없이 신호 변화와 표시를 확인하며 실제 모델 결과가 아닙니다.

긴 영상도 그대로 선택합니다. 이전 10초·20초·300프레임·200MB 고정 제한은 없습니다. 파일 크기와 코덱은 브라우저·컴퓨터의 처리 여건에 영향을 받습니다. API 지연이 없어지는 것은 아니며, 재인코딩 대기를 없애고 작은 묶음부터 보여 주는 구조입니다.

## 신호 안내

| 감지 클래스 | 화면 안내 |
| --- | --- |
| lampr | 정지 · 빨간 신호가 감지되었습니다 |
| lampy | 감속 · 속도를 줄이고 정지를 준비하세요 |
| lamp | 신호 확인 · 색을 구분하기 어렵습니다 |
| lampg | 주행 · 조심히 가세요. 주변을 확인하세요 |
| 신호 없음 | 신호 확인 |
| 현재 시각의 분석 결과 없음 | 분석 대기 |

여러 신호가 감지되면 빨강 → 노랑 → 색 미확인 → 초록 순으로 우선합니다. 표시 임계값 이상인 예측만 사용합니다. 표시할 객체를 숨겨도 신호 판정은 유지합니다. 어느 차로에 적용되는 신호인지 판단하지 않으므로 **학습용 안내이며 실제 운전 판단에 사용하지 않습니다.** 퍼센트는 개별 예측 신뢰도이며 정확도나 안전 확률이 아닙니다.

## 오류 확인

- 401/403: Private API Key와 Workspace 접근 권한을 확인합니다.
- 404: Deploy Workflow의 Workspace·Workflow ID를 확인합니다.
- outputs 수 불일치/413/시간 초과: 요청 묶음 크기를 1 또는 4로 줄여 확인합니다.
- 예측 출력 없음: Workflow Outputs가 시각화 이미지가 아닌 Predictions인지 확인합니다.
- line 없음: Instance Segmentation 모델, points, 최소 신뢰도를 확인합니다.
- 화면은 재생되지만 결과 없음: 연결 설정, 분석 시작, 현재 구간의 분석 완료 여부를 확인합니다.
- 서버 없이 HTML을 직접 열면 분석을 사용할 수 없습니다. 위 실행 명령과 주소를 사용합니다.

## 구조와 참고

- app.py: 로컬 FastAPI 서버와 요청 검증
- workflow.py: 템플릿의 Workflow 배열 요청 방식과 응답 변환
- core.py: 클래스·박스·폴리곤 좌표 검증
- web/: 영상 플레이어, Canvas 표시, 신호 판정, 대시보드 디자인

참고 템플릿: [gamza-lab/object-detection-with-microbit](https://github.com/gamza-lab/object-detection-with-microbit). Workflow의 base64 이미지 배열·Bearer 헤더 요청 방식을 참고했습니다. 얼굴 탐지·Gradio 이미지 스트리밍·마이크로비트·효과음은 이번 도로 영상 대시보드에 포함하지 않습니다.

자동 검사: Python API 계약 14개와 JavaScript 신호·시각·캐시 검사 13개, 재생 제어 통합 검사 1개. 실제 모델 API와 브라우저 재생·레이아웃 확인은 별도로 필요합니다.
