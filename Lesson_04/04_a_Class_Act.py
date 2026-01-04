import machine, time
import I2C_Scanner

i2c = machine.I2C()
SC = I2C_Scanner.I2C_Scanner(i2c)

print("\n\nRunning Scanner!")
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

