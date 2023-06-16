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
    print(sumOfValues)
    if sumOfValues >= 23500 or sumOfValues <= 22200:
        return True
    
    return False

class AccelNoReadState(AccelStates):
  def __init__(self):
    pass

  def shaking(self):
    pass