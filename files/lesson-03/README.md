# 3차시 실습 - 도로 이미지 분석 앱

50분 수업용 Streamlit 앱입니다. 모델 하나의 결과에서 일반 객체는 박스, line은 반투명 도로 영역으로 표시합니다.

현재 어노테이션 중이어도 **예제 결과로 연습** 모드에서 시작할 수 있습니다. 가상 도로와 손으로 작성한 결과를 사용하며 실제 모델의 예측·정확도가 아닙니다. 예제 모드에서는 API를 호출하지 않습니다.

## 실행 준비

Python 3.12와 인터넷 연결이 필요합니다. ZIP을 풀었다면 이 README와 app.py가 있는 폴더에서 터미널을 엽니다. 저장소를 복제했다면 먼저 다음 폴더로 이동합니다.

~~~powershell
cd files/lesson-03
~~~

Windows PowerShell에서 다음 명령을 순서대로 실행합니다. 설치는 수업 전에 마치는 것이 좋습니다.

~~~powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
~~~

브라우저에서 터미널에 표시된 Local URL을 엽니다. 종료는 터미널에서 Ctrl+C입니다.
기본 모드에서 **예제 결과 보기**를 누른 뒤 표시 임계값·도로 불투명도·클래스 선택을 바꿔 봅니다.
설치 명령 원문은 run-local.txt에도 있습니다. macOS/Linux에서는 가상환경 Python 경로가 .venv/bin/python입니다.

## 실제 모델 연결 - 학습이 끝난 뒤

1. 모델의 Deploy 안내에서 Instance Segmentation과 Serverless 지원 여부를 확인합니다. 모델 ID는 보통 프로젝트이름/버전번호 형식입니다.
2. .streamlit/secrets.toml.example을 같은 폴더의 secrets.toml로 복사합니다.
3. 복사한 파일에 실제 ROBOFLOW_API_KEY와 ROBOFLOW_MODEL_ID를 입력합니다. 이 파일은 Git과 배포 ZIP에 넣지 않습니다.
4. 앱을 다시 시작하고 **내 모델로 분석**을 선택합니다. 이미지 한 장을 올린 뒤 **분석 실행**을 누릅니다.

같은 이름의 환경 변수도 사용할 수 있으며 환경 변수가 먼저 적용됩니다. API 키를 코드·JSON·캡처·채팅에 붙이지 않습니다. 키 상태는 앱에 설정 여부만 표시됩니다.

이 앱은 https://serverless.roboflow.com의 단일 모델 추론을 사용합니다. 현재 계정의 모델·호스팅 옵션이 다르면 Deploy의 연결 방식을 확인해야 합니다. 실제 사용자 모델의 연결 성공은 아직 확인하지 않았습니다.

## 입력과 결과

- JPG·PNG·WebP 한 장, 최대 10MB·1,600만 화소입니다.
- EXIF 방향을 보정하고 흰 배경의 RGB 이미지로 바꾼 뒤 긴 변을 최대 1,600px로 줄입니다.
- 처리한 이미지의 좌표에 맞춰 결과를 그립니다. 일반 객체의 x/y는 박스 중심이며, line의 points는 폴리곤 꼭짓점입니다.
- API에는 confidence 0.05 이상을 요청합니다. 화면 임계값은 받은 결과를 다시 거릅니다. 서버에서 누락된 예측을 화면 설정만으로 복구할 수는 없습니다.
- line에 유효한 폴리곤이 없으면 안내하고 그 영역을 제외합니다. 박스를 도로 마스크로 대신 채우지 않습니다.
- 결과 PNG와 JSON을 내려받을 수 있습니다. 예제 PNG에는 DEMO 표시, JSON에는 hand-written demo 출처가 들어갑니다.
- JSON은 화면 필터 전 전체 결과와 선택 조건을 담습니다. API 키는 포함하지 않습니다.

## 다시 실행과 API 호출

버튼을 누를 때만 새 API 요청을 합니다. 결과는 사용자 세션에 두므로 임계값·색 투명도·표시 클래스 변경은 다시 추론하지 않습니다.
이미지·모드·모델 ID·키가 바뀌면 이전 결과를 지웁니다. 브라우저 새로고침으로 세션이 종료되면 결과도 사라질 수 있습니다.
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
| py를 찾을 수 없음 / 3.12가 없음 | Python 설치·선택 버전과 터미널 경로 |
| API 키 없음 | 실행 폴더의 .streamlit/secrets.toml과 앱 재시작 |
| 요청 실패 | 키 권한, 모델 ID, Serverless 지원 여부, 네트워크 |
| 표시 결과 0개 | 실제 응답, 임계값, 선택 클래스 |
| line 폴리곤 없음 | 분할 모델인지와 응답 points |
| 새 이미지에 이전 결과가 보임 | 이미지 변경 후 결과가 초기화되는지 확인 |

## 파일과 확인

app.py는 화면·세션 상태, core.py는 입력 처리·API·그리기, demo.py는 가상 예제입니다.
requirements.txt는 검사에 사용한 Streamlit 1.66.0, inference-sdk 1.8.0, Pillow 12.3.0을 지정합니다.
이 앱은 이미지 한 장을 분석합니다. 영상 프레임 처리·공개 배포는 4차시에서 다룹니다.

공식 자료:
- [Roboflow Inference](https://inference.roboflow.com/quickstart/roboflow_ecosystem/)
- [Roboflow 응답 형식](https://github.com/roboflow/computer-vision-skills/blob/main/skills/roboflow-api-reference/inference.md)
- [Streamlit 비밀 설정](https://docs.streamlit.io/develop/concepts/connections/secrets-management)
- [Streamlit 세션 상태](https://docs.streamlit.io/develop/api-reference/caching-and-state/st.session_state)
