
import os
import re
import schemdraw
import schemdraw.elements as elm

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "hardware")
FONT = "Arial Unicode MS, PingFang SC, Noto Sans CJK SC, Heiti SC, sans-serif"

def lab(d, x, y, text, ha='left', size=9, color='black'):
    d += elm.Label().at((x, y)).label(text, halign=ha, fontsize=size, color=color)

with schemdraw.Drawing(file=OUT + "/fan-sch-power-mcu.svg", show=False) as d:
    d.config(unit=2.0, fontsize=9, lw=1.3)

    # ================= power input =================
    d += elm.Rect(w=1.4, h=2.4).at((1.4, 12.6))
    lab(d, 1.4, 14.0, 'J1', 'center', 8)
    lab(d, 1.4, 11.1, '24V IN', 'center', 7)
    d += elm.Dot(open=True).at((2.1, 13.3))
    d += elm.Dot(open=True).at((2.1, 11.9))
    lab(d, 2.25, 13.55, '+', 'left', 8)
    lab(d, 2.25, 11.65, '−', 'left', 8)
    d += elm.Line().at((2.1, 13.3)).right().length(0.4)
    d += elm.Line().at((2.1, 11.9)).right().length(0.4)

    d += elm.Fuse().at((2.5, 13.3)).right().length(1.8)
    lab(d, 3.4, 13.8, 'F1 0.5 A', 'center', 7.5)
    d += elm.Schottky().at((4.3, 13.3)).right().length(1.8)
    lab(d, 5.2, 13.8, 'D1 SS34', 'center', 7.5)
    node = (6.1, 13.3)
    d += elm.Dot().at(node)
    d += elm.Capacitor().at(node).down().length(2.0)
    lab(d, 6.35, 12.4, 'C1\n220 µF\n35 V', 'left', 7.5)
    d += elm.Ground().at((6.1, 11.3))
    d += elm.Resistor().at(node).right().length(1.5)
    lab(d, 6.9, 13.8, 'R17 470 Ω', 'center', 7.5)

    # 78L05
    d += elm.Rect(w=2.1, h=2.0).at((9.1, 13.3))
    lab(d, 9.1, 14.6, 'U1  78L05', 'center', 8)
    lab(d, 8.3, 13.6, 'IN', 'left', 7)
    lab(d, 9.9, 13.6, 'OUT', 'right', 7)
    lab(d, 9.1, 12.9, 'GND', 'center', 7)
    d += elm.Line().at((8.05, 13.3)).left().length(0.45)
    d += elm.Line().at((10.15, 13.3)).right().length(0.45)
    d += elm.Line().at((9.1, 12.3)).down().length(0.7)
    d += elm.Ground().at((9.1, 11.6))

    d += elm.Vdd().at((10.9, 13.9)).label('+5 V')
    d += elm.Line().at((10.9, 13.9)).down().length(0.6)
    d += elm.Dot().at((10.9, 13.3))
    d += elm.Line().at((10.9, 13.3)).left().length(0.3)
    d += elm.Capacitor().at((10.9, 13.3)).down().length(1.7)
    lab(d, 11.15, 12.5, 'C2\n10 µF', 'left', 7.5)
    d += elm.Ground().at((10.9, 11.6))
    d += elm.Dot().at((11.9, 13.3))
    d += elm.Capacitor().at((11.9, 13.3)).down().length(1.7)
    lab(d, 12.15, 12.5, 'C3\n100 nF', 'left', 7.5)
    d += elm.Ground().at((11.9, 11.6))
    d += elm.Line().at((11.9, 13.3)).left().length(1.0)

    # ================= MCU (manual rectangle) =================
    d += elm.Line().at((15.0, 4.5)).right().length(4.0)
    d += elm.Line().at((19.0, 4.5)).up().length(5.2)
    d += elm.Line().at((19.0, 9.7)).left().length(4.0)
    d += elm.Line().at((15.0, 9.7)).down().length(5.2)
    lab(d, 17.0, 4.1, 'U2  ATtiny85-20PU', 'center', 8)

    left_pins = [('VCC', '8', 9.0), ('RESET', '1', 7.8), ('PB3', '2', 6.6), ('PB4', '3', 5.4)]
    right_pins = [('GND', '4', 9.0), ('PB2', '7', 7.8), ('PB1', '6', 6.6), ('PB0', '5', 5.4)]
    for name, num, y in left_pins:
        d += elm.Line().at((15.0, y)).left().length(1.0)
        lab(d, 15.25, y, name, 'left', 8)
        lab(d, 14.75, y + 0.22, num, 'right', 7)
    for name, num, y in right_pins:
        d += elm.Line().at((19.0, y)).right().length(1.0)
        lab(d, 18.75, y, name, 'right', 8)
        lab(d, 19.25, y + 0.22, num, 'left', 7)

    # VCC -> +5V
    d += elm.Line().at((14.0, 9.0)).up().length(1.0)
    d += elm.Vdd().at((14.0, 10.0)).label('+5 V')

    # RESET pull-up + ISP flag
    d += elm.Line().at((14.0, 7.8)).left().length(1.7)
    d += elm.Dot().at((12.3, 7.8))
    d += elm.Resistor().at((12.3, 7.8)).up().length(1.6)
    lab(d, 11.75, 8.55, 'R13\n10 kΩ', 'right', 7.5)
    d += elm.Vdd().at((12.3, 9.4)).label('+5 V')
    d += elm.Line().at((12.3, 7.8)).left().length(0.7)
    lab(d, 11.4, 7.8, 'RST → ISP', 'right', 8, '#1a4f8a')

    # PB3 -> NTC_TR
    d += elm.Line().at((14.0, 6.6)).left().length(1.7)
    lab(d, 12.1, 6.6, 'NTC_TR', 'right', 8, '#1a4f8a')

    # PB4 -> LED2 fault
    d += elm.Line().at((14.0, 5.4)).left().length(1.7)
    d += elm.Dot().at((12.3, 5.4))
    d += elm.Resistor().at((12.3, 5.4)).down().length(1.4)
    lab(d, 12.0, 4.7, 'R9\n1 kΩ', 'right', 7.5)
    d += elm.LED().at((12.3, 4.0)).down().length(1.4)
    lab(d, 12.0, 3.3, 'LED2\n故障', 'right', 7.5)
    d += elm.Ground().at((12.3, 2.6))

    # GND route
    d += elm.Line().at((20.0, 9.0)).right().length(0.6)
    d += elm.Line().at((20.6, 9.0)).up().length(1.0)
    d += elm.Line().at((20.6, 10.0)).right().length(1.8)
    d += elm.Line().at((22.4, 10.0)).down().length(3.8)
    d += elm.Ground().at((22.4, 6.2))

    # C4 decoupling near VCC/GND
    d += elm.Vdd().at((13.3, 9.6)).label('+5 V')
    d += elm.Capacitor().at((13.3, 9.6)).down().length(1.3)
    lab(d, 13.55, 8.9, 'C4\n100 nF', 'left', 7.5)
    d += elm.Ground().at((13.3, 8.3))

    # PB0 -> LED1 run
    d += elm.Line().at((20.0, 5.4)).right().length(1.0)
    d += elm.Dot().at((21.0, 5.4))
    d += elm.Resistor().at((21.0, 5.4)).down().length(1.4)
    lab(d, 21.3, 7.1, 'R7\n1 kΩ', 'left', 7.5)
    d += elm.LED().at((21.0, 4.0)).down().length(1.4)
    lab(d, 21.3, 5.7, 'LED1\n运行', 'left', 7.5)
    d += elm.Ground().at((21.0, 2.6))

    # PB1 / PB2 nets
    d += elm.Line().at((20.0, 6.6)).right().length(1.0)
    lab(d, 21.1, 6.6, 'PWM', 'left', 8, '#1a4f8a')
    d += elm.Line().at((20.0, 7.8)).right().length(1.0)
    lab(d, 21.1, 7.8, 'NTC_HS', 'left', 8, '#1a4f8a')

    # notes
    lab(d, 1.5, 1.6, '注 1：U1 输入串 R17 降压，降低 78L05 在 24 V 下的功耗；C1 兼作输入储能。', 'left', 8)
    lab(d, 1.5, 1.1, '注 2：ISP 接线：MOSI=PB0，MISO=PB1，SCK=PB2，RST=PB5；编程时建议拔掉风扇。', 'left', 8)
    lab(d, 1.5, 0.6, '注 3：C4 必须紧靠 U2 的 VCC/GND 引脚；NTC 走线远离 220 V 与继电器。', 'left', 8)

svg_path = os.path.join(OUT, "fan-sch-power-mcu.svg")
with open(svg_path, encoding="utf-8") as f:
    svg = f.read()
svg = re.sub(r'font-family="[^"]*"', f'font-family="{FONT}"', svg)
with open(svg_path, "w", encoding="utf-8") as f:
    f.write(svg)

print('sheet1 ok')

