import max7219
from machine import Pin, SPI
spi = SPI(1)
display = max7219.Matrix8x8(spi, Pin(7), 1)

start = 0
for x in range(72):
    display.fill(0)
    display.text("Kongduino", start, 0, 1)
    display.show()
    time.sleep(0.1)
    start -= 1

