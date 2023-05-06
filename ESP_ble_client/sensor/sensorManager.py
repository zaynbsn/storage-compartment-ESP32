from sensor.sensorStates import *

class SensorManager:

  stateEmitingAlert = [NoValueState]

  def __init__(self, sensor, alertDelegate):
    self.sensor = sensor
    self.currentState = InitialState()
    self.alertDelegate = alertDelegate
    self.currentState.context = self

  def getState(self):
    return self.currentState  

  def __updateState(self, newState):
    if type(self.currentState) != type(newState):
      self.currentState = newState
      self.currentState.context = self
      # print("New State: ", self.currentState)

  def __stateChecking(self):
    if self.sensor.distance_cm() >= 30 or self.sensor.distance_cm() < 0 :
      self.__updateState(FarState())

    elif 0 < self.sensor.distance_cm() < 30:
      self.__updateState(NearState())

    else:
      self.__updateState(InitialState())

  def estimateDistance(self):
    # print("Current State: ", self.currentState)
    print(self.sensor.distance_cm())
    if self.sensor.distance_cm() == (-0.03436426):
      self.__updateState(NoValueState())
      self.alertDelegate.newAlertState(self.currentState)
    else:
      self.__stateChecking()