# 图纸与 PDF 生成脚本

这些脚本用于从源码重新生成 SVG、PNG 预览和合并 PDF。日常使用不需要它们；只有修改图纸/文档时才需要。

## 依赖

- Python 3.10+
- [schemdraw](https://schemdraw.readthedocs.io/)（原理图）
- [cairosvg](https://cairosvg.org/)（SVG → PNG，需要系统 cairo）
- [markdown](https://python-markdown.github.io/)（合并 PDF）
- 中文字体：macOS 用 PingFang SC / Arial Unicode MS；Linux 建议安装 **Noto Sans CJK SC**；Windows 用微软雅黑/思源黑体。

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r tools/requirements.txt
# macOS 如 cairosvg 报错：brew install cairo
```

## 生成

在仓库根目录执行：

```bash
python tools/make_sch1.py          # 风扇：电源 + MCU
python tools/make_sch2.py          # 风扇：NTC + 输出
python tools/make_wiring.py        # 机内接线
python tools/make_knob.py          # 旋钮接线/安装
python tools/make_block.py         # 系统框图
python tools/render_previews.py    # 全部 SVG -> hardware/previews/*.png
python tools/build_pdf.py          # docs/utp3315tfl-ii-modification-guide.pdf
```

PDF 由无头 Chrome 打印。脚本默认使用 macOS 路径；其他系统请设置环境变量：

```bash
export CHROME="/usr/bin/google-chrome"   # Linux
# 或 "C:/Program Files/Google/Chrome/Application/chrome.exe"（Windows）
python tools/build_pdf.py
```

## 约定

- 所有脚本从仓库根目录运行，输出到 `hardware/` 与 `docs/`。
- SVG 内的中文字体统一为：`Arial Unicode MS, PingFang SC, Noto Sans CJK SC, Heiti SC, sans-serif`。
- 生成的 PNG 只用于预览，不要手工改；改图请改脚本。
- 不要把 `build/`、`.venv/` 提交到仓库。
