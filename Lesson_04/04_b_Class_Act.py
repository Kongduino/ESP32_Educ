import machine, time
from I2C_Scanner_v2 import I2C_Scanner

i2c = machine.I2C(0, scl=5, sda=4, freq=400000, timeout=50000)
SC = I2C_Scanner(i2c)
lastDisplay = 0
interval = 30000 # 30 seconds
display = None

while True:
    if time.ticks_ms() - lastDisplay > interval:
        print("\n\nRunning Scanner!")
        dv = "Devices: "
        SC.check()
        if SC.hasOLED:
            print(" • OLED on!")
            dv += "OLED "
            if display == None:
                from ssd1306 import SSD1306_I2C
                from freesans9 import FreeSans9Defs
                display = SSD1306_I2C(128, 64, i2c)
            display.cls()
            display.displayString(FreeSans9Defs, "OLED on", 44, 0)
            display.show(rotate180 = False)
        else:
            print(" • No OLED found!")
        if SC.has6DOF:
            print(" • 6DOF on")
            dv += "6DOF "
        else:
            print(" • No 6DOF found!")
        if SC.hasTOF:
            print(" • TOF on")
            dv += "TOF "
        else:
            print(" • No TOF found!")
        print(dv)
        if display != None:
            display.displayString(FreeSans9Defs, dv, 0, 20, 1)
            display.show(rotate180 = False)
        lastDisplay = time.ticks_ms()
