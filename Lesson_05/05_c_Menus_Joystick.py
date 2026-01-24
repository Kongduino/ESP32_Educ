from machine import Pin, ADC
import dht, machine, time, sys
from freesans9 import FreeSans9Defs

i2c = machine.I2C(0, scl = 5, sda = 4, freq = 400000, timeout = 50000)
devices = i2c.scan()
display = None
D = dht.DHT11(machine.Pin(3))
led2 = machine.Pin(12, machine.Pin.OUT) 
led2.value(0) # Turn LED off

if devices.count(0x3c) == 0:
    print("No SSD1306!")
    sys.exit()
else:
    from ssd1306 import SSD1306_I2C
    display = SSD1306_I2C(128, 64, i2c)

adc_pin_X = 11
X = Pin(adc_pin_X)
adc_pin_Y = 12
Y = Pin(adc_pin_Y)
K = Pin(13, Pin.IN, Pin.PULL_UP)

adcX = ADC(adc_pin_X)
adcY = ADC(adc_pin_Y)
adcX.width(ADC.WIDTH_12BIT)
adcY.width(ADC.WIDTH_12BIT)
# Set the attenuation (e.g., to measure up to 3.3V, use 11dB attenuation)
# Options: ADC.ATTN_0DB, ADC.ATTN_2_5DB, ADC.ATTN_6DB, ADC.ATTN_11DB
adcX.atten(ADC.ATTN_11DB)
adcY.atten(ADC.ATTN_11DB)

menuItem = [0, 0, 0]
topMenuItem = [0, 0, 0]

pages = [
    ["DHT", "Menu 1", "Menu 2", "Menu 3"],
    ["Menu 4", "Menu 5", "Menu 6"],
    ["Menu 7", "Menu 8", "Menu 9", "Menu A"],
    ]
pageIndex = 0

def drawPage():
    global menuItem, pageIndex, pages
    items = pages[pageIndex]
    display.fill(0)
    display.cls()
    title = f"P{pageIndex}"
    display.displayString(FreeSans9Defs, title, -2, 0)
    ix = menuItem[pageIndex]
    jx = topMenuItem[pageIndex]
    count = len(items)
    s = ""
    for i in range (0, 3):
        n = jx + i
        if n == count:
            n = 0
        if ix == n:
            s = "> " + pages[pageIndex][n]
        else:
            s = "  " + pages[pageIndex][n]
        display.displayString(FreeSans9Defs, s, 0, i*16+4)
    display.show(rotate180 = False)

def doNothing():
    print("Doing Nothing")
    display.cls()
    display.displayString(FreeSans9Defs, "Nothing", -1, -1)
    display.show(rotate180 = False)
    time.sleep(2)
    drawPage()

def showDHT():
    global D, lastDisplay, hasOLED, display
    led2.value(1) # Turn LED on
    time.sleep(0.5) # need to give it a little time, or the LED will just blink
    D.measure()
    T = D.temperature()
    H = D.humidity()
    print(f"\t• Temperature:\t{T}°")
    print(f"\t• Humidity:\t{H}%")
    display.cls()
    display.displayString(FreeSans9Defs, f"DHT:", 44, 0)
    display.displayString(FreeSans9Defs, f"Temp: {T}C", 0, 20)
    display.displayString(FreeSans9Defs, f"RH:  {H}%", 0, 40)
    display.show(rotate180 = False)
    led2.value(0) # Turn LED off
    time.sleep(5)
    drawPage()

actions = [
    [showDHT, doNothing, doNothing, doNothing],
    [doNothing, doNothing, doNothing],
    [doNothing, doNothing, doNothing, doNothing]
    ]

drawPage()

def getValues():
    raw_X_value = adcX.read()
    raw_Y_value = adcY.read()
    voltage_X_uv = int(adcX.read_uv() / 1000)
    voltage_Y_uv = int(adcY.read_uv() / 1000)
    raw_X_value = voltage_X_uv - 1500
    raw_Y_value = voltage_Y_uv - 1500
    K_state = K.value()
    return raw_X_value, raw_Y_value, K_state

while True:
    raw_X_value, raw_Y_value, K_state = getValues()
    if K_state == 0:
        pressed = "pressed"
        raw_X_value, raw_Y_value, K_state = getValues()
        while K_state == 0:
            raw_X_value, raw_Y_value, K_state = getValues()
        print(f"Launching item {menuItem[pageIndex]}, page {pageIndex}")
        actions[pageIndex][menuItem[pageIndex]]()
    else:
    
        if raw_X_value < 0:
            # x_direction += "left"
            raw_X_value, raw_Y_value, K_state = getValues()
            while raw_X_value < 0:
                raw_X_value, raw_Y_value, K_state = getValues()
            # debounce
            print("Left")
            pageIndex -= 1
            if pageIndex == -1:
                pageIndex = len(pages) - 1
            drawPage()
            
        elif raw_X_value > 1400:
            # x_direction += "right"
            raw_X_value, raw_Y_value, K_state = getValues()
            while raw_X_value > 1400:
                raw_X_value, raw_Y_value, K_state = getValues()
            # debounce
            print("Right")
            pageIndex += 1
            if pageIndex == len(pages):
                pageIndex = 0
            drawPage()
    
        if raw_Y_value < 0:
            #y_direction += "down"
            ix = menuItem[pageIndex] + 1
            jx = topMenuItem[pageIndex]
            print(f"ix = {ix}, jx = {jx}")
            if ix == len(pages[pageIndex]):
                ix = 0
                print("Looping to 0")
                jx = 0
            elif ix > 2:
                jx += 1
                print("Scrolling down")
                if jx == len(pages[pageIndex]):
                    print("Looping back to 0")
                    jx = 0
                    ix = 0
            print(f"--> ix = {ix}, jx = {jx}")
            menuItem[pageIndex] = ix
            topMenuItem[pageIndex] = jx
            print("Down\n")
            drawPage()
        elif raw_Y_value > 1400:
            #y_direction += "up"
            ix = menuItem[pageIndex] - 1
            jx = topMenuItem[pageIndex]
            print(f"ix = {ix}, jx = {jx}")
            if ix == -1:
                ix = len(pages[pageIndex]) - 1
                print(f"Looping to bottom : {ix}")
                jx = ix - 2
                if jx < 0:
                    jx = 0
            elif jx > menuItem[pageIndex] - 2:
                jx -= 1
                if jx < 0:
                    jx = 0
                print("Scrolling uo")
            print(f"--> ix = {ix}, jx = {jx}")
            menuItem[pageIndex] = ix
            topMenuItem[pageIndex] = jx
            print("Up\n")
            drawPage()
    time.sleep(0.3)
