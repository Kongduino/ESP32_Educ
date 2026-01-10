import time
from machine import Pin, I2C
from micropython_bmi270 import bmi270
from freesans9 import FreeSans9Defs

i2c = machine.I2C(0, scl=5, sda=4, freq=400000, timeout=50000)
bmi = bmi270.BMI270(i2c)
devices = i2c.scan()
display = None

hasOLED = False

if devices.count(0x3c) == 0:
    print("No SSD1306!")
else:
    from ssd1306 import SSD1306_I2C
    display = SSD1306_I2C(128, 64, i2c)
    hasOLED = True

while True:
    accx, accy, accz = bmi.acceleration
    accx = f"{accx:.2f} m/s2"
    accy = f"{accy:.2f} m/s2"
    accz = f"{accz:.2f} m/s2"
    print(f"x: {accx}, y: {accy}, z: {accz}")
    if hasOLED:
        display.cls()
        display.displayString(FreeSans9Defs, f"x: {accx}", 0, 4)
        display.displayString(FreeSans9Defs, f"y: {accy}", 0, 21)
        display.displayString(FreeSans9Defs, f"z: {accz}", 0, 38)
        display.show(rotate180 = False)

    time.sleep(0.5)
    gyrox, gyroy, gyroz = bmi.gyro
    #print("x:{:.2f}°/s, y:{:.2f}°/s, z{:.2f}°/s".format(gyrox, gyroy, gyroz))
    time.sleep(0.5)