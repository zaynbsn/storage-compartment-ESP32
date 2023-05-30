from systemStates import *
from ble.bleStates import *
from sensor.sensorStates import *
from leds.ledStates import *
from time import sleep

class HomeeSystem:
    def __init__(self, state, ledManager):
        self.state = state
        self.ledManager = ledManager
        self.decodedStr = ''

    def updateState(self, newState):
        self.state = newState

    def checkSystemState(self, ble=None, sensor=None):
        # print("checking system state")
        ### check everything ###
        self.updateState(SystemOKState())

        if ble:
            bleState = ble.getState()
            if type(bleState) != BLEIsReadyState:
                self.updateState(SystemNotOKState())

        if sensor:
            sensorState = sensor.getState()
            if type(sensorState) == NoValueState:
                self.updateState(SystemNotOKState())

    def decodeString(self, str):
        self.decodedStr = str.split("||")
        for i in range(len(self.decodedStr)):
            state = int(self.decodedStr[i])
            if state == 0:
                self.decodedStr[i] = RedState()
            elif state == 1:
                self.decodedStr[i] = GreenState()
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

    def stop(self):
        self.ledManager.turnOffLeds()
