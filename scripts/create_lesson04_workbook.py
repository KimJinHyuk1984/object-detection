"""Build the three-page, print-ready Korean lesson 4 workbook.

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

OUT = ROOT / "output/pdf/lesson-04-workbook.pdf"
OUT.parent.mkdir(parents=True, exist_ok=True)
DEPLOY = ROOT / "files/lesson-04-workbook.pdf"
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
c.setTitle("4차시 활동지 - 주행 인식 앱을 검증하고 공유하기")
c.setAuthor("자율주행 자동차 모델 만들기")
c.setSubject("새 영상 검증, 조건 비교, 공유 체험과 결과 발표")
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
    right="LESSON 04  /  WORKBOOK"
    tw=pdfmetrics.stringWidth(right, "Korean", 8)
    text(right, W-M-tw, 29, size=8, color=MUTED)
    text(title, M, 48, size=23, bold=True, max_width=CW)
    text(subtitle, M, 80, size=9.3, color=MUTED, max_width=CW)
    line(M, 101, W-M, 101, color=TEAL, width=1.2)

def footer(number, topic):
    line(M, 803, W-M, 803, color=LINE)
    text(f"4차시 · {topic}", M, 813, size=8.3, color=MUTED)
    text(f"{number} / 3", W-M-27, 812, size=9, bold=True, color=TEAL)
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
header(1,"검증의 기준과 관찰","4차시 · 처음 보는 주행영상에서 성공과 실패를 근거로 기록합니다.")
fields([("이름 / 모둠",1),("날짜",1)],113,height=28)
section(1,"같은 조건으로 확인하기",164)
checks(["객체 종류·위치","line 도로 영역","신호 색·안내"],203,size=9.5)
field("영상 파일명 · 학습에 사용하지 않은 영상인지 확인",M,239,CW,height=27)
fields([("영상 길이 (초)",1),("분석 빈도 (회/초)",1),("묶음 크기 (장)",1),("신뢰도 기준 (%)",1)],283,height=27)
field("Workspace / Workflow ID · API 키는 기록하지 않습니다",M,327,CW,height=27)
field("Workflow에 연결된 프로젝트 / 실제 모델 버전",M,371,CW,height=27)
note("line은 차선 사이의 주행 가능한 도로 영역입니다. 신뢰도 퍼센트는 정확도가 아닙니다.\nMODEL RESULT에서 확인합니다. 분석 대기 상태를 모델의 미탐으로 기록하지 않습니다.",418,height=43)
section(2,"성공·실패 장면 하나씩 찾기",480)
table(["구분","재생 시각","대상과 관찰한 현상 · 원인 추측은 구분하기"],
      [65,70,CW-135],
      [["성공","",""],["실패","",""]],
      520,row_height=65,header_height=34,font_size=9.5)
checks(["미탐","오탐·오분류","영역 경계","판단 어려움"],704,size=9.2)
text("저장: 01-success.png / 02-error.png · 실패를 못 찾았다면 관찰 범위를 적으세요.",M,740,size=8.7,color=MUTED,max_width=CW)
checks(["내가 직접 분석","교사의 저장 결과 관찰"],768,size=9.2)
footer(1,"새 영상 검증")

# PAGE 2 ---------------------------------------------------------------
header(2,"표시 조건을 공정하게 비교하기","같은 장면의 신뢰도 기준 비교 · 분석 빈도 비교는 교사의 사전 측정 자료로 확인")
section(3,"신뢰도 기준 40%와 70%",121)
fields([("같은 재생 시각 (분:초)",1),("선택 클래스 / 마스크 불투명도",1.5)],162,height=27)
table(["신뢰도 기준","객체 수","line 수","신호 안내","달라진 대상·표시"],
      [72,56,58,102,CW-288],
      [["40%","","","",""],["70%","","","",""]],
      212,row_height=63,header_height=34)
note("영상·모델·시각·분석 결과를 고정하고 신뢰도 기준만 바꿉니다. 이 변경 자체는 재추론하지\n않습니다. 결과가 같아도 그대로 기록합니다. 저장: 03-threshold-040.png / 04-threshold-070.png",390,height=43)
section(4,"초당 2회와 5회 분석 비교",458)
text("180초 영상·8장 묶음 계산 예시입니다. 처리 시간은 교사의 실제 측정값을 적으세요.",M,494,size=8.8,color=MUTED,max_width=CW)
table(["항목","초당 2회","초당 5회"],
      [156,(CW-156)/2,(CW-156)/2],
      [["분석 이미지 수 (계산)","360장","900장"],
       ["HTTP 요청 수 (계산)","약 45개","약 113개"],
       ["전체 처리 시간 (실측)","________ 초","________ 초"]],
      518,row_height=34,header_height=32)
text("분석 시각 간격: 약 0.5초 / 0.2초 · 원본 재생 FPS와 다릅니다.",M,668,size=9,color=MUTED,max_width=CW)
text("빈도를 바꾸면 재분석이 필요합니다. 실제 시간·사용량은 실행 조건에 따라 달라집니다.",M,690,size=8.7,color=MUTED,max_width=CW)
answer("직접 관찰한 변화 한 가지와, 추가로 확인할 원인 가설 한 가지",727,height=49)
footer(2,"조건 비교·근거 기록")

# PAGE 3 ---------------------------------------------------------------
header(3,"다른 환경에서 확인하고 발표하기","공유 방식과 실제 확인 범위를 구분하고 다음 개선 행동을 정합니다.")
section(5,"공유 체험 기록",121)
checks(["A · 배포 주소 접속","B · 별도 PC 실행","직접 확인 못 함"],164,size=9.1)
field("실제 주소 또는 PC / 브라우저 · localhost는 접속한 PC 자신입니다",M,202,CW,height=28)
checks(["앱 실행","영상 재생·탐색","실제 모델 결과"],251,size=9.3)
checks(["객체 박스","line 도로 마스크","신호 안내"],278,size=9.3)
field("확인 범위와 남은 문제 · 저장: 05-sharing-check.png",M,315,CW,height=32)
section(6,"60초 발표 준비",378)
answer("성공: 어떤 조건·장면에서 무엇이 잘 되었나요?",418,height=34)
answer("실패: 무엇을 놓치거나 잘못 표시했나요? 근거는 무엇인가요?",469,height=34)
answer("개선: 다음에 무엇을 바꾸고, 어떤 같은 조건으로 확인할까요?",520,height=42)
note("발표 순서: 조건 15초 → 성공·실패 근거 25초 → 다음 행동 20초.\nB는 재현 확인이며 외부 배포 완료가 아닙니다. 신호 안내는 학습용 출력입니다.",585,height=43)
section(7,"짝의 피드백",652)
checks(["조건 기록","근거 일치","공정한 비교","구체적인 개선"],694,size=9.2)
field("짝의 한마디 또는 내가 보완할 점",M,735,CW,height=37)
footer(3,"공유·발표·개선")

c.save()
shutil.copyfile(OUT, DEPLOY)
assert all(item["right"] <= W-M+0.5 for item in layout_checks)
assert all(item["bottom"] < H-8 for item in layout_checks)
print(json.dumps({"output":str(OUT),"download":str(DEPLOY),"pages":3,
    "text_blocks":len(layout_checks),"bounds_passed":True},ensure_ascii=False))
