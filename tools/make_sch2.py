
import os
import re
import schemdraw
import schemdraw.elements as elm

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "hardware")
FONT = "Arial Unicode MS, PingFang SC, Noto Sans CJK SC, Heiti SC, sans-serif"

def lab(d, x, y, text, ha='left', size=9, color='black'):
    d += elm.Label().at((x, y)).label(text, halign=ha, fontsize=size, color=color)

def net(d, x, y, text, direction='right', color='#1a4f8a'):
    if direction == 'right':
        d += elm.Line().at((x, y)).right().length(0.9).color(color)
        lab(d, x + 1.1, y, text, 'left', 9, color)
    elif direction == 'left':
        d += elm.Line().at((x, y)).left().length(0.9).color(color)
        lab(d, x - 1.1, y, text, 'right', 9, color)
    elif direction == 'up':
        d += elm.Line().at((x, y)).up().length(0.9).color(color)
        lab(d, x, y + 1.1, text, 'center', 9, color)
    else:
        d += elm.Line().at((x, y)).down().length(0.9).color(color)
        lab(d, x, y - 1.1, text, 'center', 9, color)

with schemdraw.Drawing(file=OUT + "/fan-sch-ntc-output.svg", show=False) as d:
    d.config(unit=2.0, fontsize=9, lw=1.3)

    # ---- NTC1 divider ----
    d += elm.Vdd().at((2.6, 13)).label('+5 V')
    d += elm.Thermistor().at((2.6, 13)).down().length(2.4)
    lab(d, 1.6, 11.9, 'NTC1\n10 kΩ B3950\n贴散热器', 'right', 7.5)
    n1 = (2.6, 10.6)
    d += elm.Dot().at(n1)
    d += elm.Resistor().at(n1).down().length(2.4)
    lab(d, 1.6, 9.4, 'R1\n10 kΩ 1%', 'right', 7.5)
    d += elm.Ground().at((2.6, 8.2))
    d += elm.Dot().at((4.4, 10.6))
    d += elm.Line().at(n1).right().length(1.8)
    d += elm.Capacitor().at((4.4, 10.6)).down().length(1.7)
    lab(d, 4.7, 10.0, 'C6\n100 nF', 'left', 8)
    d += elm.Ground().at((4.4, 8.9))
    net(d, 4.4, 10.6, 'NTC_HS → PB2')

    # ---- NTC2 divider ----
    d += elm.Vdd().at((9.2, 13)).label('+5 V')
    d += elm.Thermistor().at((9.2, 13)).down().length(2.4)
    lab(d, 8.2, 11.9, 'NTC2（可选）\n10 kΩ B3950\n贴变压器', 'right', 7.5)
    n2 = (9.2, 10.6)
    d += elm.Dot().at(n2)
    d += elm.Resistor().at(n2).down().length(2.4)
    lab(d, 8.2, 9.4, 'R2\n10 kΩ 1%', 'right', 7.5)
    d += elm.Ground().at((9.2, 8.2))
    d += elm.Dot().at((11.0, 10.6))
    d += elm.Line().at(n2).right().length(1.8)
    d += elm.Capacitor().at((11.0, 10.6)).down().length(1.7)
    lab(d, 11.3, 10.0, 'C7\n100 nF', 'left', 8)
    d += elm.Ground().at((11.0, 8.9))
    net(d, 11.0, 10.6, 'NTC_TR → PB3')

    # ---- fan rails ----
    d += elm.Vdd().at((14.8, 13.5)).label('+24 V（原风扇插座）')
    d += elm.Line().at((14.8, 13.5)).down().length(1.0)
    fp = (14.8, 12.5)
    d += elm.Dot().at(fp)
    d += elm.Line().at(fp).right().length(4.9)      # F+ rail
    d += elm.Line().at(fp).down().length(3.2)       # left end down to F-
    d += elm.Dot().at((14.8, 9.3))

    # C8 across fan
    d += elm.Dot().at((16.4, 12.5))
    d += elm.Capacitor().at((16.4, 12.5)).down().length(3.2)
    lab(d, 16.7, 11.2, 'C8\n220 µF\n35 V', 'left', 7.5)
    d += elm.Dot().at((16.4, 9.3))

    # D2 across fan
    d += elm.Dot().at((18.0, 12.5))
    d += elm.Diode().at((18.0, 9.3)).up().length(3.2)
    lab(d, 18.3, 11.2, 'D2\nSS34', 'left', 7.5)
    d += elm.Dot().at((18.0, 9.3))

    # J2 connector (3-pin): 1=+24V, 2=FAN-, 3=TACH
    d += elm.Rect(w=1.4, h=3.8).at((20.6, 10.9))
    lab(d, 20.6, 12.9, 'J2', 'center', 8)
    lab(d, 20.6, 10.2, '风扇', 'center', 7.5)
    for yy, nm in [(12.5, '1'), (9.3, '2'), (10.9, '3')]:
        d += elm.Dot(open=True).at((19.9, yy))
        lab(d, 19.7, yy, nm, 'right', 8)
    d += elm.Line().at((19.9, 12.5)).right().length(0.2)
    d += elm.Line().at((19.9, 9.3)).right().length(0.2)
    d += elm.Line().at((19.9, 10.9)).right().length(0.2)
    lab(d, 20.6, 13.5, '1 +24V   2 FAN−   3 TACH', 'center', 6.5)
    lab(d, 20.6, 8.6, '（3 脚测速线悬空）', 'center', 6.5)

    # F- rail from Q1 drain to J2.2
    d += elm.Line().at((14.8, 9.3)).right().length(5.1)
    d += elm.Dot().at((14.8, 9.3))

    # Q1 low-side switch
    Q = elm.NMos().at((14.8, 9.3)).right()
    d += Q
    lab(d, 15.3, 7.0, 'Q1\nAO3400A', 'left', 9)
    d += elm.Line().at(Q.absanchors['source']).down().length(1.2)
    d += elm.Ground().at((14.8, 6.43))

    g = Q.absanchors['gate']
    d += elm.Dot().at(g)
    d += elm.Line().at(g).left().length(1.4)
    d += elm.Resistor().at((13.4, g.y)).left().length(1.6)
    lab(d, 12.6, g.y + 0.4, 'R5 100 Ω', 'center', 7.5)
    d += elm.Line().at((11.8, g.y)).left().length(0.6)
    lab(d, 11.1, g.y, 'PWM', 'right', 9, '#1a4f8a')
    lab(d, 11.1, g.y - 0.45, '← PB1', 'right', 7, '#1a4f8a')

    d += elm.Dot().at((13.1, g.y))
    d += elm.Line().at((13.1, g.y)).down().length(1.3)
    d += elm.Resistor().at((13.1, g.y - 1.3)).down().length(1.6)
    lab(d, 13.3, g.y - 2.0, 'R6\n10 kΩ', 'left', 7.5)
    d += elm.Ground().at((13.1, g.y - 2.9))

    # notes
    lab(d, 1.5, 5.0, '注 1：NTC 接法为“NTC 在上、10 kΩ 在下”，温度升高 → ADC 电压升高。', 'left', 8)
    lab(d, 1.5, 4.5, '注 2：只装 NTC1 时 PB3 悬空，固件判为“该路故障”并自动忽略，不影响运行。', 'left', 8)
    lab(d, 1.5, 4.0, '注 3：D2 为风扇反电动势续流二极管；C8 把 31 kHz PWM 滤成平滑直流，降低风扇啸叫。', 'left', 8)
    lab(d, 1.5, 3.5, '注 4：J2 的 3 脚对应原风扇黄线（测速），本方案不用，单独热缩绝缘。', 'left', 8)

svg_path = os.path.join(OUT, "fan-sch-ntc-output.svg")
with open(svg_path, encoding="utf-8") as f:
    svg = f.read()
svg = re.sub(r'font-family="[^"]*"', f'font-family="{FONT}"', svg)
with open(svg_path, "w", encoding="utf-8") as f:
    f.write(svg)

print('sheet2 ok')

