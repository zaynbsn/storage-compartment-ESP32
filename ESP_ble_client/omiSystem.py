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
from accelerometer.accelerometerStates import *
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
                self.decodedStr[i] = RedPulseState()
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

    def turnOffLed(self):
        self.ledManager.turnOffLeds()
    
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
            self.timeoutSensors(5)
        elif self.accel.shaking():
            self.accelFirst()
            self.timeoutSensors(5)
    
    def checkOffSensor(self):
        self.sensorManager.estimateDistance()
        if type(self.sensorManager.currentState) == VeryNearState:
            self.stop()
            
    def timeoutSensors(self, t=10):
        print('timeout sensors', t, 'seconds')
        # t in seconds so convert to milliseconds
        t = t*1000
        self.sensorManager.updateState(SensorNoReadState())
        self.accel.updateState(AccelNoReadState())
        def cb(t):
            self.sensorManager.updateState(SensorInitialState())
            self.accel.updateState(AccelInitialState())
        self.timer.init(mode=Timer.ONE_SHOT, period=t, callback=cb)

    def run(self):
        if self.ble.is_connected():
            self.checkSystemState(ble=True)
            self.checkOffSensor()
        else:
            self.checkSensors()

    def stop(self):
        self.ble.send('off')
        self.turnOffLed()
        self.ble.disconnect()
        self.timeoutSensors()

    @staticmethod
    def setup():
        ############# accel ##############
        i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
        accel = Accel(i2c)

        ############# sensor ##############
        sensor = HCSR04(trigger_pin=14, echo_pin=12, echo_timeout_us=10000)
        sensorManager = SensorManager(sensor, SensorAlertManager())

        ############# ledsStrip ##############
        ledStrip = NeoPixel(Pin(23), 6)
        led1 = Led([0, 1])
        led2 = Led([2, 3])
        led3 = Led([4, 5])
        leds = [led1, led2, led3]
        ledManager = LedsManager(ledStrip, leds)

        ############# BLE ##############
        
        ble = BluetoothManager(BLEAlertManager())

        omi = OmiSystem(state=ReadSensorState(), securityState=SystemOKState(), ledManager=ledManager, sensorManager=sensorManager, accel=accel)
        omi.ble = ble
        ble.omi = omi

        return omi