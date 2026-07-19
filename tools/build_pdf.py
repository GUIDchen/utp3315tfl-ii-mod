#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把 Markdown 文档合并为一份 A4 PDF。

依赖：markdown、Google Chrome / Chromium。
用法：
    python tools/build_pdf.py
可用环境变量 CHROME 指定浏览器路径。
"""
import html
import os
import re
import shutil
import subprocess
import sys

import markdown

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

DOCS = [
    ("doc-safety", "SAFETY.md", "安全须知"),
    ("doc-intro", "docs/00-introduction.md", "项目介绍"),
    ("doc-readme", "README.md", "总览"),
    ("doc-01", "docs/01-research.md", "整机调研与电路分析"),
    ("doc-02", "docs/02-fan-mod.md", "风扇温控改造"),
    ("doc-03", "docs/03-knob-mod.md", "旋钮精度改造"),
    ("doc-04", "docs/04-bom.md", "物料清单"),
    ("doc-05", "docs/05-build-and-test.md", "施工、调试与验收"),
    ("doc-06", "docs/06-appendix.md", "附录"),
    ("doc-fw", "firmware/README.md", "固件说明"),
]

LINK_MAP = {
    "docs/00-introduction.md": "#doc-intro",
    "docs/01-research.md": "#doc-01",
    "docs/02-fan-mod.md": "#doc-02",
    "docs/03-knob-mod.md": "#doc-03",
    "docs/04-bom.md": "#doc-04",
    "docs/05-build-and-test.md": "#doc-05",
    "docs/06-appendix.md": "#doc-06",
    "../docs/05-build-and-test.md": "#doc-05",
    "03-knob-mod.md": "#doc-03",
    "04-bom.md": "#doc-04",
    "05-build-and-test.md": "#doc-05",
    "06-appendix.md": "#doc-06",
    "02-fan-mod.md": "#doc-02",
    "01-research.md": "#doc-01",
    "SAFETY.md": "#doc-safety",
    "firmware/README.md": "#doc-fw",
    "../hardware/bom.csv": "hardware/bom.csv",
}


def preprocess(text: str) -> str:
    """去掉 GitHub 专用的居中 div、徽章和 callout 标记，PDF 里看起来更干净。"""
    text = text.replace('<div align="center">', "").replace("</div>", "")
    text = re.sub(r"\[!\[[^\]]*\]\(https://img\.shields\.io[^\)]*\)\]\([^\)]*\)", "", text)
    text = text.replace("> [!WARNING]", "> **警告：**")
    return text


def convert(text: str) -> str:
    text = text.replace("](../hardware/", "](hardware/").replace("](../firmware/", "](firmware/")
    for key, value in LINK_MAP.items():
        text = text.replace("](" + key + ")", "](" + value + ")")
    md = markdown.Markdown(extensions=["tables", "fenced_code", "sane_lists", "toc"])
    return md.convert(text)


sections = []
for sid, path, title in DOCS:
    raw = open(path, encoding="utf-8").read()
    raw = preprocess(raw)
    raw = re.sub(r"^# .*?\n", "", raw, count=1)
    body = convert(raw)
    sections.append(f'<section id="{sid}" class="doc"><h1>{html.escape(title)}</h1>\n{body}</section>')

cover = '''
<div class="cover">
  <div class="kicker">UNI-T · UTP3315TFL-II</div>
  <h1 class="title">温控风扇与高精度电压旋钮改造</h1>
  <div class="subtitle">调研 · 方案对比 · 物料清单 · 接线原理图 · 固件 · 验收</div>
  <img src="hardware/previews/system-block.png" alt="系统框图">
  <div class="meta">版本 v1.0 &nbsp;·&nbsp; 2026-07 &nbsp;·&nbsp; 适用于 0–30 V / 0–5 A 单路线性机型</div>
  <div class="warn">机内有 220 V 市电与高压电容。断电放电后再施工；改造会失去保修。</div>
</div>
'''

css = '''
@page { size: A4; margin: 17mm 15mm 18mm 15mm; }
* { box-sizing: border-box; }
body { font-family: "PingFang SC","Arial Unicode MS","Noto Sans CJK SC","Heiti SC",sans-serif; font-size: 10.2pt; line-height: 1.62; color:#1c1c1c; }
.cover { height: 250mm; text-align:center; padding-top: 28mm; page-break-after: always; }
.cover .kicker { font-size: 13pt; letter-spacing: 2px; color:#2a5f9a; margin-bottom: 10mm; }
.cover h1.title { font-size: 30pt; line-height:1.25; border:none; page-break-before: avoid; margin: 0 0 6mm 0; color:#111; }
.cover .subtitle { font-size: 12pt; color:#555; margin-bottom: 14mm; }
.cover img { width: 88%; border:1px solid #ddd; border-radius: 6px; }
.cover .meta { margin-top: 12mm; color:#666; font-size: 10pt; }
.cover .warn { margin-top: 12mm; color:#a00; font-size: 9.5pt; border:1px solid #e0b4b4; background:#fff5f5; padding: 4mm; border-radius: 4px; }
section.doc { page-break-before: always; }
section.doc > h1 { font-size: 20pt; color:#111; border-bottom: 3px solid #2a5f9a; padding-bottom: 3mm; margin: 0 0 6mm 0; }
h2 { font-size: 14pt; color:#1d4670; margin: 7mm 0 2.5mm; border-bottom: 1px solid #dde3ea; padding-bottom: 1mm; }
h3 { font-size: 11.6pt; color:#222; margin: 5mm 0 2mm; }
p { margin: 2mm 0; }
ul, ol { margin: 2mm 0 2mm 5mm; padding-left: 4mm; }
li { margin: 1mm 0; }
table { border-collapse: collapse; width: 100%; margin: 3mm 0 4mm; font-size: 8.8pt; page-break-inside: avoid; }
th, td { border: 1px solid #c9d0d8; padding: 3px 5px; vertical-align: top; }
th { background: #eef2f7; color:#1d4670; font-weight: 600; }
tr:nth-child(even) td { background: #fafbfc; }
img { max-width: 100%; height: auto; display:block; margin: 3mm auto; border:1px solid #e2e2e2; border-radius: 4px; }
pre { background:#f6f8fa; border:1px solid #e3e6ea; border-radius:4px; padding: 3mm; font-size: 8.2pt; line-height:1.45; white-space: pre-wrap; word-break: break-all; page-break-inside: avoid; }
code { font-family: Menlo, Consolas, monospace; font-size: 8.6pt; background:#f2f4f7; padding: 0 1px; border-radius: 2px; }
pre code { background: none; padding:0; }
blockquote { border-left: 4px solid #c9d0d8; margin: 3mm 0; padding: 1mm 4mm; color:#555; background:#fafbfc; }
hr { border:none; border-top:1px solid #ddd; margin: 5mm 0; }
a { color:#1d4670; text-decoration: none; }
'''

html_doc = f'''<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8">
<base href="file://{ROOT}/">
<title>UTP3315TFL-II 改造方案</title>
<style>{css}</style></head>
<body>
{cover}
{''.join(sections)}
</body></html>'''

os.makedirs("build", exist_ok=True)
html_path = os.path.join("build", "combined.html")
with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_doc)

candidates = [
    os.environ.get("CHROME", ""),
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    shutil.which("google-chrome") or "",
    shutil.which("chromium") or "",
    shutil.which("chromium-browser") or "",
]
chrome = next((c for c in candidates if c and os.path.exists(c)), None)
if not chrome:
    sys.exit("未找到 Chrome/Chromium；请设置环境变量 CHROME=/path/to/chrome")

pdf = os.path.join("docs", "utp3315tfl-ii-modification-guide.pdf")
cmd = [
    chrome, "--headless", "--disable-gpu", "--no-sandbox",
    "--allow-file-access-from-files", "--virtual-time-budget=15000",
    f"--print-to-pdf={os.path.abspath(pdf)}", "--no-pdf-header-footer",
    "file://" + os.path.abspath(html_path),
]
print("Chrome:", chrome)
subprocess.run(cmd, check=True)
print("PDF:", pdf, os.path.getsize(pdf), "bytes")
