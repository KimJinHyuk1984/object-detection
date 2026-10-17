"""A synthetic road scene and hand-written predictions, never model inference."""
from PIL import Image, ImageDraw, ImageFont


def make_demo():
    image = Image.new("RGB", (960, 540), "#DCECF3")
    draw = ImageDraw.Draw(image)
    draw.rectangle((0,190,960,540), fill="#A3AC9E")
    draw.polygon([(270,190),(690,190),(960,540),(0,540)], fill="#59636A")
    draw.line([(430,210),(280,540)], fill="#FAF6D8", width=5)
    draw.line([(530,210),(680,540)], fill="#FAF6D8", width=5)
    predictions = []

    def prediction(label, box, confidence, points=None):
        left,top,right,bottom=box
        value={"class":label,"confidence":confidence,"x":(left+right)/2,"y":(top+bottom)/2,
               "width":right-left,"height":bottom-top}
        if points:
            value["points"]=[{"x":x,"y":y} for x,y in points]
        predictions.append(value)

    draw.rounded_rectangle((170,325,275,420), radius=12, fill="#367FC1")
    draw.rectangle((183,339,262,365), fill="#B9E2EF")
    draw.rectangle((180,411,197,431), fill="#26333B")
    draw.rectangle((247,411,264,431), fill="#26333B")
    prediction("car",(168,323,278,434),0.94)

    draw.ellipse((710,393,735,430),fill="#26333B")
    draw.ellipse((748,393,773,430),fill="#26333B")
    draw.line([(722,405),(739,375),(760,408)],fill="#E59F47",width=12)
    draw.ellipse((732,348,749,366),fill="#26333B")
    prediction("motor",(706,346,777,433),0.63)

    draw.ellipse((835,253,858,276),fill="#B97B58")
    draw.line([(846,277),(846,318)],fill="#754CA5",width=15)
    draw.line([(846,316),(832,343)],fill="#26333B",width=8)
    draw.line([(846,316),(861,343)],fill="#26333B",width=8)
    prediction("people",(825,250,866,348),0.82)

    for label,x,color,confidence in [
        ("lampg",145,"#1FAC72",0.91),("lampr",295,"#D94A4A",0.87),
        ("lampy",650,"#EBC84D",0.56),("lamp",800,"#879299",0.38)
    ]:
        draw.line([(x,175),(x,235)],fill="#4C565B",width=6)
        draw.rounded_rectangle((x-17,100,x+17,176),radius=8,fill="#26333B")
        draw.ellipse((x-10,128,x+10,148),fill=color)
        prediction(label,(x-19,98,x+19,178),confidence)

    draw.line([(565,145),(565,217)],fill="#4C565B",width=6)
    draw.polygon([(565,91),(595,145),(535,145)],fill="#EAE4CE",outline="#AD503F",width=5)
    prediction("sign",(533,89,597,148),0.72)
    points=[(430,210),(530,210),(680,539),(280,539)]
    prediction("line",(280,210,680,539),0.88,points)
    draw.rectangle((0,0,960,32),fill="#182B36")
    draw.text((12,7),"DEMO / SYNTHETIC ROAD SCENE",fill="white",font=ImageFont.load_default(size=17))
    return image, {"image":{"width":960,"height":540},"predictions":predictions}
