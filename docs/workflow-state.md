# 작업 상태

## 사용자 결정과 이번 범위

- 강의: 자율주행 자동차 모델 만들기(by Object Detection), 50분 × 4차시.
- 모델 하나로 9개 클래스를 인식하고 Roboflow API·Streamlit으로 배포하는 계획.
- 라벨: car, motor, people, sign, lampg, lampr, lampy, lamp, line.
- lampg/lampr/lampy는 초록/빨강/노랑, lamp는 색 구분이 어려운 신호등. sign은 표지판.
- line은 차선 사이의 주행 가능한 도로 영역. 원본은 source.mp4.
- 2026-10-17: 1차시 제작 요청에 따라 기존 1차시·캡처·YouTube 연결을 작성.
- 2026-10-17: 사용자 “이제 다음 작업하자”에 따라 다음 순서인 2차시를 제작. 이어 “아직 어노테이션 하고 있어”라고 현재 상태를 확인했으므로 학습 완료를 전제하지 않음.

이번 범위는 2차시 초안, 차시 간 이동, 활동지·교사용 안내와 검사입니다. 승인된 4차시 구성에 맞춰 루트는 강의 목록, 1차시와 2차시는 하위 페이지로 구성했습니다. 3·4차시는 준비 중입니다. WORKFLOW의 특정 단계 번호 실행 요청은 아닙니다.

## 산출물

- index.html: 4차시 목록. 1·2차시 링크, 3·4차시 준비 중.
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

- Q01: 기존 캡처는 Object Detection. 목표인 마스크 출력을 위한 Instance Segmentation 프로젝트·학습 구성 확인.
- Q02: 일반 객체의 저장 정답 형식·분할 학습 호환성. car 캡처에는 박스가 보이며 모든 저장 형식은 아직 확인하지 못함.
- Q03: sign의 포함 범위·지지대, line의 차로·차량/장애물·가림 처리 기준.
- Q04: 어노테이션 진행 중. 이미지 재열기·검수·Dataset 반영·분리·버전·학습 결과는 완료로 간주하지 않음.
- Q05: 연결된 브라우저 없음. 실제 발표 모드·모바일·테마·입력·YouTube 재생 검증 미실행.
- Q06: 실제 계정의 모델·메뉴·학습 상태·평가 값과 2차시 캡처 미확인.

## 다음 실행 조건

어노테이션을 계속하면서 프로젝트 유형과 경계 기준을 확인합니다. 검수 후 장면 단위 분리·데이터 버전 생성·단일 분할 모델 학습을 진행하고 단계별 캡처를 반영합니다. 사용 가능한 모델과 line 마스크 출력을 확인하면 3차시의 API 연결을 구체화할 수 있습니다.

Roboflow 데이터 이동·프로젝트 변경·학습·커밋·푸시·외부 배포는 수행하지 않았습니다. 보호 파일·원본은 수정하지 않았으며 해시 검사 결과는 2차시 검증 기록에 남깁니다.
