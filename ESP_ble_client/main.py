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

sensor = HCSR04(trigger_pin=14, echo_pin=12, echo_timeout_us=10000)
sensorManager = SensorManager(sensor)

led = Led([23,22,21])
leds = [led]
ledsManager = LedsManager(leds)

# CheckInitialState().runAllTests(leds=leds)
homeeSystem = HomeeSystem(SystemOKState())

ble = BluetoothManager(BLEAlertManager())
#ble.connect()

while True:
  try:
      if type(homeeSystem.state) == SystemOKState:
        if ble.is_connected():
          ledsManager.turnOnLeds()
          homeeSystem.checkSystemState(ble)

        else:
          # sensorManager.estimateDistance()
          # if type(sensorManager.currentState) == NearState:
          print(sensor.distance_cm())
          if 0 < sensor.distance_cm() <= 30:
            ble.connect()
          homeeSystem.checkSystemState()
            
        sleep(1)
      else:
        break

  except KeyboardInterrupt:
      ledsManager.deinitAllPins()
      raise