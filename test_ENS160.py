from ENS160 import ENS160
import dht, machine, time

D = dht.DHT11(machine.Pin(3))

#I2C init for sensors readout
SCL_PIN = machine.Pin(6)
SDA_PIN = machine.Pin(7)
i2c = machine.I2C(1, scl = SCL_PIN, sda = SDA_PIN, freq = 500000)
i2c0 = machine.I2C(0, scl = 5, sda = 4, timeout=50000)
devices = i2c0.scan()
display = None
hasOLED = False

if devices.count(0x3c) == 0:
    print("No SSD1306!")
else:
    from ssd1306 import SSD1306_I2C
    display = SSD1306_I2C(128, 64, i2c0)
    hasOLED = True

#init ENS160 sensor on the i2c bus
ens = ENS160(i2c)
calibrationInterval = 30 * 60000 # 30 mn
lastCalibration = 0
lastDisplay = 0 # never displayd DHT so far
interval = 30000 # 30 seconds

def calibrateENS():
    global D, lastCalibration, hasOLED
    D.measure()
    T = D.temperature()
    H = D.humidity()
    print(f"Calibrating with T = {T}, H = {H}.")
    if hasOLED:
        display.cls()
        display.displayString(FreeSans9Defs, f"Calibrating:", 10, 0)
        display.displayString(FreeSans9Defs, f"Temp: {T}C", 0, 20)
        display.displayString(FreeSans9Defs, f"RH:  {H}%", 0, 40)
        display.show(rotate180 = False)
    ens.calibrate_temp(T)
    ens.calibrate_hum(H)
    time.sleep(2)
    lastCalibration = time.ticks_ms()

def displayAQI():
    global ens, lastDisplay, hasOLED
    # get data
    # Get the air quality index
    # Return value: 1-Excellent, 2-Good, 3-Moderate, 4-Poor, 5-Unhealthy
    AQI = ens.getAQI()
    # Get TVOC concentration
    # Return value range: 0–65,000, unit: ppb
    TVOC = ens.getTVOC()
    # Get CO2 equivalent concentration calculated according to the detected data of VOCs and hydrogen (eCO2 – Equivalent CO2)
    # Return value range: 400–65000, unit: ppm
    # Five levels: Excellent (400 - 600), Good (600 - 800), Moderate(800 - 1,000), Poor (1,000 - 1,500), Unhealthy(> 1,500)
    ECO2 = ens.getECO2()
    #print data
    print(f" • AQI:\t\t{AQI}")
    print(f" • TVOC:\t{TVOC} ppb")
    print(f" • ECO2:\t{ECO2} ppm")
    if hasOLED:
        display.cls()
        display.displayString(FreeSans9Defs, f"aqi:   {AQI}", 0, 0)
        display.displayString(FreeSans9Defs, f"tvoc: {TVOC} ppb", 0, 18)
        display.displayString(FreeSans9Defs, f"eco2: {ECO2} ppm", 0, 36)
        display.show(rotate180 = False)
    lastDisplay = time.ticks_ms()

calibrateENS()

while True:
    if time.ticks_ms() - lastCalibration > calibrationInterval:
        calibrateENS()
    if time.ticks_ms() - lastDisplay > interval:
        displayAQI()

