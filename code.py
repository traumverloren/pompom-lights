
# Circuit Playground BLE code
import time
import board
import neopixel
import touchio

from rainbowio import colorwheel

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

touch_A1 = touchio.TouchIn(board.A1)  # red
touch_A3 = touchio.TouchIn(board.A3)  # on/off
touch_A5 = touchio.TouchIn(board.A5)  # green
touch_A6 = touchio.TouchIn(board.A6)  # blue
touch_TX = touchio.TouchIn(board.TX)  # rainbow

touch_sensors = [touch_TX, touch_A1, touch_A3, touch_A5, touch_A6]

for sensor in touch_sensors:
    sensor.threshold = 800

touch_A3.threshold = 1300

pixels = neopixel.NeoPixel(
    board.NEOPIXEL, 10, brightness=0.2, auto_write=False)

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
is_touched = False


def rainbow(wait):
    for j in range(255):
        for i in range(10):
            rc_index = (i * 256 // 10) + j * 5
            pixels[i] = colorwheel(rc_index & 255)
        pixels.show()
        time.sleep(wait)


def reversed_rainbow(wait):
    for j in reversed(range(255)):
        for i in reversed(range(10)):
            rc_index = (i * 256 // 10) + j * 5
            pixels[i] = colorwheel(rc_index & 255)
        pixels.show()
        time.sleep(wait)


while True:
    ble.start_advertising(advertisement)
    print("Waiting to connect")
    while not ble.connected:
        pass
    print("Connected")
    while ble.connected:
        if touch_TX or touch_A1 or touch_A3 or touch_A5 or touch_A6:
            is_touched = True
            time.sleep(1)

        if is_touched:
            if touch_A3.value:
                print("A3 touched!")
                if current_color == "off" or current_color == "":
                    pixels.fill(WHITE)
                    pixels.show()
                    new_color = "on"
                else:
                    new_color = "off"

            elif touch_TX.value:
                print("Touched TX!")
                if current_color == "rainbow":
                    reversed_rainbow(0.01)
                    new_color = "no_rainbow"
                else:
                    rainbow(0.01)
                    new_color = "rainbow"

            elif touch_A1.value and touch_A6.value and current_color != "yellow":
                print("Touched red & green!")
                pixels.fill(YELLOW)
                pixels.show()
                new_color = "yellow"

            elif touch_A1.value and touch_A5.value and current_color != "purple":
                print("Touched red & blue!")
                pixels.fill(PURPLE)
                pixels.show()
                new_color = "purple"

            elif touch_A5.value and touch_A6.value and current_color != "cyan":
                print("Touched blue & green!")
                pixels.fill(CYAN)
                pixels.show()
                new_color = "cyan"

            elif touch_A1.value and current_color != "red":
                print("Touched A1!")
                pixels.fill(RED)
                pixels.show()
                new_color = "red"

            elif touch_A5.value and current_color != "blue":
                print("Touched A5!")
                pixels.fill(BLUE)
                pixels.show()
                new_color = "blue"

            elif touch_A6.value and current_color != "green":
                print("Touched A6!")
                pixels.fill(GREEN)
                pixels.show()
                new_color = "green"

            if current_color != new_color:
                is_touched = False
                current_color = new_color
                print(current_color)
                data = current_color + "\n"
                uart.write(data.encode("utf-8"))
                time.sleep(1)
                pixels.fill(OFF)
                pixels.show()
