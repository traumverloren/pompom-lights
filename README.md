Controls my hue lights via soft touchable yarn pompoms mixed with conductive thread

Hardware:
- [Adafruit Circuit Playground Express BlueFruit](https://learn.adafruit.com/adafruit-circuit-playground-bluefruit?view=all)
- Raspberry Pi 4

See my other approach built with a Adafruit ESP32-S2 Wifi QT Py here: https://github.com/traumverloren/pompom-lights-wifi


### To run BLE client on Pi:

`pm2 start ble_client.py --name pompom --interpreter python3`
