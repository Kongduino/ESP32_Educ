import dht, machine, time
from freesans9 import FreeSans9Defs

led2 = machine.Pin(12, machine.Pin.OUT) 
led2.value(0) # Turn LED off

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
interval = 20000 # 20 seconds

def displayDHT():
    global D, lastDisplay, hasOLED, display
    led2.value(1) # Turn LED on
    time.sleep(0.5) # need to give it a little time, or the LED will just blink
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
    led2.value(0) # Turn LED off
    lastDisplay = time.ticks_ms()

contrast = 255
decrement = 51 # 255÷51 = 5 steps x 2 seconds
# Screen will turn off after 10 seconds
display.contrast(contrast)
isOFF = False
while True:
    time.sleep(2)
    contrast -= decrement
    if contrast < 1:
        contrast = 0
    if isOFF == False and contrast == 0:
        isOFF = True
        display.poweroff()
    elif contrast > 0:
        display.contrast(contrast)
    if time.ticks_ms() - lastDisplay > interval:
        display.poweron() # turn OLED on
        isOFF = False
        contrast = 255 # and reset contrast to full
        display.contrast(contrast)
        displayDHT()
