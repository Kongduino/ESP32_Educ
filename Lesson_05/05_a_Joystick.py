from machine import Pin, ADC
import time

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

    time.sleep(0.3)
