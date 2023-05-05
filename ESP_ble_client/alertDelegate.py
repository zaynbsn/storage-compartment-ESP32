class AlertDelegate:

    def newAlertState(self,bleObj):
        pass
        

class BLEAlertManager(AlertDelegate):
    
    # def __init__(self, functionToCall):
    #     self.localFunctionToCall = functionToCall
    
    def newAlertState(self,bleObj):
        print(bleObj.state.description())
        #self.localFunctionToCall(bleObj.state)
