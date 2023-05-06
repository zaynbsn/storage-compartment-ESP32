class AlertDelegate:

    def newAlertState(self,bleObj):
        pass
        

class BLEAlertManager(AlertDelegate):
    
    # def __init__(self, functionToCall):
    #     self.localFunctionToCall = functionToCall
    
    def newAlertState(self, bleState):
        print(bleState.description())
        #self.localFunctionToCall(bleObj.state)

class SensorAlertManager(AlertDelegate):
    
    # def __init__(self, functionToCall):
    #     self.localFunctionToCall = functionToCall
    
    def newAlertState(self, bleState):
        print(bleState.description())
        print("vérifiez les branchements")
        #self.localFunctionToCall(bleObj.state)
