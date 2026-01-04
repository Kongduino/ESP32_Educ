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

