from ble_client_manager import BluetoothManager
from ledsManager import LedsManager
from led import *
from tests.checkList import CheckInitialState

led = Led([23,22,21])
leds = [led]
ledsManager = LedsManager(leds)
ledsManager.turnOffLeds()

CheckInitialState().runAllTests(leds=leds)

ble = BluetoothManager()
# ble.connect()
# ble.receive()

while True:
  try:
      if ble.is_connected(): 
        ble.send("test")

  except KeyboardInterrupt:
      ledsManager.deinitAllPins()
      raise