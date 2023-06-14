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
    if self.context.isAllSlotFull():
      self.context.stop()
    self.context.checkOffSensor()

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
    if self.context.isAllSlotEmpty():
      self.context.stop()
    self.context.checkOffSensor()

class WarningState(SystemStates):
  def __init__(self):
    pass

  def run(self):
      self.context.readAllBoards()
      self.context.updateSlotState()
      self.context.updateLedStateWarning()
      self.context.changeLedsColors()
      if self.context.isAllSlotFull():
          self.context.stop()
      self.context.checkOffSensor()