# 3차시 캡처·확인 안내

**201장 어노테이션·탐지 모델 v1 학습·평가를 확인했습니다.** 받은 1.png~12.png는 모두 검토했고, [확인 내용](training-capture-review.md)에 정리했습니다. 현재 모델은 RF-DETR Object Detection (Small)이며 line 도로 마스크용 분할 모델이 필요합니다. 학습·평가 화면을 다시 찍을 필요는 없습니다.

가장 먼저 필요한 화면은 **Instance Segmentation으로 복제한 프로젝트 유형과 대표 이미지의 line 폴리곤**입니다. 13-segmentation-project.png로 저장합니다. 분할 학습 후에는 14-segmentation-prediction.png, 연결 직전에는 15-model-deploy.png로 실제 예측과 Deploy 요청 코드를 기록합니다. API 키는 제외합니다. 모델 표시 이름·URL만으로 앱의 API model_id를 정하지 않습니다.

아래 표는 별도의 앱 실행 화면 참고 목록입니다. 원본은 captures/lesson-03/에 저장합니다.

| 시점 | 파일명 | 필요한 정보 |
| --- | --- | --- |
| 지금: 영상 업로드 후 | 01-video-upload.png | 업로드 확인 모드·source.mp4·원본 길이·시작 0초·10초·2fps |
| 지금: 프레임 추출 후 | 02-video-frames.png | 추출 프레임·원본 시각·NO MODEL 표시 |
| 지금: 결과 영상 생성 후 | 03-video-playback.png | MP4 재생 화면과 다운로드 버튼 |
| 예제 표시 비교 시 | 04-demo-040.png / 04-demo-090.png | 같은 가상 이미지·전체 클래스·임계값과 DEMO 표시 |
| 분할 모델 학습 후 | 15-model-deploy.png | Deploy의 실제 model_id·요청 코드·Serverless 지원 여부. API 키 제외 |
| 실제 영상 분석 후 | 06-video-result.png | 같은 프레임의 객체 박스·line 마스크·원본 시각·모델 ID |

## 꼭 확인할 항목

- [ ] source.mp4 업로드 후 0~10초·2fps에서 20프레임이 추출된다.
- [ ] 업로드 확인 모드는 API 키 없이 동작하고 검출 결과를 만들지 않는다.
- [ ] MP4가 재생되고 다운로드한 파일도 열린다. 선택 fps의 무음 확인 영상이다.
- [ ] 임계값·불투명도·클래스·프레임 선택 변경은 API를 다시 호출하지 않는다.
- [ ] 표시 변경 후 MP4를 다시 만들면 새 조건이 적용된다.
- [ ] 파일·구간·fps·모델·모드 변경 시 이전 결과가 지워진다.
- [ ] 실제 모델에서는 객체는 박스, line은 차선 사이 주행 가능 영역의 폴리곤으로 표시된다.
- [ ] 학습에 쓰지 않은 영상 또는 별도로 남겨 둔 장면으로 인식 성능을 확인한다.
- [ ] 강의의 ZIP·PDF 다운로드와 발표 모드 18개 조각을 실제 브라우저에서 확인한다.

source.mp4의 학습에 사용한 장면을 다시 보는 것은 앱 동작 점검입니다. 그 결과만으로 새 영상에 대한 성능을 판단하지 않습니다.
API 키와 계정 이메일은 캡처하지 않습니다. 실제 secrets.toml 대신 secrets.toml.example만 공유합니다.
