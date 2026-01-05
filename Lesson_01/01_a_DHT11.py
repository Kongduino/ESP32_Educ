import dht, machine, time


D = dht.DHT11(machine.Pin(3))
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

