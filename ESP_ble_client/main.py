from ble.bleClientManager import BluetoothManager
from leds.ledsManager import LedsManager
from leds.led import *
from tests.checkList import CheckInitialState
from systemStates import *
from homeeSystem import HomeeSystem
from alertDelegate import *
from libs.hcsr04 import *
from sensor.sensorManager import SensorManager
from sensor.sensorStates import *
from neopixel import NeoPixel

sensor = HCSR04(trigger_pin=14, echo_pin=12, echo_timeout_us=10000)
sensorManager = SensorManager(sensor, SensorAlertManager())

ledStrip = NeoPixel(Pin(23), 12)
led1 = Led([1, 2])
led2 = Led([5, 6])
led3 = Led([9, 10])
leds = [led1, led2, led3]
ledManager = LedsManager(ledStrip, leds)

# CheckInitialState().runAllTests(leds=leds)
homeeSystem = HomeeSystem(SystemOKState(), ledManager)

ble = BluetoothManager(BLEAlertManager(), homeeSystem)

while True:
  try:
      if type(homeeSystem.state) == SystemOKState:
        if ble.is_connected():
          homeeSystem.checkSystemState(ble=ble)

        else:
          sensorManager.estimateDistance()
          if type(sensorManager.currentState) == NearState:
            ble.connect()
          homeeSystem.checkSystemState(sensor=sensorManager)
        sleep(1)
      else:
        break

  except KeyboardInterrupt:
      homeeSystem.stop()
      raise