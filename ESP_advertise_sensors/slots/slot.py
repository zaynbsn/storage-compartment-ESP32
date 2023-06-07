from slots.slotStates import *
from rfids.rfidStates import *
from leds.ledStates import *
from systemStates import *

class Slot:
    def __init__(self, rfid, badgeId, led):
        self.rfid = rfid
        self.badgeId = badgeId
        self.led = led
        self.currentState = InitialState()
        self.currentState.context = self

    def updateState(self, newState):
        if type(self.currentState) != type(newState):
            self.currentState = newState
            self.currentState.context = self
            print("New Slot State: ", self.currentState)

    def checkState(self):
        if type(self.rfid.currentState) == NoReadState:
            self.updateState(NotHereState())
        elif self.rfid.badgeId == self.badgeId:
            self.updateState(HereOKState())
        else:
            self.updateState(HereNOKState())

    def updateLedState(self, homeeState):
        if type(homeeState) == ExitState:
            if type(self.currentState) == NotHereState:
                self.led.updateState(LedInitialState())

            elif type(self.currentState) == HereOKState:
                self.led.updateState(WhitePulseState())

            elif type(self.currentState) == HereNOKState:
                self.led.updateState(RedState())

        elif type(homeeState) == EntryState:
            if type(self.currentState) == NotHereState:
                self.led.updateState(WhitePulseState())

            elif type(self.currentState) == HereOKState:
                self.led.updateState(LedInitialState())

            elif type(self.currentState) == HereNOKState:
                self.led.updateState(RedState())
        else:
            return