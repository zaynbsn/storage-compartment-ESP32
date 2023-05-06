class SensorsStates:
  def __init__(self):
    pass

  def description(self):
    pass

class InitialState(SensorsStates):
  def __init__(self):
    pass

  def description(self):
    return "Initial State"

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

class NoValueState(SensorsStates):
  def __init__(self):
    pass

  def description(self):
    return "Err - NoValue Sensor"