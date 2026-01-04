# Lesson 04: A Class Act!

We are going to learn about Python's classes. A `Class` is a reusable object that you can fit with functions and variables for easy re-use. We have played with classes already: the `display` object used in the OLED and MAX7219 libraries for example are classes.

Our code so far, when trying to assert whether the OLED is connected, scans the I2C bus, and looks for the ID `60`. Why do this every time, and for every I2C-based device, when we could do it once, and supply an object that has all the answers?

Here is a very basic `I2C_Scanner` class:


```python
class I2C_Scanner():
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

