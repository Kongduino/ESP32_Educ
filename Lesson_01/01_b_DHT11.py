import dht, machine, time
from freesans9 import FreeSans9Defs

i2c = machine.I2C(0)
devices = i2c.scan()
display = None

hasOLED = False

if devices.count(0x3c) == 0:
    print("No SSD1306!")
else:
    from ssd1306 import SSD1306_I2C
    display = SSD1306_I2C(128, 64, i2c)
    hasOLED = True

D = dht.DHT11(machine.Pin(3))
lastDisplay = 0 # never displayd DHT so far
interval = 30000 # 30 seconds

def displayDHT():
    global D, lastDisplay, hasOLED, display
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
    lastDisplay = time.ticks_ms()

while True:
    if time.ticks_ms() - lastDisplay > interval:
        displayDHT()

