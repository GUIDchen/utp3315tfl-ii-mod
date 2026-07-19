# 硬件图纸与 BOM

## 文件

| 文件 | 内容 |
|---|---|
| [system-block.svg](system-block.svg) / [png](previews/system-block.png) | 整机功率/控制链路与两处改造点 |
| [fan-sch-power-mcu.svg](fan-sch-power-mcu.svg) / [png](previews/fan-sch-power-mcu.png) | 风扇控制器：24 V 输入、78L05、ATtiny85、LED、ISP |
| [fan-sch-ntc-output.svg](fan-sch-ntc-output.svg) / [png](previews/fan-sch-ntc-output.png) | 风扇控制器：双 NTC 分压、Q1 低边 PWM、C8/D2、J2 |
| [fan-wiring.svg](fan-wiring.svg) / [png](previews/fan-wiring.png) | 机内接线：原风扇插座、J1/J2、NTC1/NTC2 |
| [knob-wiring.svg](knob-wiring.svg) / [png](previews/knob-wiring.png) | 10 圈电位器接线、面板开孔、安装剖面 |
| [bom.csv](bom.csv) | 可导入表格的 BOM（UTF-8 with BOM） |

SVG 为矢量原图，适合放大/打印；PNG 为 2× 预览，方便手机/Issue 里查看。

## 连接器定义

### J1：24 V 输入（2P，5.08 mm）

| 脚 | 定义 | 来源 |
|---|---|---|
| 1 | +24 V | 原风扇插座 1 脚 |
| 2 | GND | 原风扇插座 2 脚 |

### J2：风扇输出（3P，XH2.54）

| 脚 | 定义 | 接到 |
|---|---|---|
| 1 | +24 V | 风扇红线 |
| 2 | FAN−（Q1 漏极，开关地） | 风扇黑线 |
| 3 | TACH（不用） | 风扇黄线，悬空热缩 |

> 若原机主板对测速线有检测，把风扇黄线直接回主板原针脚，不接控制器。

### J3 / J4：NTC（2P，XH2.54）

| 脚 | 定义 |
|---|---|
| 1 | +5 V |
| 2 | NTC 分压节点（到 PB2/PB3） |

### J5：ISP（2×3，2.54 mm）

| 脚 | 定义 |
|---|---|
| 1 | MISO（PB1） |
| 2 | VCC（+5 V） |
| 3 | SCK（PB2） |
| 4 | MOSI（PB0） |
| 5 | RESET（PB5） |
| 6 | GND |

## 关键参数

| 参数 | 值 | 备注 |
|---|---|---|
| 输入 | 24 V（12–28 V 可工作） | 实测原风扇插座 |
| 风扇 | 80 mm / 24 V / ≤0.2 A / 3 线 | 12 V 风扇需改 DUTY_MIN |
| PWM | 31.25 kHz，8 位 | ATtiny85 8 MHz / 256 |
| 温度曲线 | 30 ℃ 25% → 55 ℃ 100% | 可改固件常量 |
| 最小占空比 | 25%（约 6 V） | 12 V 风扇建议 37.5% |
| NTC | 10 kΩ B3950，1% | 上拉 NTC、下拉 10 kΩ |
| 保护 | F1 0.5 A、D1 反接、D2 续流、NTC 故障全速 | 可选 KSD9700 70 ℃ |

## 注意

- 图纸中的元件值按“常见批次”设计；风扇电压、电位器阻值、面板尺寸必须实测。
- 散热器可能带电压；NTC 固定前先测对地电压。
- 详细施工与验收见 [../docs/05-build-and-test.md](../docs/05-build-and-test.md)。
