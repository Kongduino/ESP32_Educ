# Lesson 05: Menus and Joystick

This lesson will be a little more complex, and will have two steams, `Josytick` and `Menus`, which you can do in any order, to merge into `05_c_Menus_Joystick` at the end. And possibly a `05_d_Menus_Joystick` down the line.

## Menus

Let's start small. We want to have several pages of menus, 3 items (and late more) per page. And show which item on the current page is selected, with a `>`. `05_a_Menus.py` does the basics.

### PageX functions

There are two `drawPage_()` functions that each display the page number and 3 menu items. Based on the `menuItem` variable it shows which menu item is displayed. It's a bit fragile (since there should be a `menuItem` per page), but for now it works.

### Main loop

The main loop displays the current page, based on `pageNum` and `menuItem`. It then increments `menuItem`, and when it goes above 2, the maximum for now, it increments `pageNum` and resets `menuItem` to zero. And when `pageNum` reaches 2, it loops back to 0. A 5-second delay shows each step.

```python
pageNum = 0
menuItem = 0
while True:
    pages[pageNum]()
    time.sleep(5)
    menuItem += 1
    if menuItem == 3:
        pageNum += 1
        menuItem = 0
        if pageNum == 2:
            pageNum = 0
```

No user input for now. And no more than 3 items per page. We'll improve on that.

## Joystick

But we do need to have a look at how the joystick works before we can go on to improving menus. `05_a_Joystick.py` is very simple, 30 lines of code.

### Setup

The first part is setting up 2 ADC-compatible pins, and connecting them, plus a digital pin. I picked 11, 12, and 13.

```
from machine import Pin, ADC
import time

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
```

### Calibration

Once we have this, we display the values – the user moves the joystick around, and we'll get raw ADC and voltage values. We can see what the threshold is for each direction.

```python
while True:
    raw_X_value = adcX.read()
    raw_Y_value = adcY.read()
    voltage_X_uv = int(adcX.read_uv() / 1000)
    voltage_Y_uv = int(adcY.read_uv() / 1000)
    raw_X_value = voltage_X_uv - 1500
    raw_Y_value = voltage_Y_uv - 1500
    K_state = K.value()
    if K_state == 1:
        pressed = "not pressed"
    else:
        pressed = "pressed"

    print(f"X: {voltage_X_uv} mV; Y: {voltage_Y_uv} mV; K: {pressed}.")
    print(f"Raw X: {raw_X_value}; Raw Y: {raw_Y_value}.")

    time.sleep(0.3)
```

These (not very accurate) thresholds will be used to determine the position of the joystick: not only left and right, up and down, but also a combination of both.

```
>>> %Run -c $EDITOR_CONTENT

MPY: soft reboot
DEVICES:
[60, 104]
X: 1612 mV; Y: 1614 mV; K: not pressed.
Raw X: 112; Raw Y: 114.
X: 1611 mV; Y: 1616 mV; K: not pressed.
Raw X: 111; Raw Y: 116.
X: 1609 mV; Y: 1655 mV; K: not pressed.
Raw X: 109; Raw Y: 155.
X: 1604 mV; Y: 1634 mV; K: not pressed.
Raw X: 104; Raw Y: 134.
X: 1597 mV; Y: 1609 mV; K: not pressed.
Raw X: 97; Raw Y: 109.
X: 1594 mV; Y: 1614 mV; K: not pressed.
Raw X: 94; Raw Y: 114.
X: 2825 mV; Y: 1522 mV; K: not pressed.
Raw X: 1325; Raw Y: 22.
X: 3111 mV; Y: 1376 mV; K: not pressed.
Raw X: 1611; Raw Y: -124.
X: 3117 mV; Y: 1379 mV; K: not pressed.
Raw X: 1617; Raw Y: -121.
X: 3080 mV; Y: 1444 mV; K: not pressed.
Raw X: 1580; Raw Y: -56.
X: 1438 mV; Y: 1594 mV; K: not pressed.
Raw X: -62; Raw Y: 94.
X: 40 mV; Y: 1601 mV; K: not pressed.
Raw X: -1460; Raw Y: 101.
X: 34 mV; Y: 1601 mV; K: not pressed.
Raw X: -1466; Raw Y: 101.
X: 241 mV; Y: 990 mV; K: not pressed.
Raw X: -1259; Raw Y: -510.
X: 1907 mV; Y: 1828 mV; K: not pressed.
Raw X: 407; Raw Y: 328.
X: 2076 mV; Y: 4980 mV; K: not pressed.
Raw X: 576; Raw Y: 3480.
X: 2201 mV; Y: 4980 mV; K: not pressed.
Raw X: 701; Raw Y: 3480.
X: 2207 mV; Y: 4980 mV; K: not pressed.
Raw X: 707; Raw Y: 3480.
X: 1605 mV; Y: 1633 mV; K: not pressed.
Raw X: 105; Raw Y: 133.
X: 1339 mV; Y: 571 mV; K: not pressed.
Raw X: -161; Raw Y: -929.
X: 1359 mV; Y: 555 mV; K: not pressed.
Raw X: -141; Raw Y: -945.
X: 1841 mV; Y: 2091 mV; K: not pressed.
Raw X: 341; Raw Y: 591.
X: 1602 mV; Y: 1609 mV; K: not pressed.
Raw X: 102; Raw Y: 109.
X: 1601 mV; Y: 1610 mV; K: not pressed.
Raw X: 101; Raw Y: 110.
```

The logs show when a value changes radically. So we'll need to come up with values that indicate a change of direction.