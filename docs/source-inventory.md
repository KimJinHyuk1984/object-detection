# 자료 목록

| 자료 ID | 위치 | 유형 | 크기·수량 | 확인 범위 | 본문 사용 |
| --- | --- | --- | --- | --- | --- |
| source-001 | source.mp4 | MP4 영상 | 158,322,490바이트 | MP4 메타데이터: 약 301.49초, 1920×1080, 30fps, 영상 9,043프레임. SHA-256은 protected-baseline.json에 기록. 전체 장면 검토·개인정보 전수 검사는 미실행. | 메타데이터만 인용. 원본 영상 링크·복사·업로드 없음. |
| source-002 | img_data/ | 교재 사진 | JPG 17장 | 기존 직캠 교재 사진. 이번 차시 재사용·변환·OCR 없음. 새 내용의 출처로 사용하지 않음. | 사용 안 함 |
| source-003 | Roboflow 공식 Annotate an Image 문서 | 웹 문서 | 1개 | 2026-10-17 확인: 박스·폴리곤·마스크 도구, 다각형 닫기, 라벨 선택·검수 | 일반적인 도구 설명과 출처 링크 |
| source-004 | captures/lesson-01/ | 사용자 제공 캡처 | PNG 6장 | 6장 시각 확인. 프로젝트 Object Detection, car 박스, line 폴리곤, 작업 목록. 원본 메타·해시는 lesson-01-capture-checks.json 참조. | 앞 4장 원본과 동일한 PNG 복사. 계정 정보가 있는 04.png·04(1).png는 비공개 원본 보관. |
| source-005 | Roboflow 공식 Polygons for Object Detection 설명 | 웹 문서 | 1개 | 2026-10-17 확인: 폴리곤 어노테이션을 사용해도 탐지 모델은 박스를 출력함. | 모델 유형 확인 안내·출처 링크 |

원본 자료는 이동·삭제·수정하지 않았습니다. source.mp4는 작업 전후 해시가 같습니다.
원본 영상·사진·캡처는 .gitignore에서 제외하고, git ls-files로 현재 미추적 상태를 확인했습니다.
캡처 4장의 공개용 복사본을 assets/img/lesson-01/에 만들었습니다. PNG 글자·경계를 보존하기 위해 파일 형식을 유지했으며 원본과 SHA-256이 같습니다. 실습 코드 파일은 없습니다.
공식 문서: https://docs.roboflow.com/annotate/use-roboflow-annotate

폴리곤과 탐지 출력 근거: https://blog.roboflow.com/polygons-object-detection/
