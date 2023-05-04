from ble_client_manager import *
from time import sleep
from ledManager import LedManager

ble = BluetoothManager()
ble.connect()
ble.receive()

ledManager = LedManager()

while True:
  try:
      if ble.is_connected(): 
        ble.send("test")
      
      ledManager.displayRed()
      sleep(1)
      ledManager.displayGreen()
      sleep(1)
      ledManager.displayBlue()
      sleep(1)

  except KeyboardInterrupt:
      ledManager.deinit_pwm_pins()
      raise

