from sensorManager import *
from time import sleep
from ble_simple_central import *
import bluetooth

class BluetoothManager():
  def __init__(self):
    self.ble = bluetooth.BLE()
    self.central = BLESimpleCentral(self.ble)
    self.not_found = False
    self.with_response = False

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
    print('self.not_found', self.not_found)
    if self.not_found:
      print(self.central.is_connected(), 'self.central.is_connected()')
      while not self.central.is_connected():
        print("Fail to connect")
        break
    
    print("Connected")
    
  def is_connected(self):
      return True
      
  def disconnect(self):
    print("Disconnected")

  def _on_rx(self, v):
    print("RX", bytes(v))

  def receive(self):
    self.central.on_notify(self._on_rx)

  def send(self, v):
    print('in send', self.central.is_connected())
    with_response = False
    if self.central.is_connected():
      print("TX", v)
      self.central.write(v, self.with_response)
      sleep(1 if with_response else 0)
