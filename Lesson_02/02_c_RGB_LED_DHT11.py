import neopixel, time, dht
from machine import Pin, ADC
from freesans9 import FreeSans9Defs

D = dht.DHT11(machine.Pin(3))
hasOLED = False

if devices.count(0x3c) == 0:
    print("No SSD1306!")
else:
    from ssd1306 import SSD1306_I2C
    display = SSD1306_I2C(128, 64, i2c)
    hasOLED = True

def setColours(r, g, b):
    np[0] = (r, g, b)
    np.write()

def displayDHT():
    global D, lastDisplay
    D.measure()
    T = D.temperature()
    H = D.humidity()
    print(f"\t• Temperature:\t{T}°")
    print(f"\t• Humidity:\t{H}%")
    if hasOLED:
        display.cls()
        display.displayString(FreeSans9Defs, f"DHT:", 44, 0)
        display.displayString(FreeSans9Defs, f"Temp: {T}C", 0, 20)
        display.displayString(FreeSans9Defs, f"RH:  {H}%", 0, 40)
        display.show(rotate180 = False)
    if T < 10:
        setColours(0, 0, 255) # Blue
    elif T < 18:
        setColours(255, 255, 143) # Yellow
    elif T < 26:
        setColours(0, 255, 0) # Green
    elif T < 33:
        setColours(255, 191, 0) # Orange
    else:
        setColours(255, 0, 0)
    lastDisplay = time.ticks_ms() # Red

np = neopixel.NeoPixel(machine.Pin(48), 1)
# We only have one neopixel, on Pin 48
np[0] = (0, 0, 0) # RGB values
np.write()

lastDisplay = 0 # never displayd DHT so far
interval = 30000 # 30 seconds

while True:
    if time.ticks_ms() - lastDisplay > interval:
        displayDHT()
