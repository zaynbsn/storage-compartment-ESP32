from sensorStates import *

class SensorManager:
  def __init__(self, sensor):
    self.sensor = sensor
    self.currentState = InitialState()
    self.currentState.context = self

  def __updateState(self, newState):
    if type(self.currentState) != type(newState):
      self.currentState = newState
      self.currentState.context = self
      print("New State: ", self.currentState)

  def __stateChecking(self):
    if self.sensor.distance_cm() >= 50.0 or self.sensor.distance_cm() < 0.0 :
      self.__updateState(FarState())

    elif 0.0 < self.sensor.distance_cm() < 50.0:
      self.__updateState(NearState())

    else:
      self.__updateState(InitialState())

  def estimateDistance(self):
    print("Current State: ", self.currentState)
    print("distance: ",  self.sensor.distance_cm())
    self.__stateChecking()  