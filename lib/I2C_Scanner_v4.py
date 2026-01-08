class I2C_Scanner():
    def __init__(self, i2c, objects):
        self._myI2C = i2c
        self._objects = objects
        self.check()

    def check(self):
        self._devices = self._myI2C.scan()
        print(self._devices)
        for x in self._objects:
            print(f"Looking for {x}")
            if x in self._devices:
                self._objects[x] = True

    @property
    def hasOLED(self):
        return self._objects[self._ID_OLED]

    @property
    def has6DOF(self):
        return self._objects[self._ID_6DOF]

    @property
    def hasTOF(self):
        return self._objects[self._ID_TOF]


