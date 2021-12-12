import adafruit_requests as requests

from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService


# Add a secrets.py to your filesystem that has a dictionary called secrets with "ssid" and
# "password" keys with your WiFi credentials. DO NOT share that file or commit it into Git or other
# source control.
# pylint: disable=no-name-in-module,wrong-import-order
try:
    from secrets import secrets
except ImportError:
    print("api secrets are kept in secrets.py, please add them there!")
    raise

ble = BLERadio()
uart_connection = None

color = ''
new_color = ''

while True:
    if not uart_connection:
        print("Trying to connect...")
        for adv in ble.start_scan(ProvideServicesAdvertisement):
            if UARTService in adv.services:
                uart_connection = ble.connect(adv)
                print("Connected")
                break
        ble.stop_scan()

    if uart_connection and uart_connection.connected:
        uart_service = uart_connection[UARTService]
        while uart_connection.connected:
            new_color = uart_service.readline().decode("utf-8")
            if new_color != color:
                color = new_color
                print(current_color)
                if color == "green":
                    requests.put('https://192.168.178.41/api/' + {secrets["api_id"]} + '/groups/12/action', {"scene":"URnH9in2-faN3hS"})
