
# Circuit Playground BLE code
import time
import board
import neopixel
import touchio

# Don't forget to update board to latest circuitpython
# https://learn.adafruit.com/welcome-to-circuitpython/installing-circuitpython

# Use Mu editor for easiest IDE experience

# Add reqd libraries to lib/ folder on arduino (eg adafruit_ble, neopixel)
# (check serial console for errors ro know which ones)
# https://circuitpython.org/libraries

from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService

ble = BLERadio()
uart = UARTService()
advertisement = ProvideServicesAdvertisement(uart)

touch_A1 = touchio.TouchIn(board.A1)
touch_A3 = touchio.TouchIn(board.A3)
touch_A4 = touchio.TouchIn(board.A4)
touch_A6 = touchio.TouchIn(board.A6)

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
current_color = "on"

while True:
    ble.start_advertising(advertisement)
    print("Waiting to connect")
    while not ble.connected:
        pass
    print("Connected")
    while ble.connected:
        if touch_A1.value and current_color != "red":
            print("Touched A1!")
            pixels.fill(RED)
            pixels.show()
            new_color = "red"
            if new_color != current_color:
                current_color = new_color
                print(new_color)
                data = current_color + "\n"
                uart.write(data.encode("utf-8"))
                time.sleep(2)
        if touch_A3.value:
            print("A3 touched!")
            if current_color == "off" or current_color == "":
                new_color = "on"
            else:
                new_color = "off"
            current_color = new_color
            data = current_color + "\n"
            uart.write(data.encode("utf-8"))
            time.sleep(2)
        if touch_A4.value and current_color != "blue":
            print("Touched A4!")
            pixels.fill(BLUE)
            pixels.show()
            new_color = "blue"
            if new_color != current_color:
                current_color = new_color
                print(new_color)
                data = current_color + "\n"
                uart.write(data.encode("utf-8"))
                time.sleep(2)
        if touch_A6.value and current_color != "green":
            print("Touched A6!")
            pixels.fill(GREEN)
            pixels.show()
            new_color = "green"
            if new_color != current_color:
                current_color = new_color
                print(new_color)
                data = current_color + "\n"
                uart.write(data.encode("utf-8"))
                time.sleep(2)
        time.sleep(0.1)
        pixels.fill(OFF)
        pixels.show()
