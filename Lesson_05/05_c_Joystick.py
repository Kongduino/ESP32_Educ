from machine import Pin, ADC, I2C
import time
from freesans9 import FreeSans9Defs

i2c = machine.I2C(0, scl=5, sda=4, freq=400000, timeout=50000)
devices = i2c.scan()
display = None

if devices.count(0x3c) == 0:
    print("No SSD1306!")
    sys.exit()
else:
    from ssd1306 import SSD1306_I2C
    display = SSD1306_I2C(128, 64, i2c)

def leftArrow():
    py = 40
    display.fill_rect(10, py, 22, 8, 1)
    for i in range (0, 10):
        display.line(i, py + 4, 10, py + 12 - i, 1)
        display.line(i, py + 4, 10, py - 4 + i, 1)
    display.show()

def rightArrow():
    py = 40
    display.fill_rect(128 - 10 - 22, py, 128 - 10, 8, 1)
    for i in range (0, 10):
        display.line(128 - i, py + 4, 118, py + 12 - i, 1)
        display.line(128 - i, py + 4, 118, py - 4 + i, 1)
    display.show()

def upArrow():
    px = 64
    display.fill_rect(px - 4, 10, 8, 22, 1)
    for i in range (0, 10):
        display.line(px + i, i, px + i, 10, 1)
        display.line(px - i, i, px - i, 10, 1)
    display.show()

def downArrow():
    px = 64
    display.fill_rect(px - 4, 64 - 22 - 10, 8, 22, 1)
    for i in range (0, 10):
        display.line(px + i, 64 - i, px + i, 54, 1)
        display.line(px - i, 64 - i, px - i, 54, 1)
    display.show()

adc_pin_X = 11
X = Pin(adc_pin_X)
adc_pin_Y = 12
Y = Pin(adc_pin_Y)
K = Pin(13, Pin.IN, Pin.PULL_UP)

adcX = ADC(adc_pin_X)
adcY = ADC(adc_pin_Y)
adcX.width(ADC.WIDTH_12BIT)
adcY.width(ADC.WIDTH_12BIT)
# Set the attenuation (e.g., to measure up to 3.3V, use 11dB attenuation)
# Options: ADC.ATTN_0DB, ADC.ATTN_2_5DB, ADC.ATTN_6DB, ADC.ATTN_11DB
adcX.atten(ADC.ATTN_11DB)
adcY.atten(ADC.ATTN_11DB)

while True:
    raw_X_value = adcX.read()
    raw_Y_value = adcY.read()
    voltage_X_uv = int(adcX.read_uv() / 1000)
    voltage_Y_uv = int(adcY.read_uv() / 1000)
    raw_X_value = voltage_X_uv - 1500
    raw_Y_value = voltage_Y_uv - 1500
    K_state = K.value()
    if K_state == 1:
        pressed = "not pressed"
    else:
        pressed = "pressed"

    print(f"X: {voltage_X_uv} mV; Y: {voltage_Y_uv} mV; K: {pressed}.")
    print(f"Raw X: {raw_X_value}; Raw Y: {raw_Y_value}.")

    x_direction = "pointing "
    y_direction = "pointing "
    display.cls()
    if raw_X_value < 0:
        x_direction += "left"
        leftArrow()
    elif raw_X_value > 1400:
        x_direction += "right"
        rightArrow()
    else:
        x_direction = "neutral"
    if raw_Y_value < 0:
        y_direction += "down"
        downArrow()
    elif raw_Y_value > 1400:
        y_direction += "up"
        upArrow()
    else:
        y_direction = "neutral"

    print(f"X: {x_direction}; Y: {y_direction}.\n")
    time.sleep(0.3)
