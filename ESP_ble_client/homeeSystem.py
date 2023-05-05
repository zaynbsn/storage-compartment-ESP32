from systemStates import *
from bleStates import *
from time import sleep

class HomeeSystem:
    def __init__(self, state):
        self.state = state

    def updateState(self, newState):
        self.state = newState
    
    def checkSystemState(self, ble):
        print("checking system state")
        ### check everything ###
        ble.checkBLE()
        sleep(3)
        if type(ble.state) == BLEIsReadyState:
            self.updateState(SystemOKState())
        else:
            self.updateState(SystemNotOKState())