class AlertDelegate:

    def newAlertState(self,bleObj):
        pass
        

class BLEAlertManager(AlertDelegate):
    
    # def __init__(self, functionToCall):
    #     self.localFunctionToCall = functionToCall
    
    def newAlertState(self, bleState):
        print(bleState.description())
        #self.localFunctionToCall(bleObj.state)
