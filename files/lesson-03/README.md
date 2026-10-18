# 3차시 실습 - 도로 영상 테스트 앱

50분 수업용 Streamlit 앱입니다. 모델 하나의 결과에서 일반 객체는 박스, line은 반투명 도로 영역으로 표시합니다.

기본 **영상 업로드 확인** 모드에서는 모델 없이 source.mp4의 업로드·추출·MP4 생성을 확인합니다. 객체 검출은 하지 않습니다. **예제 결과로 연습**은 가상 도로와 손으로 작성한 예측으로 표시 원리를 연습하는 보조 모드입니다. 두 모드는 API를 호출하지 않습니다.

## 실행 준비

64비트 Python 3.11 또는 3.12와 인터넷 연결이 필요합니다. ZIP을 풀었다면 이 README와 app.py가 있는 폴더에서 터미널을 엽니다. 저장소를 복제했다면 먼저 다음 폴더로 이동합니다.

~~~powershell
cd files/lesson-03
~~~

사용하는 터미널에 맞춰 **PowerShell 또는 CMD 중 한 가지**를 선택해 세 명령을 순서대로 실행합니다. 아래 명령은 Python 3.11 기준입니다. 3.12를 사용한다면 첫 줄의 -3.11을 -3.12로 바꾸면 됩니다. 설치는 수업 전에 마치는 것이 좋습니다.

이미 다른 Python 버전으로 만든 .venv가 있다면 기존 환경을 덮어쓰지 말고, 새 폴더에 ZIP을 풀어 해당 버전의 가상환경을 만드세요.

### PowerShell

~~~powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
~~~

### CMD(명령 프롬프트)

~~~bat
py -3.11 -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m streamlit run app.py
~~~

두 방식 모두 가상환경의 Python을 직접 실행하므로 별도로 activate할 필요가 없습니다.
브라우저에서 터미널에 표시된 Local URL을 엽니다. 종료는 터미널에서 Ctrl+C입니다.
기본 **영상 업로드 확인**에서 source.mp4를 선택하고 **프레임 추출 확인 → 결과 영상 만들기**를 누릅니다. 이미 설치했다면 requirements.txt 설치 명령을 다시 실행해 영상 처리 패키지를 추가하세요.
설치 명령 원문은 PowerShell용 run-local.txt와 CMD용 run-local-cmd.txt에도 있습니다. macOS/Linux에서는 가상환경 Python 경로가 .venv/bin/python입니다.

## Streamlit 이미지 폭 오류가 날 때

`TypeError: '<=' not supported between instances of 'str' and 'int'`가 `st.image(..., width="stretch")`에서 발생하면, 실행 중인 Streamlit이 문자열 폭을 지원하지 않는 버전입니다. 수정본은 입력·결과 이미지와 영상 프레임에 숫자 픽셀 폭을 전달하고, 결과 표는 기본 자동 폭을 사용합니다.

다운로드해 둔 이전 실습 폴더는 저장소 수정으로 자동 갱신되지 않습니다. 새 ZIP을 별도 폴더에 풀고 위의 가상환경 설치·실행 명령을 사용하세요. 기존 secrets.toml이 있다면 로컬에서 새 폴더로 옮길 수 있습니다.

이 실습은 Python 3.11과 3.12에서 사용할 수 있도록 PyAV 18.1.0을 지정합니다. 이전 ZIP의 av==19.0.1은 3.11에서 설치할 수 없으므로 최신 requirements.txt도 함께 교체하세요. 이미지 폭 오류의 직접 원인은 Python 3.11이 아니라 Streamlit API 차이이며, 지정한 Streamlit 1.66.0을 설치해 사용합니다.

설치한 환경과 실행 환경을 다음 명령으로 확인할 수 있습니다(PowerShell·CMD 공통).

~~~bat
.\.venv\Scripts\python.exe -c "import sys, streamlit; print(sys.executable); print(sys.version); print(streamlit.__version__)"
~~~

프로젝트의 .venv 경로, 선택한 Python 3.11 또는 3.12, Streamlit 1.66.0이 출력되어야 합니다. 전역 `streamlit run app.py` 대신 같은 가상환경의 `python.exe -m streamlit run app.py`를 사용합니다.

## 실제 모델 연결 - 학습이 끝난 뒤

1. 모델의 Deploy 안내에서 Instance Segmentation과 Serverless 지원 여부를 확인합니다. 모델 ID는 보통 프로젝트이름/버전번호 형식입니다.
2. .streamlit/secrets.toml.example을 같은 폴더의 secrets.toml로 복사합니다.
3. 복사한 파일에 실제 ROBOFLOW_API_KEY와 ROBOFLOW_MODEL_ID를 입력합니다. 이 파일은 Git과 배포 ZIP에 넣지 않습니다.
4. 앱을 다시 시작하고 **내 모델로 분석**을 선택합니다. **영상 업로드**에서 파일·구간·fps를 정하고 **영상 분석 실행**을 누릅니다.

같은 이름의 환경 변수도 사용할 수 있으며 환경 변수가 먼저 적용됩니다. API 키를 코드·JSON·캡처·채팅에 붙이지 않습니다. 키 상태는 앱에 설정 여부만 표시됩니다.

이 앱은 https://serverless.roboflow.com의 단일 모델 추론을 사용합니다. 현재 계정의 모델·호스팅 옵션이 다르면 Deploy의 연결 방식을 확인해야 합니다. 실제 사용자 모델의 연결 성공은 아직 확인하지 않았습니다.

## 영상 업로드 테스트

1. MP4·MOV·AVI 파일을 업로드합니다. 최대 200MB이며 source.mp4는 로컬에서 직접 선택합니다. YouTube 주소는 강의 시청용입니다.
2. 시작 0초·길이 10초·2fps로 시작합니다. 영상 끝을 넘는 구간은 실제 끝까지만 추출합니다.
3. 한 번에 최대 20초·60프레임, 긴 변 960px입니다. 처리할 구간을 바꿔 여러 장면을 확인합니다.
4. 실제 모드는 프레임마다 같은 모델에 요청합니다. 10초·2fps는 최대 20개 프레임 요청입니다.
5. 프레임 선택으로 원본 시각·박스·line 경계를 확인하고, **결과 영상 만들기**로 MP4를 재생·저장합니다.
6. MP4는 추출 프레임을 선택 fps로 이어 붙인 무음 H.264 확인 영상입니다. 원본의 모든 프레임을 분석하거나 추적하지 않으며 프레임이 드문 입력은 재생 길이가 짧아질 수 있습니다.
7. 결과 PNG·JSON도 저장할 수 있습니다. 업로드 확인 모드는 NO MODEL 표시와 미추론 출처를 남깁니다.

원본 코덱에 따라 브라우저 미리보기가 안 보일 수 있습니다. MP4(H.264)로 변환해 확인하세요. 디코딩할 수 없는 파일은 오류로 안내합니다.

## 이미지 예제와 공통 결과

- 실제 모드의 보조 입력 **이미지 한 장**에서는 JPG·PNG·WebP 한 장, 최대 10MB·1,600만 화소입니다.
- EXIF 방향을 보정하고 흰 배경의 RGB 이미지로 바꾼 뒤 긴 변을 최대 1,600px로 줄입니다.
- 처리한 이미지의 좌표에 맞춰 결과를 그립니다. 일반 객체의 x/y는 박스 중심이며, line의 points는 폴리곤 꼭짓점입니다.
- API에는 confidence 0.05 이상을 요청합니다. 화면 임계값은 받은 결과를 다시 거릅니다. 서버에서 누락된 예측을 화면 설정만으로 복구할 수는 없습니다.
- line에 유효한 폴리곤이 없으면 안내하고 그 영역을 제외합니다. 박스를 도로 마스크로 대신 채우지 않습니다.
- 결과 PNG와 JSON을 내려받을 수 있습니다. 예제 PNG에는 DEMO 표시, JSON에는 hand-written demo 출처가 들어갑니다.
- JSON은 화면 필터 전 전체 결과와 선택 조건을 담습니다. API 키는 포함하지 않습니다.

## 다시 실행과 API 호출

버튼을 누를 때만 새 API 요청을 합니다. 결과는 사용자 세션에 두므로 임계값·색 투명도·표시 클래스·확인 프레임 변경은 다시 추론하지 않습니다.
영상/이미지·분석 구간·fps·모드·모델 ID·키가 바뀌면 이전 결과를 지웁니다. 표시 조건을 바꾸면 이전 MP4를 지우며 새 조건으로 다시 만들 수 있습니다. API 분석은 반복하지 않습니다. 중간 프레임 요청이 실패하면 부분 결과를 성공으로 저장하지 않습니다. 브라우저 새로고침으로 세션이 종료되면 결과도 사라질 수 있습니다.
업로드 파일을 앱에서 디스크에 저장하지 않습니다. 실제 모드의 요청은 Roboflow 사용량을 발생시킬 수 있습니다.

## 9개 클래스

| 이름 | 의미 |
| --- | --- |
| car | 자동차 |
| motor | 오토바이 |
| people | 사람 |
| sign | 표지판 |
| lampg | 초록 신호등 |
| lampr | 빨간 신호등 |
| lampy | 노란 신호등 |
| lamp | 색을 구분하기 어려운 신호등 |
| line | 차선 사이의 주행 가능한 도로 영역 |

## 막혔을 때

| 상황 | 확인 |
| --- | --- |
| py를 찾을 수 없음 / 선택한 버전이 없음 | 64비트 Python 3.11 또는 3.12 설치·선택과 터미널 경로 |
| API 키 없음 | 실행 폴더의 .streamlit/secrets.toml과 앱 재시작 |
| 요청 실패 | 키 권한, 모델 ID, Serverless 지원 여부, 네트워크 |
| 표시 결과 0개 | 실제 응답, 임계값, 선택 클래스 |
| line 폴리곤 없음 | 분할 모델인지와 응답 points |
| 새 이미지에 이전 결과가 보임 | 이미지 변경 후 결과가 초기화되는지 확인 |

## 파일과 확인

app.py·video_ui.py는 화면·세션 상태, video.py는 프레임 추출·MP4 생성, core.py는 입력 처리·API·그리기, demo.py는 가상 예제입니다.
requirements.txt는 검사에 사용한 Streamlit 1.66.0, inference-sdk 1.8.0, Pillow 12.3.0, PyAV 18.1.0을 지정합니다.
3차시에서 영상 업로드 테스트까지 진행하고, 4차시에서는 배포와 다른 환경에서의 점검을 다룹니다.

공식 자료:
- [Roboflow Inference](https://inference.roboflow.com/quickstart/roboflow_ecosystem/)
- [Roboflow 응답 형식](https://github.com/roboflow/computer-vision-skills/blob/main/skills/roboflow-api-reference/inference.md)
- [Streamlit 비밀 설정](https://docs.streamlit.io/develop/concepts/connections/secrets-management)
- [Streamlit 세션 상태](https://docs.streamlit.io/develop/api-reference/caching-and-state/st.session_state)

- [Streamlit 영상 표시와 H.264](https://docs.streamlit.io/develop/api-reference/media/st.video)
- [PyAV 영상 처리](https://pyav.basswood.io/docs/stable/cookbook/basics.html)
- [PyAV 18.1.0의 Python 3.11 지원](https://pypi.org/project/av/18.1.0/)
