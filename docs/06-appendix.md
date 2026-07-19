# 06 · 附录：参数、引脚与参考

## A. NTC 分压速查

条件：10 kΩ NTC（B=3950，25 ℃ 标称），上拉 NTC、下拉 10 kΩ 1 %，5.0 V 供电。

| 温度 ℃ | R_NTC kΩ | V_ADC V | ADC 码（10 位） |
|---|---|---|---|
| 20 | 12.49 | 2.22 | 454 |
| 25 | 10.00 | 2.50 | 512 |
| 30 | 8.04 | 2.77 | 567 |
| 35 | 6.56 | 3.01 | 616 |
| 40 | 5.32 | 3.26 | 668 |
| 45 | 4.36 | 3.48 | 713 |
| 50 | 3.60 | 3.68 | 753 |
| 55 | 2.99 | 3.84 | 787 |
| 60 | 2.49 | 4.00 | 820 |
| 65 | 2.09 | 4.13 | 847 |
| 70 | 1.76 | 4.25 | 871 |

固件用 Beta 公式：

**T = 1 / (1/T0 + (1/B) × ln(R/R0)) − 273.15**

其中 R = R_fixed × (5 − V) / V。

## B. ATtiny85 DIP-8 引脚

| 引脚 | 名称 | 本方案用途 | 备注 |
|---|---|---|---|
| 1 | PB5 / RESET | ISP RESET | 10 kΩ 上拉（内部也有） |
| 2 | PB3 | NTC_TR / ADC3 | 可选 |
| 3 | PB4 | 故障 LED | 低电平点亮？本方案高电平点亮 |
| 4 | GND | 地 |  |
| 5 | PB0 | 运行 LED / MOSI | 烧录时 LED 会闪 |
| 6 | PB1 | PWM / MISO | OC0B，31.25 kHz |
| 7 | PB2 | NTC_HS / ADC2 / SCK | 烧录时被 10 kΩ 加载 |
| 8 | VCC | +5 V | 100 nF 就近去耦 |

> 注意：ATtiny85 的 ADC 通道是 ADC0=PB0、ADC1=PB1、ADC2=PB2、ADC3=PB3。本方案 NTC 接 PB2/PB3，对应 Arduino 的 `A2`/`A3`，不是 `A1`。

## C. 其他器件引脚

### 78L05（TO-92）

面对印字面、引脚朝下，常见顺序为 **OUT / GND / IN**（不同厂家可能不同）。以数据手册/实测为准；本方案在原理图上标的是 IN/OUT/GND 名称，不依赖引脚号。

### AO3400A（SOT-23）

| 引脚 | 功能 |
|---|---|
| 1 | Gate |
| 2 | Source |
| 3 | Drain |

### SS34（SMA）

| 端 | 功能 |
|---|---|
| 无条纹 | 阳极 |
| 条纹 | 阴极 |

### XH2.54 3P（风扇）

本方案定义：**1=+24 V，2=FAN−，3=TACH**。不同批次风扇插头顺序可能不同，务必按实物线色与万用表确认。

## D. 固件关键参数

文件：[firmware/fan_ctrl_attiny85.ino](../firmware/fan_ctrl_attiny85.ino)

| 常量 | 默认 | 说明 |
|---|---|---|
| `T_START` | 30.0 | 开始升速温度 |
| `T_FULL` | 55.0 | 全速温度 |
| `DUTY_MIN` | 64 | 25 %；12 V 风扇建议 96 |
| `DUTY_MAX` | 255 | 100 % |
| `KICK_MS` | 800 | 上电全速启动时间 |
| `SLEW_MS` | 6 | 每级占空比步进时间 |
| `NTC_B` | 3950 | NTC B 值 |
| `R_FIXED` | 10000 | 下拉电阻 |

## E. 熔丝/时钟

- ATtiny85 出厂为 1 MHz 内部 RC；必须改为 **8 MHz internal**，否则 PWM 频率只有 3.9 kHz（可闻）。
- 用 ATTinyCore 的 Burn Bootloader 设置：
  - Clock: 8 MHz (internal)
  - BOD: 2.7 V
  - EESAVE: 可选
- 不需要外部晶振。

## F. 参考来源

1. UNI-T UTP3315TFL-II 产品页：<https://uni-trendus.com/products/utp3315tfl-ii>
2. UNI-T UTP3313TFL-II/UTP3315TFL-II 说明书：<https://en.sekorm.com/doc/2558379.html>
3. ph0en1x.net：拆机、变压器、继电器、D1047、24 V 风扇、6 V 静音实测：<https://ph0en1x.net/118-regulated-power-supply-uni-t-utp3315tfl-ii-review-and-mod.html>
4. Electronics Repair School 评测：<https://forum.sorinelectronics.com/index.php?topic=2003.0>
5. 迅维网：电压电位器 1 kΩ 维修记录：<https://www.chinafix.com/forum.php?mod=viewthread&action=printable&tid=1280263>
6. 迅维网：碳膜电位器寿命讨论：<https://www.chinafix.com/forum.php?mod=viewthread&action=printable&tid=1113045>
7. elektroda：同型风扇降噪/显示校正讨论（波兰语）：<https://www.elektroda.pl/rtvforum/topic3657843.html>

## G. 版本记录

| 版本 | 日期 | 说明 |
|---|---|---|
| v1.0 | 2026-07 | 初版：调研、风扇温控、10 圈电位器、BOM、接线图、固件 |

## H. 待实测/待补充

- [ ] 实物风扇电压/电流/针序
- [ ] V-COARSE 实际阻值（1 kΩ 还是 10 kΩ）
- [ ] 面板开孔与 PCB 间距
- [ ] 满载散热器/变压器温度曲线
- [ ] 改造前后输出纹波对比
- [ ] 10 圈电位器实际安装照片
