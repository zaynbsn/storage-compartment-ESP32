from systemStates import *
from ble.bleStates import *
from leds.ledStates import *

from machine import Pin, SoftI2C
from accelerometer.accelerometer import Accel

from ble.bleClientManager import BluetoothManager
from leds.ledsManager import LedsManager
from leds.led import *
from systemStates import *
from alertDelegate import *
from libs.hcsr04 import *
from sensor.sensorManager import SensorManager
from sensor.sensorStates import *
from neopixel import NeoPixel

class HomeeSystem:
    def __init__(self, state, ledManager, sensorManager, accel):
        self.state = state
        self.ledManager = ledManager
        self.sensorManager = sensorManager
        self.accel = accel
        self.ble = None
        self.cooldown = 0
        self.decodedStr = ''

    def updateState(self, newState):
        self.state = newState

    def checkSystemState(self, ble=False, sensor=False):
        # print("checking system state")
        ### check everything ###
        self.updateState(SystemOKState())

        if ble and self.ble:
            bleState = self.ble.getState()
            if type(bleState) != BLEIsReadyState:
                self.updateState(SystemNotOKState())

        if sensor and self.sensorManager:
            sensorState = self.sensorManager.getState()
            if type(sensorState) == NoValueState:
                self.updateState(SystemNotOKState())

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

    def run(self):
        if self.ble.is_connected():
            self.launchCooldown()
        else:
            self.sensorManager.estimateDistance()
            if type(self.sensorManager.currentState) == NearState:
                # change state to Entry
                self.ble.connect()
            elif Accel.shaking(self.accel):
                # change state to Exit
                print('SHAKING')
                self.ble.connect()
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
        led1 = Led()
        led2 = Led()
        led3 = Led()
        leds = [led1, led2, led3]
        ledManager = LedsManager(ledStrip, leds)

        ############## BLE ##############
        
        ble = BluetoothManager(BLEAlertManager())

        homee = HomeeSystem(state=SystemOKState(), ledManager=ledManager, sensorManager=sensorManager, accel=mpu)
        homee.ble = ble

        return homee