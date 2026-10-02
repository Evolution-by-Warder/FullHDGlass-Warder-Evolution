#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFilter
import sys

out = sys.argv[1]
W, H = 1280, 720
img = Image.new("RGB", (W, H), (3, 10, 18))
px = img.load()
for y in range(H):
    for x in range(W):
        px[x, y] = (int(3 + 8*x/W + 7*y/H), int(10 + 13*x/W), int(18 + 22*(1-y/H)))
draw = ImageDraw.Draw(img, "RGBA")
for y in range(450, H):
    a = int(45 * (1 - (y - 450) / 270.0))
    draw.line((0, y, W, y), fill=(20, 100, 160, max(0, a)))
bars = [28,45,72,54,88,122,95,67,110,150,120,82,60,95,135,104,72,48]
for i, h in enumerate(bars):
    x = 65 + i * 24
    draw.rounded_rectangle((x, 430-h, x+10, 430), 4, fill=(25, 180, 255, 120))
for i, h in enumerate(reversed(bars)):
    x = 920 + i * 17
    draw.rounded_rectangle((x, 450-h, x+8, 450), 3, fill=(255, 170, 45, 125))
draw.ellipse((140, 90, 355, 420), fill=(6, 15, 24, 235), outline=(45, 180, 245, 210), width=5)
for yy in range(125, 365, 13):
    draw.line((165, yy, 330, yy), fill=(90, 175, 220, 100), width=2)
for xx in range(175, 330, 16):
    draw.line((xx, 115, xx-18, 375), fill=(90, 175, 220, 80), width=1)
draw.rounded_rectangle((175, 360, 320, 445), 24, fill=(20, 24, 30, 245), outline=(255, 172, 55, 180), width=4)
draw.line((248, 445, 205, 520), fill=(80, 90, 100, 255), width=12)
draw.line((248, 445, 292, 520), fill=(80, 90, 100, 255), width=12)
draw.arc((118, 74, 380, 440), 205, 335, fill=(30, 210, 255, 240), width=7)
draw.arc((130, 88, 368, 426), 20, 150, fill=(255, 165, 48, 230), width=6)
cx, cy, rr = 1030, 285, 185
draw.ellipse((cx-rr, cy-rr, cx+rr, cy+rr), fill=(5, 25, 42, 240), outline=(255, 173, 60, 220), width=5)
for off in (-95,-48,0,48,95):
    draw.arc((cx-rr, cy-rr+off//3, cx+rr, cy+rr-off//3), 0, 359, fill=(35, 150, 210, 95), width=2)
for frac in (0.35,0.62,0.82):
    ew = int(rr*2*frac)
    draw.ellipse((cx-ew//2, cy-rr, cx+ew//2, cy+rr), outline=(255, 183, 70, 90), width=2)
europe=[(996,205),(1028,190),(1065,205),(1084,232),(1056,247),(1025,238),(1002,250),(978,232)]
africa=[(1015,250),(1060,252),(1080,288),(1063,330),(1036,375),(1008,340),(995,300)]
draw.polygon(europe, fill=(240,175,65,165)); draw.polygon(africa, fill=(225,145,45,150))
draw.arc((cx-rr-30,cy-rr-18,cx+rr+40,cy+rr+18),210,20,fill=(255,175,50,230),width=6)
draw.arc((cx-rr-10,cy-rr+25,cx+rr+55,cy+rr-25),25,195,fill=(45,190,255,190),width=5)
draw.rounded_rectangle((440,95,840,515), 10, fill=(3, 9, 15, 218), outline=(48, 150, 205, 150), width=2)
draw.rounded_rectangle((15,12,W-15,72), 10, fill=(1,6,11,225), outline=(45,120,170,150), width=2)
draw.rounded_rectangle((15,545,W-15,H-18), 10, fill=(1,6,11,230), outline=(45,120,170,150), width=2)
img = img.filter(ImageFilter.GaussianBlur(radius=0.35))
img.save(out, "PNG")
print("Generated", out)
