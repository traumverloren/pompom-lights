
# Circuit Playground BLE code
import time
import board
import neopixel
import touchio

from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService

ble = BLERadio()
uart = UARTService()
advertisement = ProvideServicesAdvertisement(uart)

touch_A1 = touchio.TouchIn(board.A1)
touch_A2 = touchio.TouchIn(board.A2)
touch_A3 = touchio.TouchIn(board.A3)
touch_A4 = touchio.TouchIn(board.A4)
touch_A5 = touchio.TouchIn(board.A5)
touch_A6 = touchio.TouchIn(board.A6)
touch_TX = touchio.TouchIn(board.TX)

pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=0.2, auto_write=False)

RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
WHITE = (255, 255, 255)
OFF = (0, 0, 0)

new_color = ""
color_sent = ""

while True:
    ble.start_advertising(advertisement)
    print("Waiting to connect")
    while not ble.connected:
        pass
    print("Connected")
    while ble.connected:
        if touch_A1.value:
            print("Touched A1!")
            pixels.fill(GREEN)
            pixels.show()
            new_color = "green"
            if new_color != color_sent:
                color_sent = new_color
                print(color_sent)
                print(new_color)
                uart.write(color_sent.encode("utf-8"))
        if touch_A2.value:
            print("A2 touched!")
        if touch_A3.value:
            print("A3 touched!")
        if touch_A4.value:
            print("A4 touched!")
        if touch_A5.value:
            print("A5 touched!")
        if touch_A6.value:
            print("A6 touched!")
        if touch_TX.value:
            print("TX touched!")

        time.sleep(0.01)
        pixels.fill(OFF)
        pixels.show()

