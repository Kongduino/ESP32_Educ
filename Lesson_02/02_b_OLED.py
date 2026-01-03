import time
from machine import Pin, ADC

adc_pin = Pin(13, mode=Pin.IN)
adc = ADC(adc_pin)
adc.atten(ADC.ATTN_11DB)
lastRead = 0
interval = 100
lastValue = int(adc.read() / 16)
display.contrast(lastValue)
# This code inherits 'display' from boot.py

while True:
    if time.ticks_ms() - lastRead > interval:
        now = int(adc.read() / 16)
        if lastValue != now:
            display.contrast(now)
            print(f"Contrast: {now}")
            if now == 0:
                display.poweroff()
            else:
                display.poweron()
            lastValue = now
            lastRead = time.ticks_ms()



