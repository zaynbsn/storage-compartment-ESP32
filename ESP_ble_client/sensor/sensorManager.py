from sensor.sensorStates import *

class SensorManager:

  stateEmitingAlert = [NoValueState]

  def __init__(self, sensor, alertDelegate):
    self.sensor = sensor
    self.currentState = SensorInitialState()
    self.alertDelegate = alertDelegate
    self.currentState.context = self

  def getState(self):
    return self.currentState  

  def updateState(self, newState):
    if type(self.currentState) != type(newState):
      self.currentState = newState
      self.currentState.context = self
      # print("New State: ", self.currentState)

  def __stateChecking(self):
    if self.sensor.distance_cm() >= 30 or self.sensor.distance_cm() < 0 :
      self.updateState(FarState())

    elif 5 < self.sensor.distance_cm() < 30:
      self.updateState(NearState())
    
    elif 0 < self.sensor.distance_cm() < 5:
      self.updateState(VeryNearState())

    else:
      self.updateState(SensorInitialState())

  def estimateDistance(self):
    if type(self.currentState) != SensorNoReadState: 
      print(self.sensor.distance_cm())
      if self.sensor.distance_cm() == (-0.03436426):
        self.updateState(NoValueState())
        self.alertDelegate.newAlertState(self.currentState)
      else:
        self.__stateChecking()

  def getDistance(self):
    print(self.sensor.distance_cm())
    return self.sensor.distance_cm()