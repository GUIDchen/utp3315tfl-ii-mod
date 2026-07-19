
# -*- coding: utf-8 -*-
import os, math
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "hardware")
FONT = "Arial Unicode MS, PingFang SC, Noto Sans CJK SC, Heiti SC, sans-serif"
def esc(s): return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
class SVG:
    def __init__(self,w,h):
        self.w,self.h=w,h
        self.parts=[f'<rect x="0" y="0" width="{w}" height="{h}" fill="#fff"/>']
    def raw(self,s): self.parts.append(s)
    def rect(self,x,y,w,h,fill="#fff",stroke="#333",sw=2,rx=10,dash=None):
        d=f' stroke-dasharray="{dash}"' if dash else ""
        self.raw(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>')
    def text(self,x,y,s,size=16,fill="#111",anchor="middle",weight="normal"):
        self.raw(f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" font-weight="{weight}">{esc(s)}</text>')
    def line(self,x1,y1,x2,y2,stroke="#333",sw=2,dash=None):
        d=f' stroke-dasharray="{dash}"' if dash else ""
        self.raw(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{sw}"{d} stroke-linecap="round"/>')
    def arrow(self,x1,y1,x2,y2,stroke="#333",sw=3,dash=None):
        d=f' stroke-dasharray="{dash}"' if dash else ""
        self.raw(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{sw}"{d} stroke-linecap="round"/>')
        ang=math.atan2(y2-y1,x2-x1); L=11
        for s in (0.5,-0.5):
            self.raw(f'<line x1="{x2}" y1="{y2}" x2="{x2-L*math.cos(ang+s)}" y2="{y2-L*math.sin(ang+s)}" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round"/>')
    def save(self,p):
        open(p,"w",encoding="utf-8").write(f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" viewBox="0 0 {self.w} {self.h}">\n'+"\n".join(self.parts)+"\n</svg>\n")

s=SVG(1600,950)
s.text(40,55,"UTP3315TFL-II 电路结构与两处改造点",30,"#111","start","bold")
s.text(40,88,"上：原机功率与控制链路（据拆机与同类机型推断）；下：本次风扇温控与旋钮精度改造。",16,"#555","start")

def box(x,y,w,h,lines,stroke="#333",fill="#fff"):
    s.rect(x,y,w,h,fill,stroke,2,10)
    n=len(lines)
    for i,t in enumerate(lines):
        s.text(x+w/2, y+h/2 + (i-(n-1)/2)*22 + 6, t, 15, "#222")

# power row
box(60,150,150,80,["220 V AC"],"#333","#f7f7f7")
box(240,150,170,80,["保险丝 / 开关","110-220 V 选择"],"#333","#f7f7f7")
box(440,150,190,80,["主变压器","YSD-2160 160 W"],"#333","#f7f7f7")
box(660,150,160,80,["继电器","抽头切换 8/15/23 V"],"#333","#f7f7f7")
box(850,150,160,80,["整流 + 滤波","4700 µF"],"#333","#f7f7f7")
box(1040,150,170,80,["D1047 ×2","线性调整"],"#333","#f7f7f7")
box(1240,150,170,80,["输出","0-30 V / 0-5 A"],"#333","#eef7ee")

for x1,x2 in [(210,240),(410,440),(630,660),(820,850),(1010,1040),(1210,1240)]:
    s.arrow(x1,190,x2,190,"#333",3)

# control row
box(240,320,190,80,["辅助电源","6 V / 16 V → ±12 V, 5 V"],"#2a5f9a","#f4f7fc")
box(500,320,190,80,["显示板","4 位 LED，V/I"],"#2a5f9a","#f4f7fc")
box(760,320,240,100,["4 只电位器","V/I 粗调 + 微调","（本次换 V 粗调）"],"#b06a00","#fdf6e8")
box(1060,320,190,80,["CV 误差放大","设定 V 与反馈比较"],"#2a5f9a","#f4f7fc")
box(1280,320,170,80,["CC 误差放大","设定 I 与分流比较"],"#2a5f9a","#f4f7fc")

s.arrow(430,360,500,360,"#2a5f9a",3)
s.arrow(690,360,760,370,"#2a5f9a",3)
s.arrow(1000,360,1060,360,"#2a5f9a",3)
s.arrow(1250,360,1280,360,"#2a5f9a",3)
s.arrow(1155,320,1155,235,"#2a5f9a",3)
s.arrow(1365,320,1365,235,"#2a5f9a",3)
s.text(1160,300,"驱动",12,"#2a5f9a","start")
s.text(1370,300,"驱动",12,"#2a5f9a","start")
s.text(595,430,"显示板采样输出 V/I",12,"#2a5f9a","middle")

# fan row
box(240,600,180,80,["24 V 风扇电源","原风扇插座 1/2 脚"],"#2a7a3a","#f2f8f2")
box(520,590,230,100,["FAN-CTRL-24V","ATtiny85 + NTC","31 kHz PWM"],"#2a7a3a","#e8f5e8")
box(850,600,190,80,["原 80 mm 24 V 风扇","红/黑/黄 3 线"],"#2a7a3a","#f2f8f2")
box(520,740,160,60,["NTC1 散热器"],"#2a6fb0","#eef4fb")
box(710,740,160,60,["NTC2 变压器（可选）"],"#2a6fb0","#eef4fb")

s.arrow(420,640,520,640,"#2a7a3a",3)
s.arrow(750,640,850,640,"#2a7a3a",3)
s.arrow(600,740,600,695,"#2a6fb0",3)
s.arrow(790,740,700,695,"#2a6fb0",3)
s.text(762,680,"PWM / 平滑直流",12,"#2a7a3a","start")

# knob row
box(1060,590,210,90,["10 圈精密电位器","替换 V 粗调"],"#b06a00","#fdf6e8")
box(1330,590,160,90,["V 设定节点","（原电位器焊盘）"],"#b06a00","#fdf6e8")
s.arrow(1270,635,1330,635,"#b06a00",3)
s.line(1410,590,1410,440,"#b06a00",2,"6 5")
s.line(1410,440,1155,440,"#b06a00",2,"6 5")
s.arrow(1155,440,1155,400,"#b06a00",2,"6 5")
s.text(1420,500,"改这里",12,"#b06a00","start")

# notes
s.text(40,870,"改造原则：风扇只改供电与温控，不动主功率环路；旋钮只换同阻值电位器，不改设定网络。",14,"#444","start")
s.text(40,898,"风险点：PWM 地电流与 NTC 走线可能耦合噪声；开面板孔与拆焊电位器可能伤及 PCB；改动后必须重新校验 V/I 精度。",14,"#a00","start")
s.text(40,926,"未验证项：主板上 24 V 风扇供电的实际电流余量、电位器实际阻值与引脚定义，施工前必须实测。",14,"#666","start")

s.save(os.path.join(OUT,"system-block.svg"))
print("ok")

