"""Build the four-page, print-ready Korean lesson 2 workbook.

Requires reportlab. Font paths may be overridden for another operating system.
The PDF in output/pdf is copied unchanged to files for the lecture download.
"""
from pathlib import Path
import argparse
import json
import shutil

from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument("--font-regular", default="C:/Windows/Fonts/malgun.ttf")
parser.add_argument("--font-bold", default="C:/Windows/Fonts/malgunbd.ttf")
args = parser.parse_args()
pdfmetrics.registerFont(TTFont("Korean", args.font_regular))
pdfmetrics.registerFont(TTFont("KoreanBold", args.font_bold))

OUT = ROOT / "output/pdf/lesson-02-workbook.pdf"
OUT.parent.mkdir(parents=True, exist_ok=True)
DEPLOY = ROOT / "files/lesson-02-workbook.pdf"
DEPLOY.parent.mkdir(parents=True, exist_ok=True)
W, H = A4
M = 44
CW = W - 2 * M
INK = colors.HexColor("#182B36")
TEAL = colors.HexColor("#17695F")
MUTED = colors.HexColor("#52636C")
LINE = colors.HexColor("#B9C8C8")
PALE = colors.HexColor("#EFF5F3")
LIGHT = colors.HexColor("#F6F8F8")
WHITE = colors.white

c = canvas.Canvas(str(OUT), pagesize=A4, pageCompression=1)
c.setTitle("2차시 활동지 - 모델을 학습하고 평가하기")
c.setAuthor("자율주행 자동차 모델 만들기")
c.setSubject("데이터 점검, 장면 단위 분리, 단일 분할 모델 학습과 평가")
c.setCreator("ReportLab")
c.setViewerPreference("PrintScaling", "None")
layout_checks = []
page_number = 0

def line(x1, y1, x2, y2, color=LINE, width=0.6):
    c.setStrokeColor(color)
    c.setLineWidth(width)
    c.line(x1, H-y1, x2, H-y2)

def rect(x, y, w, h, fill=None, stroke=None, radius=0):
    c.setFillColor(fill or WHITE)
    c.setStrokeColor(stroke or fill or WHITE)
    c.setLineWidth(0.6)
    if radius:
        c.roundRect(x, H-y-h, w, h, radius, fill=bool(fill), stroke=bool(stroke))
    else:
        c.rect(x, H-y-h, w, h, fill=bool(fill), stroke=bool(stroke))

def text(value, x, top, size=10, bold=False, color=INK, max_width=None):
    font = "KoreanBold" if bold else "Korean"
    tw = pdfmetrics.stringWidth(value, font, size)
    if max_width is not None:
        assert tw <= max_width + 0.2, (page_number, value, tw, max_width)
    c.setFillColor(color)
    c.setFont(font, size)
    c.drawString(x, H-top-size, value)
    layout_checks.append({"page": page_number, "text": value, "right": round(x+tw, 2), "bottom": round(top+size+3, 2)})

def para(value, x, y, width, height, size=10, leading=14, bold=False, color=INK):
    style = ParagraphStyle("body", fontName="KoreanBold" if bold else "Korean",
        fontSize=size, leading=leading, textColor=color, wordWrap="CJK",
        spaceBefore=0, spaceAfter=0)
    p = Paragraph(escape(value).replace("\n", "<br/>"), style)
    pw, ph = p.wrap(width, height)
    assert ph <= height + 0.1, (page_number, value, ph, height)
    p.drawOn(c, x, H-y-ph)
    layout_checks.append({"page": page_number, "text": value, "right": round(x+pw, 2), "bottom": round(y+ph, 2)})

def check(label, x, y, size=9.5):
    rect(x, y+2, 8, 8, stroke=MUTED)
    text(label, x+13, y-1, size=size)
    return x + 13 + pdfmetrics.stringWidth(label, "Korean", size) + 17

def checks(items, y, x=M, size=9.5):
    for item in items:
        x = check(item, x, y, size)
    assert x-17 <= W-M+0.2, (page_number, "checkbox row", x)

def field(label, x, y, width, height=36):
    text(label, x, y, size=9.5, bold=True, color=MUTED, max_width=width)
    line(x, y+height, x+width, y+height)

def fields(items, y, height=36, gap=20):
    total = sum(ratio for _, ratio in items)
    usable = CW-gap*(len(items)-1)
    x=M
    for label, ratio in items:
        width=usable*ratio/total
        field(label, x, y, width, height)
        x += width+gap

def answer(label, y, height=48, hint=None):
    text(label, M, y, size=10, bold=True, max_width=CW)
    if hint:
        text(hint, M, y+17, size=8.5, color=MUTED, max_width=CW)
    line(M, y+height, W-M, y+height)

def note(value, y, height=38):
    rect(M, y, CW, height, fill=PALE, radius=5)
    rect(M, y, 3, height, fill=TEAL)
    para(value, M+12, y+9, CW-24, height-15, size=8.6, leading=12, color=MUTED)

def section(num, title, y):
    rect(M, y, 26, 25, fill=TEAL, radius=5)
    text(f"{num:02}", M+6, y+5, size=10.5, bold=True, color=WHITE)
    text(title, M+37, y+2, size=14.5, bold=True, max_width=CW-37)

def header(number, title, subtitle):
    global page_number
    page_number=number
    text("자율주행 자동차 모델 만들기", M, 28, size=9.3, bold=True, color=TEAL)
    right="LESSON 02  /  WORKBOOK"
    tw=pdfmetrics.stringWidth(right, "Korean", 8)
    text(right, W-M-tw, 29, size=8, color=MUTED)
    text(title, M, 48, size=23, bold=True, max_width=CW)
    text(subtitle, M, 80, size=9.3, color=MUTED, max_width=CW)
    line(M, 101, W-M, 101, color=TEAL, width=1.2)

def footer(number, topic):
    line(M, 803, W-M, 803, color=LINE)
    text(f"2차시 · {topic}", M, 813, size=8.3, color=MUTED)
    text(f"{number} / 4", W-M-27, 812, size=9, bold=True, color=TEAL)
    c.showPage()

def table(headers, widths, rows, y, row_height=23, header_height=32, font_size=9):
    assert abs(sum(widths)-CW)<0.1
    rect(M, y, CW, header_height, fill=PALE)
    x=M
    for label, width in zip(headers, widths):
        para(label, x+8, y+7, width-16, header_height-9, size=8.4, leading=10.5, bold=True, color=TEAL)
        x+=width
    line(M,y,M+CW,y,color=TEAL,width=0.8)
    for i, row in enumerate(rows):
        top=y+header_height+i*row_height
        if i%2==0:
            rect(M,top,CW,row_height,fill=LIGHT)
        x=M
        for j,(value,width) in enumerate(zip(row,widths)):
            if value:
                para(value,x+8,top+6,width-16,row_height-8,size=font_size,leading=12,bold=(j==0))
            x+=width
        line(M,top+row_height,M+CW,top+row_height)
    bottom=y+header_height+len(rows)*row_height
    x=M
    for width in widths[:-1]:
        x+=width
        line(x,y+header_height,x,bottom,color=LINE,width=0.35)
    return bottom

# PAGE 1 ---------------------------------------------------------------
header(1, "모델을 학습하고 평가하기", "50분 활동지 · 데이터 확인부터 오류 분석까지, 실제로 확인한 내용을 기록하세요.")
fields([("이름 / 모둠", 1), ("날짜", 1)], 113, height=28)
checks(["어노테이션 중", "데이터 검수 완료", "학습 대기 / 진행", "학습 완료"], 156)
section(1, "데이터와 정답 확인", 183)
fields([("프로젝트 이름", 1.1), ("현재 프로젝트 작업 유형", 1)], 219, height=29)
text("Instance Segmentation 유형 확인", M, 262, size=9.5, bold=True)
checks(["확인", "아직"],262,x=M+210)
field("일반 객체의 정답 형식과 분할 학습 호환성", M, 285, CW, height=25)
table(
    ["클래스", "의미", "라벨이 있는\n이미지 수", "전체 객체 /\n라벨 수", "Train의\n라벨 수"],
    [52,126,110,110,CW-398],
    [
        ["car","자동차","","",""],
        ["motor","오토바이","","",""],
        ["people","사람","","",""],
        ["sign","표지판","","",""],
        ["lampg","초록 신호등","","",""],
        ["lampr","빨간 신호등","","",""],
        ["lampy","노란 신호등","","",""],
        ["lamp","색 구분 어려운 신호등","","",""],
        ["line","주행 가능 도로 영역","","",""],
    ],
    327, row_height=22, header_height=33, font_size=8.9
)
answer("sign: 어떤 표지판을 포함하며, 지지대는 어떻게 처리하나요?", 571, height=33)
answer("line: 차로 범위와 차량·장애물·가려진 도로는 어떻게 처리하나요?", 619, height=36)
fields([("검수한 전체 이미지 수 (장)",1),("Dataset에 반영한 이미지 수 (장)",1)],678,height=29)
note("line은 도색된 선이 아닌, 차선 사이의 주행 가능한 도로 영역입니다.\n이미지 수와 라벨 수는 다릅니다. 예시가 0개인 클래스도 확인하고, 미확인 값은 비워 둡니다.",731,height=42)
footer(1,"정답·클래스 점검")

# PAGE 2 ---------------------------------------------------------------
header(2, "장면을 나누어 평가하기", "가까운 프레임은 같은 묶음으로 두고, 처음 보는 장면을 남겨 둡니다.")
section(2, "장면 단위 데이터 분리 계획", 121)
card_gap=10
card_w=(CW-2*card_gap)/3
for i,(label,body) in enumerate([
    ("TRAIN · 학습","모델이 정답을 보며 배울 자료"),
    ("VALID · 검증","설정·임계값과 개선안을 비교할 자료"),
    ("TEST · 시험","설정을 확정한 뒤 최종 확인할 자료")
]):
    x=M+i*(card_w+card_gap)
    rect(x,158,card_w,54,fill=PALE,radius=5)
    text(label,x+10,166,size=9.2,bold=True,color=TEAL,max_width=card_w-20)
    para(body,x+10,183,card_w-20,24,size=8.5,leading=11)
text("우리 영상의 장면 묶음과 배정 이유를 적으세요. 각 묶음의 가까운 프레임은 함께 배정합니다.",M,226,size=8.7,color=MUTED,max_width=CW)
table(["묶음","영상 · 시간 구간 / 장면","이미지 수","Train / Valid\n/ Test","배정 이유 · 희소 클래스"],
      [42,151,63,90,CW-346],
      [[key,"","","",""] for key in "ABCD"],246,row_height=47,header_height=35)
fields([("Train (장)",1),("Valid (장)",1),("Test (장)",1)],484,height=29)
answer("거의 같은 인접 프레임이 서로 다른 분리에 있나요?",537,height=41)
answer("구간 경계에 있는 비슷한 프레임은 어떻게 처리할까요?",599,height=41)
answer("이 영상 하나만으로는 확인하기 어려운 도로·날씨·상황은 무엇인가요?",661,height=41)
note("70 / 20 / 10은 설명용 비율입니다. 실제 장면과 클래스 분포를 함께 확인합니다.\n원본을 먼저 나눈 뒤 학습 데이터에 증강을 적용합니다. Test는 최종 확인용으로 남깁니다.",735,height=43)
footer(2,"데이터 분리 계획")

# PAGE 3 ---------------------------------------------------------------
header(3, "버전과 결과를 기록하기", "준비 중인 항목은 비워 두고, 학습 상태와 결과를 구분해 기록하세요.")
section(3, "데이터 버전과 학습 기록",121)
field("데이터 버전 이름 / 번호",M,158,CW,height=25)
field("전처리 설정 (방향 · 크기 등)",M,200,CW,height=25)
field("증강 설정",M,242,CW,height=25)
text("첫 비교 기준 버전은 추가 증강 없이 준비합니다.",M,276,size=8.6,color=MUTED)
fields([("모델 종류",1.35),("입력 크기",1)],297,height=25)
field("학습 시작 가중치 / 제공 옵션",M,339,CW,height=25)
fields([("시작 시각",1),("실제 상태 (대기 · 진행 · 완료 등)",1.45)],381,height=25)
text("작은 신호등·표지판과 line 정답 미리보기",M,424,size=9.3,bold=True)
checks(["확인","아직"],424,x=M+285)
text("마스크 출력",M,450,size=9.3,bold=True)
checks(["확인","아직"],450,x=M+100)
field("마스크 출력을 확인한 이미지",M,477,CW,height=25)
section(4, "지표 읽기",530)
text("평가 데이터",M,568,size=9.5,bold=True)
checks(["Valid","Test","확인 필요"],568,x=M+100)
text("위치 기준",M,594,size=9.5,bold=True)
checks(["Box","Mask","확인 필요"],594,x=M+100)
fields([("지표의 정확한 이름",1.5),("실제 확인한 값",1)],625,height=25)
fields([("IoU 기준 (예: @50 또는 @50:95)",1.25),("예측 표시 confidence 임계값",1)],671,height=25)
note("실제 화면에서 확인한 값만 기록합니다. 학습 중이면 성능 수치를 추정하지 않습니다.\n전체 지표 화면과 개별 이미지의 예측 점수는 구분해서 기록합니다.",735,height=43)
footer(3,"학습·평가 기록")

# PAGE 4 ---------------------------------------------------------------
header(4, "오류를 찾아 개선하기", "관찰한 오류 하나를 고르고, 확인할 근거와 바꿀 한 가지를 연결해 보세요.")
section(5, "오류 분석",121)
checks(["실제 모델 예측","수업의 가상 사례"],157)
field("이미지 이름 / 영상 시간 · 오류 위치",M,183,CW,height=25)
checks(["놓침","잘못된 클래스","과도한 / 부족한 영역","기타"],225)
answer("정답과 예측이 어떻게 다른가요?",256,height=37)
answer("확인할 데이터와 가능한 원인은 무엇인가요?",309,height=37)
answer("이번에 바꿀 한 가지는 무엇인가요?",362,height=37)
answer("어떤 Valid 이미지·조건을 유지하고, 무엇을 비교할까요?",415,height=43)
text("예: 같은 이미지·임계값에서 클래스 오류, 놓침, 도로 경계 또는 지표를 비교합니다.",M,468,size=8.5,color=MUTED,max_width=CW)
section(6,"종료 질문과 다음 시간 준비",497)
answer("인접 프레임을 같은 묶음으로 두는 이유는 무엇인가요?",535,height=31)
answer("신호등 색을 크게 바꾸는 증강에 주의할 이유는 무엇인가요?",580,height=31)
answer("내 모델에서 먼저 개선할 오류와 그 근거는 무엇인가요?",625,height=31)
field("학습이 끝났다면: 모델 식별자",M,676,CW,height=26)
field("아직 남은 작업 / 다음 시간 전에 확인할 것",M,721,CW,height=26)
text("Test는 설정 확정 후 최종 확인에 사용합니다. 모델 식별자와 API 비밀키는 다르며, 키는 적지 않습니다.",
     M,770,size=8.3,color=MUTED,max_width=CW)
footer(4,"오류 분석·마무리")

c.save()
shutil.copyfile(OUT, DEPLOY)
assert all(item["right"] <= W-M+0.5 for item in layout_checks)
assert all(item["bottom"] < H-8 for item in layout_checks)
check_path = ROOT/"tmp/pdfs/lesson-02-layout-checks.json"
check_path.parent.mkdir(parents=True, exist_ok=True)
check_path.write_text(json.dumps({"pages":4,"text_blocks":len(layout_checks),"checks":layout_checks},
    ensure_ascii=False,indent=2),encoding="utf-8")
print(json.dumps({"output":str(OUT),"download":str(DEPLOY),"pages":4,
    "text_blocks":len(layout_checks)},ensure_ascii=False))
