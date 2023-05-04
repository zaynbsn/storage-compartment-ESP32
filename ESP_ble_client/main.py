from ble_client_manager import *
from time import sleep
from ledManager import LedManager
from led import *
from ledState import *

ble = BluetoothManager()
ble.connect()
ble.receive()

led = Led([23,22,21])
ledManager = LedManager([led])

while True:
  try:
      if ble.is_connected(): 
        ble.send("test")

      led.updateState(FullState())
      led.turnOnLed()
      sleep(1)

      led.updateState(EmptyState())
      led.turnOnLed()
      sleep(1)

      led.updateState(WrongItemState())
      led.turnOnLed()
      sleep(1)
      
      ledManager.turnOffLeds()
      sleep(1)

  except KeyboardInterrupt:
      led.deinit_pwm_pins()
      raise

