# 작업 상태

## 사용자 결정

- 강의 제목: 자율주행 자동차 모델 만들기(by Object Detection).
- 현재 라벨: car, lampg, lampr, lampy, lamp, line, motor, people, sign. sign은 표지판으로 사용자 확인.
- 신호등 라벨 확정: lampg는 초록, lampr는 빨강, lampy는 노랑, lamp는 신호등이지만 색을 구분하기 어려운 경우. line은 차선 사이 주행 가능 도로 영역.
- **모델 하나**로 인식하고 Roboflow API와 Streamlit으로 배포하는 계획.
- 원본 영상: source.mp4. 사용자가 어노테이션 작업 진행 중이라고 알림.
- 총 수업 시간: **50분 × 4차시 = 200분**.
- 2026-10-17: 사용자 “좋아! … 이미지 캡쳐 해야하는 부분, 확인해야 하는 부분은 꼭 얘기해줘. … 1차시부터 작업을 시작해볼까?”에 따라 승인된 계획 중 1차시 제작.
- 같은 작업 중 사용자 “차선 사이의 주행 가능한 도로 영역”이라고 마스크 대상을 확정.

## 현재 범위

1차시 웹 강의 초안을 작성했습니다. 캡처 6장 확인·4장 반영을 마쳤으며, 모델 유형과 목표의 불일치 해결·라벨 기준 확인·브라우저 화면 검증이 남아 있습니다.
요청은 WORKFLOW.md의 특정 N단계 호출이 아니라 승인된 수업 계획의 1차시 제작입니다.
이번 작업에서는 사용자 승인 범위에 필요한 본문·스타일·메타·교사용 기록을 작성하고 공통 파일 보호 규칙을 지켰습니다.
2~4차시 콘텐츠나 배포 작업은 진행하지 않았습니다.

## 산출물

- index.html: 5개 섹션·21개 발표 조각.
- assets/css/lecture.css: 1차시 레이아웃·반응형·개념 도식.
- data/site.js: 강의 메타 변경, instructor 데이터 유지.
- docs/lesson-01-capture-guide.md: 캡처 6장 확인 결과·실제 9개 라벨·남은 확인 항목.
- docs/lesson-01-teacher-guide.md: 50분 진행안.
- docs/section-plan.md, slide-map.md: 구조·시간·발표 순서.
- docs/lesson-01-verification.md 및 JSON 결과: 수행 검사와 한계.
- docs/protected-baseline.json: 최초 보호 파일·영상 해시.
- .gitignore: 원본 자료·캡처·검증 임시 파일 제외.

## 완료한 섹션 초안

road-mission / vision-concepts / annotation-ready / annotation-practice / annotation-review

## 미해결 항목

- Q01: 캡처로 Object Detection 유형 확인. 마스크 출력을 위해 Instance Segmentation 학습에 기존 정답을 사용할 수 있는지 점검 필요. 9개 클래스와 lamp 의미 구분은 사용자 설명으로 확정.
- Q02: 일반 객체의 저장된 정답 형식 및 단일 분할 학습 호환성 확인. car 화면에는 박스가 보임.
- Q03: 주행 가능 영역의 차로 범위·장애물·가림 처리 기준.
- Q04: 캡처 6장 수신·4장 반영 완료. 나머지 목록 2장은 계정 정보로 원본 보관. 개별 이미지 재열기·검수 완료는 별도 확인 필요.
- Q05: 연결된 브라우저가 없어 시각·실제 입력·YouTube 영상 재생 검증 미실행.

다음 작업은 분할 학습용 프로젝트 준비 → 기존 라벨 보존 확인 → 표지판·도로 경계 기준 확정 → 1차시 화면 검증 → 2차시 학습 준비입니다.
실행 순서와 프로젝트 유형·9개 클래스 목록 캡처 안내는 lesson-01-capture-guide.md에 기록했습니다. 표지판은 도로 도식과 실습 경계 확인 항목에도 반영했습니다.
Roboflow 데이터 이동·프로젝트 전환·학습·외부 배포는 수행하지 않았습니다.
보호 파일 기준은 protected-baseline.json을 보존합니다. 검증 서버는 종료했고 임시 브라우저 프로필은 정리했습니다.

SOURCE VIDEO에는 사용자 지정 YouTube 영상(ihokShSN51Y)을 임베드하고 새 탭 링크를 추가했습니다. 영상 관찰과 프레임 설명을 두 발표 조각으로 나눴으며 50분 수업 배분은 유지합니다.
