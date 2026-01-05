# Lesson 04: A Class Act!

We are going to learn about Python's classes. A `Class` is a reusable object that you can fit with functions and variables for easy re-use. We have played with classes already: the `display` object used in the OLED and MAX7219 libraries for example are classes.

Our code so far, when trying to assert whether the OLED is connected, scans the I2C bus, and looks for the ID `60`. Why do this every time, and for every I2C-based device, when we could do it once, and supply an object that has all the answers?

Here is a very basic `I2C_Scanner` class:


```python
class I2C_Scanner_v1():
    def __init__(self, i2c):
        self._hasOLED = False
        self._has6DOF = False
        self._hasTOF = False
        self._myI2C = i2c
        self._devices = self._myI2C.scan()
        if 60 in self._devices:
            self._hasOLED = True
        if 41 in self._devices:
            self._hasTOF = True
        if 104 in self._devices:
            self._has6DOF = True

    @property
    def hasOLED(self):
        return self._hasOLED

    @property
    def has6DOF(self):
        return self._has6DOF

    @property
    def hasTOF(self):
        return self._hasTOF
```

## So what if I want to check regularly?

Like, if I plug in later on a new device. The scanner wouldn't be aware of that, right? Indeed, my dear, it wouldn't be... So... We need to change the code, and add a `check()` function:

```python
class I2C_Scanner():
    def __init__(self, i2c):
        self._hasOLED = False
        self._has6DOF = False
        self._hasTOF = False
        self._myI2C = i2c
        self.check()

    def check(self):
        self._devices = self._myI2C.scan()
        if 60 in self._devices:
            self._hasOLED = True
        if 41 in self._devices:
            self._hasTOF = True
        if 104 in self._devices:
            self._has6DOF = True

    @property
    def hasOLED(self):
        return self._hasOLED

    @property
    def has6DOF(self):
        return self._has6DOF

    @property
    def hasTOF(self):
        return self._hasTOF
```

This way, you can check regularly, and update the variables inside the scanner. Here is the updated example, with bonus code, where it uses the display if it's present. Why not? :-)


```python
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

```