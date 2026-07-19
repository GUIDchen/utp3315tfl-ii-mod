# Changelog

本项目遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/) 与 [语义化版本](https://semver.org/lang/zh-CN/)。

## [1.0.0] - 2026-07-19

### Added

- 整机调研：UTP3315TFL-II 规格、内部构造、功率链路、CV/CC 拓扑推断。
- 风扇温控方案：ATtiny85 + 双 NTC + 31.25 kHz PWM + 失效安全。
- 旋钮精度方案：同阻值 10 圈电位器替换 V-COARSE，含机械安装与校准。
- 原理图、机内接线图、旋钮接线图、系统框图（SVG + PNG）。
- BOM（Markdown + CSV），含参考价、渠道、替代料。
- ATtiny85 固件与烧录说明。
- 施工、调试、验收与故障排查文档。
- 44 页完整 PDF（含安全须知、项目介绍、调研、方案、BOM、施工验收、附录、固件说明）。

### Known limitations

- 尚未汇总整机实测数据；曲线、温度、纹波为设计目标/验收方法。
- 风扇尺寸存在资料冲突（文章写 12 cm，照片与机箱比例判断为 80 mm）；施工前必须实测。
- 未提供 PCB 文件；当前为万用板方案。
