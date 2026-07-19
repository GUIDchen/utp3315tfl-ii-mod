# FAN-CTRL-24V 固件说明

## 1. 文件

- `fan_ctrl_attiny85.ino`：主程序，ATtiny85，8 MHz 内部时钟。

## 2. 开发板设置（Arduino IDE + ATTinyCore）

1. 安装 ATTinyCore：
   - 首选项 → 附加开发板管理器网址：
     `http://drazzy.com/package_drazzy.com_index.json`
   - 开发板管理器搜索 “ATtinyCore” 并安装。
2. 选择：
   - Board: **ATtiny25/45/85**
   - Chip: **ATtiny85**
   - Clock: **8 MHz (internal)**
   - BOD: **2.7 V**
   - Programmer: **USBasp** 或 **Arduino as ISP**
3. **先 Burn Bootloader**（设置熔丝，把出厂 1 MHz 改成 8 MHz），再 Upload。

> 不 Burn Bootloader 直接上传，芯片仍按 1 MHz 运行：PWM 只有 3.9 kHz，会听到啸叫，NTC 采样也变慢。

## 3. ISP 接线

| ISP 6 针 | ATtiny85 |
|---|---|
| MISO | PB1（6 脚） |
| VCC | 8 脚 |
| SCK | PB2（7 脚） |
| MOSI | PB0（5 脚） |
| RESET | PB5（1 脚） |
| GND | 4 脚 |

PB2 上有 NTC 分压（10 kΩ 到 2.5 V），通常不影响；若烧录失败，临时拔掉 NTC1 或 R1。

## 4. 可调参数

在文件顶部：

| 常量 | 默认 | 说明 |
|---|---|---|
| `T_START` | 30.0 | 开始升速温度（℃） |
| `T_FULL` | 55.0 | 全速温度（℃） |
| `DUTY_MIN` | 64 | 最小占空比（0–255）；64=25% |
| `DUTY_MAX` | 255 | 最大占空比 |
| `KICK_MS` | 800 | 上电全速时间（ms） |
| `SLEW_STEP` | 2 | 每 6 ms 改变多少级 |
| `NTC_B` | 3950 | NTC B 值 |
| `R_FIXED` | 10000 | 下拉电阻 |

### 12 V 风扇

若实测风扇是 12 V，把 `DUTY_MIN` 改为 **96**（37.5%，约 4.5 V），否则低温时可能不启动。

### 曲线更激进/更保守

- 想更安静：`T_FULL` 改 60，或 `DUTY_MIN` 改 48（18.75%）。
- 想更凉快：`T_START` 改 28，`T_FULL` 改 50。

改完重新烧录，按 [../docs/05-build-and-test.md](../docs/05-build-and-test.md) 记录温度—电压表。

## 5. 上电自检

1. 运行 LED（PB0）常亮。
2. 上电前 0.8 s 风扇全速（启动踢一脚），随后降到当前温度对应转速。
3. 手捏 NTC1：几秒内升速。
4. 拔掉 NTC1：全速，故障 LED 2 Hz 闪烁。
5. 短接 NTC1：全速，故障 LED 闪烁。
6. 温度 >68 ℃：故障 LED 常亮（不改变风扇全速）。

## 6. 常见问题

| 现象 | 原因 | 处理 |
|---|---|---|
| PWM 有啸叫 | 熔丝仍是 1 MHz（3.9 kHz） | Burn Bootloader 设 8 MHz |
| 风扇不转 | DUTY_MIN 太低、Q1 坏、24 V 未到 | 临时把 DUTY_MIN 改 128；测 J2 |
| 常全速 | NTC 开路/短路、ADC 脚虚焊 | 测 PB2/PB3 电压；补焊 |
| 转速跳变 | NTC 接触不良、电源纹波 | 固定 NTC；加 100 nF |
| 烧录失败 | SCK 被 NTC 加载、线序错 | 拔 NTC1；核对 ISP 线 |

## 7. 代码结构

- `readTemp()`：ADC → 电压 → NTC 电阻 → Beta 公式 → ℃；异常返回 `NAN`。
- `loop()`：双 NTC 取最大温度 → 分段线性 → 限速 → `OCR0B`。
- 看门狗 1 s；主循环 6 ms，正常不会复位。
- 不使用 `millis()`/`analogWrite()`，因为 Timer0 已被改成 31.25 kHz。
