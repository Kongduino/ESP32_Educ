import machine, time
from I2C_Scanner_v2 import I2C_Scanner

i2c = machine.I2C(0, scl=5, sda=4, freq=400000, timeout=50000)
SC = I2C_Scanner(i2c)
lastDisplay = 0 # never displayd DHT so far
interval = 30000 # 30 seconds

while True:
    if time.ticks_ms() - lastDisplay > interval:
        print("\n\nRunning Scanner!")
        SC.check()
        if SC.hasOLED:
            print(" • OLED on!")
        else:
            print(" • No OLED found!")
        if SC.has6DOF:
            print(" • 6DOF on")
        else:
            print(" • No 6DOF found!")
        if SC.hasTOF:
            print(" • TOF on")
        else:
            print(" • No TOF found!")
        lastDisplay = time.ticks_ms()
