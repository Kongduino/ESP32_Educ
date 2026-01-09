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

    #@property
    # Since we are passing a parameter, it cannot be a property anymore.
    def hasDevice(ID):
        return self._objects[ID]
