# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()
import machine, time

i2c = machine.I2C()
devices = i2c.scan()
print(devices)
import test_ssd1306