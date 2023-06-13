class SensorsStates:
  def __init__(self):
    pass

  def description(self):
    pass

class SensorInitialState(SensorsStates):
  def __init__(self):
    pass

  def description(self):
    return "Initial State"

class SensorNoReadState(SensorsStates):
  def __init__(self):
    pass

  def description(self):
    return "Sensor No Read State"

class FarState(SensorsStates):
  def __init__(self):
    pass

  def description(self):
    return "Far State"


class NearState(SensorsStates):
  def __init__(self):
    pass

  def description(self):
    return "Near State"
  
class VeryNearState(SensorsStates):
  def __init__(self):
    pass

  def description(self):
    return "Near State"
class NoValueState(SensorsStates):
  def __init__(self):
    pass

  def description(self):
    return "Err - NoValue Sensor"