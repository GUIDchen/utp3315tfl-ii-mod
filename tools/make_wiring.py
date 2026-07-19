
# -*- coding: utf-8 -*-
import os, math
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "hardware")
FONT = "Arial Unicode MS, PingFang SC, Noto Sans CJK SC, Heiti SC, sans-serif"

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

class SVG:
    def __init__(self, w, h, bg="#ffffff"):
        self.w, self.h = w, h
        self.parts = [f'<rect x="0" y="0" width="{w}" height="{h}" fill="{bg}"/>']
    def raw(self, s): self.parts.append(s)
    def rect(self, x, y, w, h, fill="#ffffff", stroke="#333333", sw=2, rx=8, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.raw(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>')
    def circle(self, cx, cy, r, fill="#ffffff", stroke="#333333", sw=2, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.raw(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>')
    def line(self, x1, y1, x2, y2, stroke="#333333", sw=2, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.raw(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{sw}"{d} stroke-linecap="round"/>')
    def poly(self, pts, stroke="#333333", sw=5, fill="none", dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        p = " ".join(f"{x},{y}" for x, y in pts)
        self.raw(f'<polyline points="{p}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d} stroke-linejoin="round" stroke-linecap="round"/>')
    def text(self, x, y, s, size=18, fill="#111111", anchor="start", weight="normal"):
        self.raw(f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" font-weight="{weight}">{esc(s)}</text>')
    def save(self, path):
        svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" viewBox="0 0 {self.w} {self.h}">\n' + "\n".join(self.parts) + "\n</svg>\n"
        open(path, "w", encoding="utf-8").write(svg)

s = SVG(1700, 1000)
s.text(40, 55, "UTP3315TFL-II 风扇温控改造 · 机内接线示意", 30, "#111", weight="bold")
s.text(40, 88, "俯视示意，不按比例；施工前务必断电并放电。红色=+24V，黑色=GND，黄色=测速，蓝色=NTC。", 16, "#555")

# fan
s.rect(60, 130, 230, 250, "#f6f6f6", "#888", 2, 10)
s.circle(175, 255, 82, "#e9e9e9", "#555", 3)
s.circle(175, 255, 20, "#cfcfcf", "#555", 2)
for ang in (30, 120, 210, 300):
    a = math.radians(ang)
    s.line(175 + 22*math.cos(a), 255 + 22*math.sin(a), 175 + 72*math.cos(a), 255 + 72*math.sin(a), "#555", 5)
s.text(175, 405, "原机 80×80×25 风扇", 15, "#333", "middle")
s.text(175, 428, "24 V，3 线（红/黑/黄）", 14, "#666", "middle")

s.poly([(240, 200), (600, 200), (620, 200)], "#d33", 5)
s.poly([(240, 240), (580, 240), (620, 240)], "#222", 5)
s.poly([(240, 280), (520, 280)], "#e0b000", 5)
s.line(525, 270, 550, 290, "#d00", 3)
s.line(550, 270, 525, 290, "#d00", 3)
s.text(60, 470, "风扇黄线（测速）不接，单独热缩绝缘", 14, "#a00")

# board
s.rect(620, 120, 340, 450, "#eef7ee", "#2a7a3a", 3, 10)
s.text(790, 155, "FAN-CTRL-24V 控制板", 18, "#1c5c2a", "middle", "bold")
s.text(790, 180, "ATtiny85 + NTC + PWM", 14, "#3a6a45", "middle")

# J2
s.rect(605, 185, 30, 75, "#fff", "#333", 2, 4)
s.text(645, 175, "J2 风扇", 13, "#333", "start", "bold")
for yy, c, nm in [(200, "#d33", "+24V"), (240, "#222", "FAN−"), (280, "#e0b000", "TACH")]:
    s.circle(620, yy, 6, "#fff", c, 3)
    s.text(642, yy+4, nm, 11, "#333")

# J1
s.rect(605, 310, 30, 55, "#fff", "#333", 2, 4)
s.text(645, 300, "J1 24V 输入", 13, "#333", "start", "bold")
s.circle(620, 330, 6, "#fff", "#d33", 3)
s.circle(620, 355, 6, "#fff", "#222", 3)
s.text(642, 334, "+24V", 11, "#333")
s.text(642, 359, "GND", 11, "#333")

# J3/J4
s.text(790, 330, "J3  NTC1（散热器）", 14, "#2a6fb0", "middle")
s.text(790, 355, "J4  NTC2（变压器，可选）", 14, "#2a6fb0", "middle")
s.rect(690, 545, 60, 25, "#fff", "#333", 2, 4)
s.rect(810, 545, 60, 25, "#fff", "#333", 2, 4)
s.text(720, 538, "J3", 13, "#333", "middle")
s.text(840, 538, "J4", 13, "#333", "middle")

# internals
s.rect(700, 400, 90, 50, "#fff", "#2a7a3a", 2, 6)
s.text(745, 430, "U2", 14, "#1c5c2a", "middle", "bold")
s.rect(820, 400, 80, 50, "#fff", "#2a7a3a", 2, 6)
s.text(860, 430, "Q1", 14, "#1c5c2a", "middle", "bold")
s.rect(700, 470, 200, 45, "#fff", "#2a7a3a", 2, 6)
s.text(800, 498, "C8 / D2 / 78L05", 13, "#1c5c2a", "middle")

# original socket
s.rect(110, 690, 240, 170, "#f6f6f6", "#888", 2, 10)
s.text(230, 720, "原风扇插座（主板）", 16, "#333", "middle", "bold")
for yy, c, nm in [(750, "#d33", "1  +24V"), (785, "#222", "2  GND"), (820, "#e0b000", "3  TACH")]:
    s.circle(350, yy, 7, "#fff", c, 3)
    s.text(338, yy+4, nm, 12, "#333", "end")

s.poly([(357, 750), (565, 750), (565, 330), (620, 330)], "#d33", 5)
s.poly([(357, 785), (585, 785), (585, 355), (620, 355)], "#222", 5)
s.poly([(357, 820), (430, 820)], "#e0b000", 5)
s.line(435, 810, 455, 830, "#d00", 3)
s.line(455, 810, 435, 830, "#d00", 3)
s.text(465, 826, "不接", 13, "#a00")

# heatsink
s.rect(1140, 130, 300, 280, "#e3e3e3", "#666", 2, 8)
for i in range(6):
    s.line(1160 + i*40, 145, 1160 + i*40, 395, "#aaa", 3)
s.rect(1180, 200, 60, 90, "#fff", "#333", 2, 4)
s.rect(1260, 200, 60, 90, "#fff", "#333", 2, 4)
s.text(1250, 245, "D1047 ×2", 13, "#333", "middle", "bold")
s.circle(1310, 165, 14, "#dfefff", "#2a6fb0", 3)
s.text(1332, 170, "NTC1", 14, "#2a6fb0", "start", "bold")
s.text(1130, 420, "功率管散热器", 15, "#333", "end")
s.text(1130, 442, "NTC1 贴 D1047", 13, "#666", "end")

# transformer
s.rect(1140, 650, 320, 230, "#f4e7c8", "#a87a20", 2, 8)
s.text(1320, 780, "主变压器", 17, "#6b4a10", "middle", "bold")
s.text(1320, 805, "YSD-2160", 13, "#6b4a10", "middle")
s.circle(1165, 700, 14, "#dfefff", "#2a6fb0", 3)
s.text(1187, 705, "NTC2（可选）", 13, "#2a6fb0", "start", "bold")

# NTC cables
s.poly([(1310, 179), (1310, 600), (720, 600), (720, 570)], "#2a6fb0", 4)
s.poly([(1165, 714), (1165, 640), (840, 640), (840, 570)], "#2a6fb0", 4)

# notes
s.text(40, 930, "施工要点：1) 断开原风扇插头，万用表确认 24 V 与 GND；2) 原插座只取电给 J1，风扇改由 J2 供电；", 14, "#444")
s.text(40, 955, "3) 风扇黄线不接，单独热缩；4) NTC 引线远离 220 V、继电器与整流桥；5) 控制板用尼龙柱固定，避免与市电走线交叉。", 14, "#444")

s.save(os.path.join(OUT, "fan-wiring.svg"))
print("ok")

