/*
 * FAN-CTRL-24V  —  UNI-T UTP3315TFL-II 温控风扇
 * ------------------------------------------------------------
 * MCU : ATtiny85-20PU, 8 MHz internal RC, BOD 2.7 V
 * PWM : PB1 / OC0B, fast PWM 8-bit, 8 MHz / 256 = 31.25 kHz
 * NTC : PB2 = ADC2 (heatsink), PB3 = ADC3 (transformer, optional)
 * LED : PB0 = run, PB4 = fault
 *
 * 依赖：Arduino IDE + ATTinyCore
 *   Board   : ATtiny25/45/85
 *   Chip    : ATtiny85
 *   Clock   : 8 MHz (internal)
 *   BOD     : 2.7 V
 *
 * 烧录前先 Burn Bootloader 设置 8 MHz 熔丝；否则 PWM 只有 3.9 kHz，会啸叫。
 *
 * 曲线：T <= 30C -> 25%；30..55C 线性升到 100%；>=55C 全速。
 * 失效：NTC 开路/短路 -> 全速；双 NTC 取较高温度。
 */

#include <Arduino.h>
#include <math.h>
#include <avr/wdt.h>
#include <util/delay.h>

/* ---------------- 引脚 ---------------- */
#define PIN_LED_RUN  0     /* PB0 */
#define PIN_PWM      1     /* PB1 / OC0B */
#define PIN_NTC_HS   2     /* PB2 / ADC2 */
#define PIN_NTC_TR   3     /* PB3 / ADC3 */
#define PIN_LED_ERR  4     /* PB4 */

/* ---------------- 可调参数 ---------------- */
static const float NTC_R0   = 10000.0f;  /* NTC 25C 标称 10k */
static const float NTC_B    = 3950.0f;   /* B 值 */
static const float NTC_T0   = 298.15f;   /* 25C, K */
static const float R_FIXED  = 10000.0f;  /* 下拉电阻 10k */

static const float T_START  = 30.0f;     /* 开始升速，C */
static const float T_FULL   = 55.0f;     /* 全速，C */
static const uint8_t DUTY_MIN = 64;      /* 25% of 24V = 6V；12V 风扇建议 96 */
static const uint8_t DUTY_MAX = 255;     /* 100% */

static const uint16_t KICK_MS = 800;     /* 上电全速启动时间 */
static const uint8_t  SLEW_STEP = 2;     /* 每 6ms 改变的占空比级数 */
static const uint8_t  SLEW_MS = 6;       /* 主循环周期 */

/* ---------------- 状态 ---------------- */
static uint8_t  duty = 0;
static uint8_t  target = DUTY_MIN;
static bool     fault = false;
static uint16_t blink_cnt = 0;
static bool     blink_state = false;

/* ---------------- NTC ---------------- */
static float readTemp(uint8_t ch) {
  int adc = analogRead(ch);                 /* 0..1023, Vcc 参考 */
  if (adc >= 1015 || adc <= 8) return NAN;  /* 开路 / 短路 */
  float v = (float)adc * (5.0f / 1023.0f);
  /* NTC 在上、10k 在下：V = 5 * Rfixed / (Rntc + Rfixed) */
  float r = R_FIXED * (5.0f - v) / v;
  float t = 1.0f / (1.0f / NTC_T0 + log(r / NTC_R0) / NTC_B) - 273.15f;
  if (t < -20.0f || t > 150.0f) return NAN;
  return t;
}

/* ---------------- 初始化 ---------------- */
void setup() {
  pinMode(PIN_PWM, OUTPUT);
  pinMode(PIN_LED_RUN, OUTPUT);
  pinMode(PIN_LED_ERR, OUTPUT);
  digitalWrite(PIN_LED_RUN, LOW);
  digitalWrite(PIN_LED_ERR, LOW);

  /* Timer0: fast PWM, 8-bit, no prescale, OC0B non-inverting */
  TCCR0A = _BV(COM0B1) | _BV(WGM01) | _BV(WGM00);
  TCCR0B = _BV(CS00);
  TIMSK0 &= ~_BV(TOIE0);   /* 关掉 Arduino millis() 的溢出中断，31 kHz 下没必要 */
  OCR0B = 0;

  /* ADC: Vcc 参考，/128（analogRead 会再配置，这里只做初始） */
  ADMUX  = _BV(REFS0);
  ADCSRA = _BV(ADEN) | _BV(ADPS2) | _BV(ADPS1) | _BV(ADPS0);

  wdt_enable(WDTO_1S);
  wdt_reset();

  /* 上电先全速踢一脚，帮风扇克服静摩擦 */
  OCR0B = DUTY_MAX;
  _delay_ms(KICK_MS);

  duty = DUTY_MIN;
  OCR0B = duty;
  wdt_reset();
}

/* ---------------- 主循环 ---------------- */
void loop() {
  wdt_reset();

  float t1 = readTemp(PIN_NTC_HS);
  float t2 = readTemp(PIN_NTC_TR);
  bool f1 = isnan(t1);
  bool f2 = isnan(t2);
  float t = 25.0f;

  if (f1 && f2) {
    /* 两路都失效：全速，故障灯闪 */
    fault = true;
    target = DUTY_MAX;
  } else {
    fault = false;
    if (f1)      t = t2;
    else if (f2) t = t1;
    else         t = (t1 > t2) ? t1 : t2;

    if (t <= T_START) {
      target = DUTY_MIN;
    } else if (t >= T_FULL) {
      target = DUTY_MAX;
    } else {
      float k = (t - T_START) / (T_FULL - T_START);
      target = DUTY_MIN + (uint8_t)(k * (float)(DUTY_MAX - DUTY_MIN));
    }
  }

  /* 限速升降，避免风扇“打嗝” */
  if (duty < target) {
    duty = (target - duty > SLEW_STEP) ? (duty + SLEW_STEP) : target;
  } else if (duty > target) {
    duty = (duty - target > SLEW_STEP) ? (duty - SLEW_STEP) : target;
  }
  OCR0B = duty;

  digitalWrite(PIN_LED_RUN, (duty > 0) ? HIGH : LOW);

  /* 故障灯：NTC 故障闪 2 Hz；过温常亮 */
  if (fault) {
    if (++blink_cnt >= 80) {          /* 80 * 6 ms ≈ 0.5 s */
      blink_cnt = 0;
      blink_state = !blink_state;
      digitalWrite(PIN_LED_ERR, blink_state ? HIGH : LOW);
    }
  } else {
    blink_cnt = 0;
    blink_state = false;
    digitalWrite(PIN_LED_ERR, (t > 68.0f) ? HIGH : LOW);
  }

  _delay_ms(SLEW_MS);
}
