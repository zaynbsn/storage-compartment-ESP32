from ble_client_manager import *
from time import sleep

ble = BluetoothManager()
ble.connect()
ble.receive()

while True:
  ble.send("test")
  sleep(1)
