from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService

import socket
import adafruit_requests

http = adafruit_requests.Session(socket)

# Add a secrets.py to your filesystem that has a dictionary called secrets with "ssid" and
# "password" keys with your WiFi credentials. DO NOT share that file or commit it into Git or other
# source control.
try:
    from secrets import secrets
except ImportError:
    print("api secrets are kept in secrets.py, please add them there!")
    raise


ble = BLERadio()
uart_connection = None

HUE_URL = 'http://' + secrets["ip_address"] + '/api/' + secrets["api_id"] + '/groups/12/action'

color = ''

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
            print(uart_service.readline().decode("utf-8"))
            if "green" in uart_service.readline().decode("utf-8"):
                print("COLOR IS GREEN!!!!")
                print("PUTing data to {0}".format(HUE_URL))
                response = http.put(HUE_URL, data='{"scene":"URnH9in2-faN3hS"}')

                print("-" * 40)
                print(response.status_code)
                print("-" * 40)
                response.close()
