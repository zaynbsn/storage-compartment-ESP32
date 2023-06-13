class SystemStates:
  def __init__(self):
    pass

  def run(self):
    pass

class SystemInitialState(SystemStates):
  def __init__(self):
    pass

  def run(self):
    self.context.updateState(self.context.wirelessManager.receivedState)

class EntryState(SystemStates):
  def __init__(self):
    pass

  def run(self):
    self.context.readAllBoards()
    self.context.updateSlotState()
    self.context.updateLedState()
    # send ble
    self.context.sendToBle(bypass=True)
    self.context.changeLedsColors()
    self.context.turnOnLeds()

class ExitState(SystemStates):
  def __init__(self):
    pass

  def run(self):
    self.context.readAllBoards()
    self.context.updateSlotState()
    self.context.updateLedState()
    # send ble
    self.context.sendToBle(bypass=True)
    self.context.changeLedsColors()
    self.context.turnOnLeds()

class WarningState(SystemStates):
  def __init__(self):
    pass

  def run(self):
      self.context.readAllBoards()
      self.context.updateSlotState()
      self.context.updateLedStateWarning()
      self.context.changeLedsColors()
      print('isSlotFull', self.context.isAllSlotFull())
      if self.context.isAllSlotFull():
          self.context.updateState(SystemInitialState())
          self.context.sendOff()