# 어노테이션·학습 결과 캡처 확인

확인일: 2026-10-18. 원본: captures/lesson-03/1.png~12.png. 12장 모두 시각 확인했습니다.

**201장 어노테이션과 v1 모델 학습 완료가 화면으로 확인됩니다. 학습된 모델은 RF-DETR Object Detection (Small)입니다.** 이 모델은 객체 박스를 출력합니다. 목표인 단일 모델의 line 도로 마스크를 위해서는 Instance Segmentation 구성이 필요합니다. 현재 모델의 탐지 평가와 앞으로 만들 분할 모델의 평가는 구분합니다.

## 캡처에서 확인한 사실

| 원본 | 화면 | 확인한 내용 |
| --- | --- | --- |
| 1.png | Annotate | Annotated 201 / Unannotated 0, Object Detection. Dataset 배지 0은 촬영 당시 상태 |
| 2.png | Dataset 추가 | 원본 201장, Train 141 / Valid 40 / Test 20, 70/20/10 선택 |
| 3.png | Preprocessing | Auto-Orient, Resize Stretch 512×512 선택 |
| 4.png | Augmentation | 증강 추가 전 중간 화면 |
| 5.png | Augmentation | Hue ±15°, Noise 최대 0.1%, Bounding Box: Brightness ±15% 선택. 경고 상세는 보이지 않음 |
| 6.png | Create | 483 images (3x) 선택. 원본 이미지 수와 증강 후 수를 구분 |
| 7.png | Dataset Analytics | 201장, 정답 2,972개, 평균 14.8개/장, 정답 누락 이미지 0, null example 0, 사용 클래스 9개 |
| 8.png | Classes & Tags | 등록 이름 11개 중 정답이 있는 클래스는 9개. aicar·carcar는 각각 0개 |
| 9.png | Train a Model | 저장된 v1: 483장, 88%/8%/4%, 9개 클래스, 전처리 2개·증강 3개. 다음 저장 이름 v2는 새 학습 완료의 증거가 아님 |
| 10.png | Models | v1의 aicar-aae4t-1-rfdetr-small-t1, Roboflow RF-DETR Object Detection (Small), Test 지표 확인 |
| 11.png | Model Evaluation | Test 20장, mAP@50 47.3%, Precision 53.0%, Recall 41.2%, F1 45.9%, 표시된 최적 confidence 37% |
| 12.png | 클래스별 성능 | confidence 37%의 정답·성공·혼동·누락·오탐 그래프. car의 Correct Predictions 120개 툴팁 확인 |

v1의 483장은 141×3+40+20과 일치합니다. 423/40/20의 비율을 반올림하면 88%/8%/4%이므로 증강 후 비율로 해석할 수 있습니다. 이는 화면 수치에 근거한 계산이며 서로 다른 원본 483장을 뜻하지 않습니다. v1의 정확한 전처리·증강 매개변수가 앞선 선택 화면과 모두 같은지는 버전 상세로 확인해야 합니다.

## 클래스별 정답 수

아래 수치는 **이미지 수가 아닌 어노테이션 인스턴스 수**입니다.

| 클래스 | 의미 | 정답 수 |
| --- | --- | ---: |
| car | 자동차 | 1,532 |
| line | 차선 사이의 주행 가능 도로 영역 | 841 |
| people | 사람 | 179 |
| sign | 표지판 | 153 |
| lampg | 초록 신호등 | 151 |
| lampr | 빨간 신호등 | 51 |
| lamp | 색을 구분하기 어려운 신호등 | 32 |
| motor | 오토바이 | 29 |
| lampy | 노란 신호등 | 4 |
| 합계 | 사용 클래스 9개 | 2,972 |

- lampy는 전체 4개뿐이므로 다양한 장면의 예시 보강이 우선입니다. 분리 막대는 Train에만 있는 것으로 보이지만, Valid/Test의 정확한 개수는 분리별 숫자로 확인해야 합니다. 없는 평가 예시의 성능을 추정하지 않습니다.
- aicar·carcar는 정답이 없는 추가 이름입니다. 사용 계획이 없다면 정리할 후보이며 원격 프로젝트에서 삭제하지 않았습니다. 앱의 클래스 목록은 사용자가 정한 9개를 유지합니다.
- car·line의 정답이 많은 편입니다. 전체 점수와 함께 희소 클래스의 누락·오탐을 확인합니다. 12번의 다른 막대 높이로 정확한 개수를 추정하지 않습니다.

## 평가 값의 해석

- Test 20장 기준 **박스 탐지 평가**입니다. mAP@50 47.3%를 마스크 성능이나 전체 정확도 47.3%로 부르지 않습니다. 실제 도로 마스크 예측 화면은 아직 없습니다.
- 37%는 이 평가 화면에 표시된 confidence입니다. 모든 영상에 최적인 배포값으로 고정하지 않습니다. 운영 임계값은 Valid에서 비교하고, Test 점수에 맞춰 반복 조정하지 않습니다.
- 4.7ms는 화면의 Serverless Cloud API 서버 처리 시간 중앙값(20회 요청)입니다. 네트워크 시간이 제외되어 앱의 업로드·추론·표시 속도나 실시간 처리 보장이 아닙니다.
- 10번 그래프는 mAP@50:95를 선택했지만 정확한 숫자 툴팁은 없습니다. 확인된 mAP@50과 혼동하거나 값을 추정해 기록하지 않습니다.
- Model URL과 모델 표시 이름은 확인했지만, 앱에 넣을 API model_id와 요청 방식은 Deploy Model 코드로 확인해야 합니다. 표시 이름에서 프로젝트/버전을 조합해 입력하지 않습니다.

## 다음 작업: 기존 정답을 보존하며 분할 모델 준비

1. 현재 프로젝트와 v1 모델을 보존합니다. Roboflow 프로젝트 목록의 ⋯ → **Duplicate Project → Instance Segmentation**으로 복제를 준비합니다. 메뉴 위치가 다르면 같은 이름의 복제 기능을 찾습니다.
2. 복제된 프로젝트에서 대표 이미지를 다시 엽니다. 특히 line의 도로 폴리곤이 유지되는지, 객체 정답이 분할 학습에 허용되는 형식인지, 9개 클래스와 이미지 수·분리가 유지되는지 확인합니다. 박스가 사각형 마스크로 변환되더라도 실제 객체 윤곽 마스크와는 다릅니다. 이 수업은 일반 객체를 박스로 표시하므로 필요한 정답 보완 범위를 먼저 판단합니다.
3. 확인한 데이터로 Instance Segmentation 모델을 학습합니다. 신호등 색 라벨을 보존하도록 다음 비교 버전에서는 Hue 제외를 권합니다. lampy 예시, 작은 신호등·표지판, Stretch 512×512의 형태 변화도 검토합니다. 모든 이미지의 재라벨링이나 기존 모델 삭제부터 시작할 필요는 없습니다.
4. 학습 후 실제 예측의 line 마스크와 Deploy Model의 요청 코드를 확인하고 Streamlit에 연결합니다. 학습에 쓰지 않은 블랙박스 영상의 10초·2fps 구간부터 객체 박스·도로 영역·신호등 색 혼동을 확인합니다.

프로젝트 복제 절차는 [Roboflow 담당자의 공식 지원 답변](https://discuss.roboflow.com/t/roboflow-missing-yolov8-instance-segmentation-weight-pt-segmentation-version-to-download-how-to-train-and-deploy-with-segmentation-masks/8942)을 참고했습니다. 탐지와 별도의 분할 모델은 [RF-DETR Segmentation 문서](https://rfdetr.roboflow.com/latest/learn/run/segmentation/)에서 확인했습니다. 폴리곤을 정답으로 그렸어도 탐지 모델은 박스를 출력할 수 있습니다. [Roboflow 설명](https://blog.roboflow.com/polygons-object-detection/)

Hue 제외는 신호등 색을 정답으로 쓰는 이 프로젝트에 대한 제안입니다. 현재 모델이 색상 증강 때문에 실패했다고 단정하지 않습니다. [Roboflow 증강 안내](https://roboflow.com/blog/object-detection-augmentation)

## 추가 캡처가 필요한 시점

학습 완료·평가 화면은 이미 받았습니다. 같은 화면을 다시 찍을 필요는 없습니다.

| 시점 | 권장 파일명 | 확인할 내용 |
| --- | --- | --- |
| 복제 후 가장 먼저 | 13-segmentation-project.png | 프로젝트 유형 Instance Segmentation, 대표 이미지의 line 폴리곤 유지 |
| 분할 모델 학습 후 | 14-segmentation-prediction.png | 학습된 모델의 실제 예측과 line 도로 마스크. 정답 편집 화면과 구분 |
| API 연결 직전 | 15-model-deploy.png | Deploy Model의 요청 코드, model_id·엔드포인트·지원 방식. API 키 제외 |

원본은 기존 captures/lesson-03/ 폴더에 저장하면 됩니다. 기존 탐지 모델을 먼저 연결해 시험하려는 경우에도 Deploy Model의 실제 코드가 필요하며 line 마스크는 출력되지 않습니다.

## 강의 반영과 보존

- 2·3·5·6번 설정 화면에 이어 7·8·11·12번 데이터·평가 화면을 원본 바이트 그대로 assets/img/lesson-02/에 복사했습니다. 2차시의 읽기 화면 캡처 안내에 총 8장을 배치했습니다.
- 1번(계정 정보), 9번(계정 식별 정보), 10번(사용량·결제 관련 영역)은 공개 이미지로 복사하지 않았습니다. 필요한 학습 사실만 글로 반영했습니다. 4번은 설정 중간 상태로 기록합니다.
- 원본 12장과 기존 작업은 보존합니다. Roboflow 프로젝트 복제·추가 학습·API 호출·커밋·푸시는 수행하지 않았습니다.
