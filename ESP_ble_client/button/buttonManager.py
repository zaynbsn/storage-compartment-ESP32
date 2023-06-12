class ButtonManager:
  def __init__(self, button):
    self.button = button

  def isPressed(self):
    if self.button.value == 1:
      return True
    return False