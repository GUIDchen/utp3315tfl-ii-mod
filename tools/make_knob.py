
# -*- coding: utf-8 -*-
import os, math
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "hardware")
FONT = "Arial Unicode MS, PingFang SC, Noto Sans CJK SC, Heiti SC, sans-serif"

def esc(s): return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")

class SVG:
    def __init__(self,w,h,bg="#ffffff"):
        self.w,self.h=w,h
        self.parts=[f'<rect x="0" y="0" width="{w}" height="{h}" fill="{bg}"/>']
    def raw(self,s): self.parts.append(s)
    def rect(self,x,y,w,h,fill="#fff",stroke="#333",sw=2,rx=8,dash=None):
        d=f' stroke-dasharray="{dash}"' if dash else ""
        self.raw(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>')
    def circle(self,cx,cy,r,fill="#fff",stroke="#333",sw=2,dash=None):
        d=f' stroke-dasharray="{dash}"' if dash else ""
        self.raw(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>')
    def line(self,x1,y1,x2,y2,stroke="#333",sw=2,dash=None):
        d=f' stroke-dasharray="{dash}"' if dash else ""
        self.raw(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{sw}"{d} stroke-linecap="round"/>')
    def text(self,x,y,s,size=18,fill="#111",anchor="start",weight="normal"):
        self.raw(f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" font-weight="{weight}">{esc(s)}</text>')
    def save(self,p):
        open(p,"w",encoding="utf-8").write(f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" viewBox="0 0 {self.w} {self.h}">\n'+"\n".join(self.parts)+"\n</svg>\n")

s=SVG(1600,1180)
s.text(40,55,"UTP3315TFL-II 电压调节旋钮精度改造 · 接线与安装示意",30,"#111",weight="bold")
s.text(40,88,"方案：把 VOLTAGE COARSE 碳膜单圈电位器换成同阻值 10 圈精密电位器，保留 FINE 微调。",16,"#555")

# ---------------- left: display board ----------------
s.rect(60,120,460,760,"#f2f7f2","#2a7a3a",3,10)
s.text(290,158,"原机显示板（背面）",18,"#1c5c2a","middle","bold")
pots=[(180,265,"VOLTAGE COARSE","V-粗调"),(180,455,"VOLTAGE FINE","V-微调"),(180,645,"CURRENT COARSE","I-粗调"),(180,835,"CURRENT FINE","I-微调")]
for cx,cy,en,cn in pots:
    s.text(cx,cy-72,en,13,"#333","middle","bold")
    s.text(cx,cy-52,cn,12,"#666","middle")
    s.circle(cx,cy,52,"#dcdcdc","#555",3)
    s.circle(cx,cy,9,"#bbb","#555",2)

# highlight V coarse
s.rect(110,190,300,150,"none","#d00",3,10,"8 6")


# terminals of highlighted pot (outside the circle, to the right)
for yy,n in [(240,"1"),(265,"2"),(290,"3")]:
    s.circle(255,yy,7,"#fff","#333",3)
    s.text(268,yy+4,n,12,"#333")
s.text(292,238,"先标记线序",11,"#a00")
# ribbon to 8P
s.line(262,265,420,265,"#666",3,"6 4")
s.rect(420,235,60,60,"#fff","#666",2,4)
s.text(450,225,"8P 排线",11,"#333","middle")
s.text(450,318,"→ 主板",11,"#333","middle")
s.text(290,910,"先拍照、标记 1/2/3；实测阻值（常见 1 kΩ，以实物为准）",12,"#a00","middle")

# ---------------- right: 10-turn pot ----------------
s.rect(760,120,800,430,"#f7f9fc","#2a5f9a",3,10)
s.text(1160,165,"10 圈精密电位器（同阻值替换）",18,"#1d4670","middle","bold")
s.circle(1050,350,85,"#e8eef7","#2a5f9a",3)
s.circle(1050,350,14,"#c9d6e8","#2a5f9a",2)
s.text(1050,350,"10T",14,"#1d4670","middle","bold")
s.circle(1050,350,108,"none","#888",2,"4 4")
s.line(1050,242,1050,205,"#333",4)
s.text(1070,212,"旋钮 Ø22",12,"#555","start")
for x,y,nm in [(950,440,"CCW"),(1050,465,"WIPER"),(1150,440,"CW")]:
    s.circle(x,y,9,"#fff","#333",3)
    s.text(x,y+30,nm,12,"#333","middle")
s.line(1050,440,1050,465,"#333",3)
s.text(1050,520,"10 圈 = 3600°；30 V 量程约 8.3 mV/°",13,"#1d4670","middle")

# table
s.text(800,595,"接线对应（以实测为准）",15,"#111","start","bold")
rows=[("原电位器 1（CCW）","→ 新电位器 CCW","#333"),
      ("原电位器 2（WIPER）","→ 新电位器 WIPER","#a00"),
      ("原电位器 3（CW）","→ 新电位器 CW","#333")]
for i,(a,b,c) in enumerate(rows):
    s.text(800,630+i*30,a,13,"#333")
    s.text(1015,630+i*30,b,13,c,"start","bold")
s.text(800,735,"要求：阻值一致（常见 1 kΩ；以实测为准），线性 B 型，功率 ≥0.5 W。",12,"#555")
s.text(800,760,"WIPER 线最短、双绞；焊点热缩，避免与面板金属件短路。",12,"#555")

# ---------------- bottom: cross section ----------------
s.text(60,950,"安装剖面（不按比例）",16,"#111","start","bold")
s.line(220,985,220,1100,"#333",6)
s.text(220,975,"面板",12,"#333","middle")
s.line(360,985,360,1100,"#2a7a3a",6)
s.text(360,975,"显示板",12,"#2a7a3a","middle")
s.rect(370,1010,90,65,"#dcdcdc","#555",2,6)
s.text(415,1045,"本体",11,"#333","middle")
s.line(460,1042,150,1042,"#666",8)
s.rect(100,1017,50,50,"#c9d6e8","#2a5f9a",2,6)
s.text(125,1090,"旋钮",11,"#333","middle")
s.text(220,1125,"开孔 Ø9.5",11,"#a00","middle")
s.text(415,1120,"Ø22 × 22 深",11,"#333","middle")
s.text(300,1150,"轴 Ø6.35 × 20",11,"#333","middle")

# ---------------- alternative notes ----------------
s.text(800,930,"若面板空间不足 / 不想开孔：",15,"#111","start","bold")
s.text(800,960,"① 5:1 行星减速旋钮（3D 打印或成品慢调旋钮），分辨率提高 5 倍，不改电路；",13,"#444")
s.text(800,985,"② 只在面板背面加 L 支架固定 10 圈电位器，用 6 mm 联轴器接原轴；",13,"#444")
s.text(800,1010,"③ 电子微调：在设定电压节点叠加 ±0.5 V 精密基准（需读懂电路，风险较高）。",13,"#444")
s.text(800,1050,"注意：改后先空载校验 0 V / 5 V / 12 V / 24 V / 30 V，再带载测试；",13,"#a00")
s.text(800,1075,"     若显示值与万用表差 >20 mV，再微调主板 V 校准电位器（先标记原位）。",13,"#a00")

s.save(os.path.join(OUT,"knob-wiring.svg"))
print("ok")

