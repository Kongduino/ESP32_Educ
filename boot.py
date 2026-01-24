# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()
import machine, time, sys

i2c = machine.I2C()
devices = i2c.scan()
print(f"DEVICES:\n{devices}")

display = None

if devices.count(0x3c) == 0:
    print("No SSD1306!")
else:
    from ssd1306 import SSD1306_I2C
    display = SSD1306_I2C(128, 64, i2c)

def showText(line, px, py, refresh = True):
    global display
    print(line)
    if display == None:
        return
    display.text(line, px, py)
    if refresh == True:
        display.show()

if display != None:
    display.fill(0)
    display.fill_rect(0, 0, 32, 32, 1)
    display.fill_rect(2, 2, 28, 28, 0)
    display.vline(9, 8, 22, 1)
    display.vline(16, 2, 22, 1)
    display.vline(23, 8, 22, 1)
    display.fill_rect(26, 24, 2, 4, 1)
    display.show()
    display.text('MicroPython', 40, 0, 1)
    display.show()
    display.text('SSD1306', 40, 12, 1)
    display.show()
    display.text('OLED 128x64', 40, 24, 1)
    display.show()
    display.text('uPython!', 0, 48, 1)
    display.doubleText(6)
    display.show()
    time.sleep(2)
    
    display.cls()
    from freesans9 import FreeSans9Defs
    display.displayString(FreeSans9Defs, "Kongduino", 0, 0)
    display.displayString(FreeSans9Defs, "says hi!", 50, 18)
    display.show(rotate180 = False)
    time.sleep(2)
    
    display.cls()
    from freemono9 import FreeMono9Defs
    display.displayString(FreeMono9Defs, "Ready!", -1, -1, False)
    display.show(rotate180 = False)
    time.sleep(2)



