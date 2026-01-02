# LESSON 01: DHT

## Installation

The DHT11/22 sensors are the most basic, *Hello World*-like sensors in the IoT arsenal. They provide vaguely accurate temperature and humidity data. They are usually easy to use (as the gritty details are hidden behind a library), and provide instant gratification for the learner.

The DHT11 is usually blue, whereas the DHT22 normally comes in white. You can see on the board that we have a DHT11. Connect it with a 3-pin "Boson" cable to Pin 3, the 2nd connector on the left from the top. I was tempted – like you probably are right now – to connect it to the first one, Pin 8: but that pin is already in use for I2C, which we will use shoertly, for the OLED display.

![Connection](../Assets/DHT11.png)

While we're at it, you can connect the OLED, with a Boson-to-Dupont cable; from left to right, looking at the Boson connector:

* C: SCL, Pin 9 (Green on the photo)
* D: SDA, Pin 8 (Blue on the photo)
* G: GND, one of the many GND pins (Black on the photo)
* V: VCC, one of the many 3.3 V pins (Red on the photo)

![OLED](../Assets/OLED.png)

## Dive in

This lesson is divided into 3 steps. [Part a](https://github.com/Kongduino/ESP32_Educ/blob/master/Lesson_01/01_a_DHT11.py) teaches you the basics of reading data from the DHT11 and display on a regular basis, here 30 seconds.

```python
import dht, machine, time

D = dht.DHT11(machine.Pin(8))
lastDisplay = 0 # never displayd DHT so far
interval = 30000 # 30 seconds

def displayDHT():
    global D, lastDisplay
    D.measure()
    T = D.temperature()
    H = D.humidity()
    print(f"\t• Temperature:\t{T}°")
    print(f"\t• Humidity:\t{H}%")
    lastDisplay = time.ticks_ms()

while True:
    if time.ticks_ms() - lastDisplay > interval:
        displayDHT()
```

There's already a DHT library in MicroPython, so we don't need to install anything, just `import dht` amd create a DHT object, which we will call `D`. We set up an interval to 30,000 milliseconds, and a `lastDisplay` semaphore to 0, ie never used so far.

In a `while True` loop (which means it never fails, ie runs forever), we check the elapsed time in milliseconds, and compare it with the lastDisplay record: `time.ticks_ms() - lastDisplay`. If it's more than 30 seconds, we print data in the REPL, and update `lastDisplay`. If not, we just skip over.

The `displayDHT()` function reads DHT data, and prints it out. Having a function here isn't necessary, as we only use it in one place, but it is good practice – it keeps the code cleaner, and easier to read.

The `global` keyword here tells Python that we will be using **existing** global variables, `D` and `lastDisplay` – without this new variables, local to `displayDHT()` would be created, which would lead to errors.

The way the DHT11 works is, you ask it first to take measurements: it does not do this automatically, but needs to be prompted. Then you can read the current temperature and humidity. And display it in the REPL.

A word about `print(f"...")`. The `f` here is important: it allows Python to format the output with variables, which are quoted between curly brackets. Thus:

```python
print(f"\t• Temperature:\t{T}°")
```

Means that Python needs to replace `{T}` with the contents of the variable T. This makes the code much easier to read.

Press the RUN button (the green arrow) and the code should start displaying Temperature and Humidity right away.

![Display](../Assets/DHT11_a.png)
