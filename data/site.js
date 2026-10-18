/* ★ 공통 관리 파일: instructor는 템플릿 원본에서만 수정해 모든 강의에 반영합니다.
 * site, levels와 otherLectures는 각 강의 저장소에서 수정합니다.
 * 동기화 스크립트는 이 파일을 덮어쓰지 않습니다. instructor 변경은 수동으로 병합합니다.
 */
window.SITE = {
  site: {
    title: "자율주행 자동차 모델 만들기",
    subtitle: "Roboflow와 Python 웹앱으로 완성하는 4차시 프로젝트",
    repo: "object-detection" // 진행 기록을 구분하는 이름. 복제한 저장소 이름으로 변경합니다.
  },
  // ── 이 아래 instructor 블록은 모든 강의 저장소에서 동일하게 유지한다 ──
  instructor: {
    name: "김진혁",
    affiliation: "동양고등학교 · 수학, 정보",
    email: "kimjh0630@naver.com",
    photo: "assets/img/instructor.jpg",
    credentials: [
      "동양고등학교 교사(수학, 정보)",
      "성균관대학교 일반대학원 수학교육전공 박사 수료",
      "서울시교육청 초중등 AI교육 연구회 부회장",
      "(2022개정 교육과정) 『데이터 과학』 교과서 집필진(올드앤뉴)",
      "(2022개정 교육과정) 『논리와 사고』 교과서 집필진(세종)",
      "AIEDAP마스터 교원(서울, 경기, 인천, 제주 권역)",
      "서울시교육청 AI융합교육 선도교사(2023~)",
      "2026학년도 서울시교육청 AI중점학교 지원단",
      "『인공지능 진로진학 교육자료』 집필진(서울시교육청, 2022)",
      "『면접보고 대학가자』 집필진(올드앤뉴, 2023)"
    ]
  },

  // ── 이 아래는 강의마다 교체한다 ──
  // 원소가 1개이면 루트가 강의 페이지, 2개 이상이면 루트가 허브입니다.
  // 단일 강의의 badge는 비워 둡니다. 번호가 필요 없으므로 표시하지 않습니다.
  // 단일 강의의 slug는 폴더/URL 선택에는 무시하지만 진행 기록의 고정 ID로 사용합니다.
  // 다중 강의에서는 slug와 하위 폴더명, 하위 HTML의 body[data-level]을 일치시킵니다.
  levels: [
    {
      "slug": "road-perception",
      "badge": "1차시",
      "title": "AI에게 도로를 가르치기",
      "subtitle": "자율주행 자동차 모델 만들기 · 객체와 주행 가능 영역의 정답 표시",
      "kicker": "LESSON 01 / ROAD PERCEPTION",
      "duration": "50분",
      "target": "",
      "difficulty": "입문",
      "tags": [
        "Roboflow",
        "Instance Segmentation",
        "Python 웹앱"
      ],
      "accent": "neon-green",
      "emoji": "",
      "cover": "",
      "status": "ready"
    },
    {
      "slug": "model-training",
      "badge": "2차시",
      "title": "모델을 학습하고 평가하기",
      "subtitle": "자율주행 자동차 모델 만들기 · 데이터 분리부터 오류 분석까지",
      "kicker": "LESSON 02 / TRAIN & EVALUATE",
      "duration": "50분",
      "target": "",
      "difficulty": "입문",
      "tags": [
        "Roboflow",
        "Instance Segmentation",
        "모델 평가"
      ],
      "accent": "violet",
      "emoji": "",
      "cover": "",
      "status": "ready"
    },
    {
      "slug": "api-app",
      "badge": "3차시",
      "title": "API로 영상 테스트 앱 만들기",
      "subtitle": "주행영상을 업로드하고 프레임별 예측 확인하기",
      "kicker": "LESSON 03 / API & APP",
      "duration": "50분",
      "target": "",
      "difficulty": "입문",
      "tags": [
        "Roboflow API",
        "Python 웹앱"
      ],
      "accent": "amber",
      "emoji": "",
      "cover": "",
      "status": "ready"
    },
    {
      "slug": "video-app",
      "badge": "4차시",
      "title": "주행영상 앱 배포하기",
      "subtitle": "영상 업로드 앱의 배포와 실제 모델 결과 점검",
      "kicker": "LESSON 04 / VIDEO & DEPLOY",
      "duration": "50분",
      "target": "",
      "difficulty": "입문",
      "tags": [
        "영상",
        "Python 웹앱"
      ],
      "accent": "neon-green",
      "emoji": "",
      "cover": "",
      "status": "coming"
    }
  ],

  // 다른 강의로 이동하는 링크 (전부 외부 절대 주소)
  otherLectures: [
    {
      title: "딥러닝 CNN으로 포트홀을 찾아라",
      url: "https://kimjinhyuk1984.github.io/pothole/",
      emoji: ""
    }
  ]
};
