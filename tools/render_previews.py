#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把 hardware/*.svg 渲染为 hardware/previews/*.png，并修正中文字体。

用法：
    python tools/render_previews.py
"""
import os
import re
import sys

try:
    import cairosvg
except ImportError:
    sys.exit("缺少 cairosvg：pip install -r tools/requirements.txt")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HW = os.path.join(ROOT, "hardware")
PREVIEWS = os.path.join(HW, "previews")
FONT = "Arial Unicode MS, PingFang SC, Noto Sans CJK SC, Heiti SC, sans-serif"

SVGS = [
    "system-block.svg",
    "fan-sch-power-mcu.svg",
    "fan-sch-ntc-output.svg",
    "fan-wiring.svg",
    "knob-wiring.svg",
]


def fix_font(path: str) -> None:
    """把 SVG 的 font-family 统一成跨平台中文字体栈。"""
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    new = re.sub(r'font-family="[^"]*"', f'font-family="{FONT}"', text)
    if new != text:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new)


def main() -> None:
    os.makedirs(PREVIEWS, exist_ok=True)
    for name in SVGS:
        svg = os.path.join(HW, name)
        if not os.path.exists(svg):
            print(f"[skip] {name} 不存在")
            continue
        fix_font(svg)
        png = os.path.join(PREVIEWS, name.replace(".svg", ".png"))
        cairosvg.svg2png(url=svg, write_to=png, scale=2.0)
        print(f"[ok] {name} -> previews/{os.path.basename(png)} ({os.path.getsize(png)} bytes)")


if __name__ == "__main__":
    main()
