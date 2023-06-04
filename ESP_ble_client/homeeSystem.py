from securityStates import *
from ble.bleStates import *
from leds.ledStates import *

from machine import Pin, SoftI2C
from accelerometer.accelerometer import Accel

from ble.bleClientManager import BluetoothManager
from leds.ledsManager import LedsManager
from leds.led import *
from alertDelegate import *
from libs.hcsr04 import *
from sensor.sensorManager import SensorManager
from sensor.sensorStates import *
from systemStates import *
from neopixel import NeoPixel
from time import sleep_ms

class HomeeSystem:
    def __init__(self, state, securityState, ledManager, sensorManager, accel):
        self.state = state
        self.securityState = securityState

        self.ledManager = ledManager
        self.sensorManager = sensorManager
        self.accel = accel
        self.ble = None

        self.cooldown = 0
        self.decodedStr = ''

    def updateState(self, newState):
        self.state = newState
    
    def updateSecurityState(self, newState):
        self.securityState = newState

    def checkSystemState(self, ble=False, sensor=False):
        self.updateSecurityState(SystemOKState())

        if ble and self.ble:
            bleState = self.ble.getState()
            if type(bleState) != BLEIsReadyState:
                self.updateSecurityState(SystemNotOKState())

        if sensor and self.sensorManager:
            sensorState = self.sensorManager.getState()
            if type(sensorState) == NoValueState:
                self.updateSecurityState(SystemNotOKState())

    def decodeString(self, str):
        self.decodedStr = str.split("||")
        self.decodedStr = [1, 1, 0] 
        for i in range(len(self.decodedStr)):
            state = int(self.decodedStr[i])
            if state == 0:
                self.decodedStr[i] = RedState()
            elif state == 1:
                self.decodedStr[i] = WhiteState()
            elif state == 2:
                self.decodedStr[i] = BlueState()
            else:
                self.decodedStr[i] = InitialState()

        self.updateLedsStates()
        self.turnOnLeds()

    def updateLedsStates(self):
        for i in range(len(self.ledManager.leds)):
            self.ledManager.leds[i].updateState(self.decodedStr[i])

    def turnOnLeds(self):
        self.ledManager.run()

    def launchCooldown(self):
        self.checkSystemState(ble=True)
        self.cooldown += 1
        print(self.cooldown)
        if self.cooldown >= 300:
            self.cooldown = 0
            self.ble.disconnect()
            self.stop()

    def sendSystemState(self, value):
        count = 0
        while not self.ble.is_connected():
            if count >= 3:
                print('no connexion to check ack')
                self.updateState(BLENotConnectedState())
                return
            print('waiting connexion to send SystemState :', value)
            count += 1
            sleep(1)
        self.ble.send(value)

    def accelFirst(self):
        self.updateState(EntryState())
        print('SHAKING')
        self.ble.connect()
        self.sendSystemState('Entry')

    def sensorFirst(self):
        self.updateState(ExitState())
        self.ble.connect()
        self.sendSystemState('Exit')

    def checkSensors(self):
        self.sensorManager.estimateDistance()
        if type(self.sensorManager.currentState) == NearState:
            self.sensorFirst()
        elif Accel.shaking(self.accel):
            self.accelFirst()

    def run(self):
        if self.ble.is_connected():
            self.launchCooldown()
        else:
            self.checkSensors()
        self.checkSystemState(sensor=True)

    def stop(self):
        self.ledManager.turnOffLeds()
        self.ble.disconnect()

    @staticmethod
    def setup():
        ############# accel ##############
        i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
        mpu = Accel(i2c)

        ############# sensor ##############
        sensor = HCSR04(trigger_pin=14, echo_pin=12, echo_timeout_us=10000)
        sensorManager = SensorManager(sensor, SensorAlertManager())

        ############# ledsStrip ##############
        ledStrip = NeoPixel(Pin(23), 12)
        led1 = Led([0, 1, 2])
        led2 = Led([4, 5, 6, 7])
        led3 = Led([9, 10, 11])
        leds = [led1, led2, led3]
        ledManager = LedsManager(ledStrip, leds)
        from leds.pulse import Pulse
        
        Pulse.animate(ledsStrip=ledStrip, pixels=[led1.pixels, led2.pixels], duration=2)

        ############## BLE ##############
        
        ble = BluetoothManager(BLEAlertManager())

        homee = HomeeSystem(state=ReadSensorState(), securityState=SystemOKState(), ledManager=ledManager, sensorManager=sensorManager, accel=mpu)
        homee.ble = ble

        return homee