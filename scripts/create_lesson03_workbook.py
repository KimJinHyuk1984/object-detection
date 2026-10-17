"""Build the two-page, print-ready Korean lesson 3 workbook.

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

OUT = ROOT / "output/pdf/lesson-03-workbook.pdf"
OUT.parent.mkdir(parents=True, exist_ok=True)
DEPLOY = ROOT / "files/lesson-03-workbook.pdf"
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
c.setTitle("3차시 활동지 - API로 이미지 앱 만들기")
c.setAuthor("자율주행 자동차 모델 만들기")
c.setSubject("Streamlit 앱 실행, 표시 조건 비교, Roboflow API 연결과 오류 점검")
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
    right="LESSON 03  /  WORKBOOK"
    tw=pdfmetrics.stringWidth(right, "Korean", 8)
    text(right, W-M-tw, 29, size=8, color=MUTED)
    text(title, M, 48, size=23, bold=True, max_width=CW)
    text(subtitle, M, 80, size=9.3, color=MUTED, max_width=CW)
    line(M, 101, W-M, 101, color=TEAL, width=1.2)

def footer(number, topic):
    line(M, 803, W-M, 803, color=LINE)
    text(f"3차시 · {topic}", M, 813, size=8.3, color=MUTED)
    text(f"{number} / 2", W-M-27, 812, size=9, bold=True, color=TEAL)
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
header(1,"이미지 분석 앱 실습 기록","3차시 · API 키 없이 예제로 시작하고, 표시 조건이 결과에 미치는 영향을 관찰합니다.")
fields([("이름 / 모둠",1),("날짜",1)],113,height=28)
checks(["예제 결과로 연습","내 모델로 분석 (학습 후)"],157)
section(1,"앱 실행 확인",187)
checks(["실습 폴더와 파일을 확인했다"],226)
checks(["앱을 실행하고 입력 이미지와 결과를 비교했다"],253)
checks(["예제 결과와 실제 모델의 예측을 구분할 수 있다"],280)
section(2,"표시 조건 비교",318)
text("예제 모드에서 모든 클래스를 선택하고, 같은 이미지로 세 조건을 비교하세요.",M,352,size=9,color=MUTED,max_width=CW)
table(["표시 임계값","객체 수","도로 영역 수","사라진 대상","변화 설명"],
      [77,69,79,132,CW-357],
      [["0.40","","","",""],["0.70","","","",""],["0.90","","","",""]],
      378,row_height=48,header_height=34)
note("객체 수와 line 영역 수를 구분합니다. 표의 숫자는 예제에서 관찰한 표시 개수입니다.\n이 결과만으로 실제 모델의 정확도를 판단하지 않습니다.",573,height=43)
answer("line만 선택하고 불투명도를 바꾸면, 예측 값과 화면 중 무엇이 바뀌나요?",641,height=40)
fields([("저장한 결과 PNG 파일명",1),("적용한 임계값 / 선택 클래스",1)],709,height=28)
text("예제 PNG의 DEMO 표시와 JSON의 출처를 확인합니다. API 키는 기록하지 않습니다.",M,768,size=8.5,color=MUTED,max_width=CW)
footer(1,"실행·표시 조건 비교")

# PAGE 2 ---------------------------------------------------------------
header(2,"연결 준비와 오류 점검","학습 전에는 실제 모델 설정을 비워 두고, 예제로 응답과 표시 흐름을 설명합니다.")
section(3,"모델 연결 준비",121)
field("학습이 끝났다면 모델 ID (프로젝트이름 / 버전번호)",M,160,CW,height=27)
checks(["분할 모델 유형 확인","Serverless 지원 확인","아직 학습 전 / 확인 전"],206,size=9)
answer("응답의 x·y·width·height와 points는 각각 어떤 표시를 만들까요?",241,height=40)
note("모델 ID는 모델과 버전을 선택하는 값입니다. API 키는 요청 권한을 확인하는 비밀값입니다.\n실제 API 키는 본인 컴퓨터의 설정에만 넣고 활동지·캡처·Git에 포함하지 않습니다.",301,height=43)
section(4,"오류 한 가지와 해결 순서",367)
checks(["설정 없음","요청 실패","표시 결과 0개","line 폴리곤 없음"],407,size=9)
answer("어떤 상황에서 어떤 현상이 나타났나요?",440,height=38)
answer("먼저 확인할 항목과 다음에 시도할 것은 무엇인가요?",494,height=38)
section(5,"종료 질문",558)
answer("임계값을 바꿀 때마다 API를 다시 호출해야 하나요? 이유를 적으세요.",597,height=31)
answer("새 이미지나 모델로 바뀌면 이전 결과를 지워야 하는 이유는 무엇인가요?",642,height=31)
answer("영상의 모든 프레임을 API에 보내면 시간과 사용량은 어떻게 달라질까요?",687,height=31)
field("다음 시간 전 확인할 것",M,744,CW,height=27)
footer(2,"연결·오류·마무리")

c.save()
shutil.copyfile(OUT, DEPLOY)
assert all(item["right"] <= W-M+0.5 for item in layout_checks)
assert all(item["bottom"] < H-8 for item in layout_checks)
print(json.dumps({"output":str(OUT),"download":str(DEPLOY),"pages":2,
    "text_blocks":len(layout_checks)},ensure_ascii=False))
