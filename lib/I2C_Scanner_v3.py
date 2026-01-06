class I2C_Scanner():
    def __init__(self, i2c):
        self._hasOLED = False
        self._has6DOF = False
        self._hasTOF = False
        self._myI2C = i2c
        self._objects = {}
        self._objects[60] = self._hasOLED
        self._objects[41] = self._hasTOF
        self._objects[104] = self._has6DOF
        self.check()

    def check(self):
        self._devices = self._myI2C.scan()
        for x in self._objects:
            if x in self._devices:
                self._objects[x] = True

    @property
    def hasOLED(self):
        return self._hasOLED

    @property
    def has6DOF(self):
        return self._has6DOF

    @property
    def hasTOF(self):
        return self._hasTOF


