from sensorManager import *
from time import sleep
from ble_simple_central import *
import bluetooth

class BluetoothManager():
  def __init__(self):
    self.ble = bluetooth.BLE()
    self.central = BLESimpleCentral(self.ble)
    self.not_found = True

  def _on_scan(self, addr_type, addr, name):
    if addr_type is not None:
      print("Found peripheral:", addr_type, addr, name)
      self.central.connect()
    else:
      self.not_found = True
      print("No peripheral found.")
          
  def _scan(self):
    self.central.scan(callback=self._on_scan)

  def connect(self):
    self._scan()
    # Wait for connection...
    count = 0
    while not self.central.is_connected():
      if self.not_found:
        count+=1
        print("Fail to connect")
        if count >= 3:
          print("aborting connection.")
          break
        else:
          print("retrying in 3 sec...")
        sleep(3)
      else:
        print("Connected")

  def _on_rx(self, v):
    print("RX", bytes(v))

  def receive(self):
    self.central.on_notify(self._on_rx)
    with_response = False

    while self.central.is_connected():
        try:
            self.receive
        except:
            print("TX failed")
    sleep(5000 if with_response else 5000)

    print("Disconnected")
