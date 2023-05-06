from systemStates import *
from ble.bleStates import *
from time import sleep

class HomeeSystem:
    def __init__(self, state):
        self.state = state

    def updateState(self, newState):
        self.state = newState
    
    def checkSystemState(self, ble=None):
        print("checking system state")
        ### check everything ###
        self.updateState(SystemOKState())

        if ble:
          bleState = ble.getState()
          if type(bleState) != BLEIsReadyState:
              self.updateState(SystemNotOKState())