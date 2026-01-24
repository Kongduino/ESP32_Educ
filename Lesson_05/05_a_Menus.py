import dht, machine, time, sys
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

def drawPage0():
    global menuItem
    display.fill(0)
    display.cls()
    display.displayString(FreeSans9Defs, "P0", -2, 0)
    if menuItem == 0:
        display.displayString(FreeSans9Defs, "> Menu 0", 0, 4)
    else:
        display.displayString(FreeSans9Defs, "* Menu 0", 0, 4)
    if menuItem == 1:
        display.displayString(FreeSans9Defs, "> Menu 1", 0, 20)
    else:
        display.displayString(FreeSans9Defs, "* Menu 1", 0, 20)
    if menuItem == 2:
        display.displayString(FreeSans9Defs, "> Menu 2", 0, 36)
    else:
        display.displayString(FreeSans9Defs, "* Menu 2", 0, 36)
    display.show(rotate180 = False)

def drawPage1():
    display.fill(0)
    display.cls()
    display.displayString(FreeSans9Defs, "P1", -2, 0)
    if menuItem == 0:
        display.displayString(FreeSans9Defs, "> Menu 0", 0, 4)
    else:
        display.displayString(FreeSans9Defs, "* Menu 0", 0, 4)
    if menuItem == 1:
        display.displayString(FreeSans9Defs, "> Menu 1", 0, 20)
    else:
        display.displayString(FreeSans9Defs, "* Menu 1", 0, 20)
    if menuItem == 2:
        display.displayString(FreeSans9Defs, "> Menu 2", 0, 36)
    else:
        display.displayString(FreeSans9Defs, "* Menu 2", 0, 36)
    display.show(rotate180 = False)

pages = [drawPage0, drawPage1]
pageNum = 0
menuItem = 0
while True:
    pages[pageNum]()
    time.sleep(5)
    menuItem += 1
    if menuItem == 3:
        pageNum += 1
        menuItem = 0
        if pageNum == 2:
            pageNum = 0

