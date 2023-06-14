from math import fabs

class AccelStates:
  def __init__(self):
    pass

  def shaking(self):
    pass

class AccelInitialState(AccelStates):
  def __init__(self):
    pass

  def shaking(self):
    values = self.context.get_acc_values()
    sumOfValues = 0
    for i in range(0,len(values)):
        sumOfValues += fabs(values[i])
    if sumOfValues >= 31000:
        return True
    
    return False

class AccelNoReadState(AccelStates):
  def __init__(self):
    pass

  def shaking(self):
    pass