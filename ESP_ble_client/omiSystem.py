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
from button.buttonManager import *
from systemStates import *
from neopixel import NeoPixel
from time import sleep_ms
from machine import Timer


class OmiSystem:
    def __init__(self, state, securityState, ledManager, sensorManager, accel):
        self.state = state
        self.securityState = securityState

        self.ledManager = ledManager
        self.sensorManager = sensorManager
        self.accel = accel
        self.ble = None
        self.timer = Timer(0)

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
        if str == 'off':
            self.ledManager.turnOffLeds()
            return

        self.decodedStr = str.split("||")
        print(self.decodedStr)
        if type(self.state) == EntryState:
            self.ledManager.turnOffLeds()
            return

        if self.decodedStr == ['0', '0', '0']:
            for i in range(len(self.decodedStr)):
                state = int(self.decodedStr[i])
                self.decodedStr[i] = LedInitialState()

        elif self.decodedStr == ['1', '1', '1']:
            for i in range(len(self.decodedStr)):
                state = int(self.decodedStr[i])
                self.decodedStr[i] = RedState()
        else:
            for i in range(len(self.decodedStr)):
                state = int(self.decodedStr[i])
                if state == 0:
                    self.decodedStr[i] = LedInitialState()
                elif state == 1:
                    self.decodedStr[i] = WhitePulseState()

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
        # todo timer
        

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
    
    def checkOffSensor(self):
        self.sensorManager.estimateDistance()
        if type(self.sensorManager.currentState) == VeryNearState:
            self.stop()
            self.sensorManager.updateState(SensorNoReadState())
            def cb(t):
                self.sensorManager.updateState(SensorInitialState())
            self.timer.init(mode=Timer.ONE_SHOT, period=2000, callback=cb)

    def run(self):
        if self.ble.is_connected():
            self.launchCooldown()
            self.checkOffSensor()
            # self.ledManager.run()
        else:
            self.checkSensors()
        self.checkSystemState(sensor=True)

    def stop(self):
        self.ble.send("off")
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

        ############# BLE ##############
        
        ble = BluetoothManager(BLEAlertManager())

        omi = OmiSystem(state=ReadSensorState(), securityState=SystemOKState(), ledManager=ledManager, sensorManager=sensorManager, accel=mpu)
        omi.ble = ble
        ble.omi = omi

        return omi