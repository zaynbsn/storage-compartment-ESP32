from time import sleep_ms
from machine import Timer
from pulse.pulseStates import *

class Pulse:
  def __init__(self):
    self.timer = Timer(1)
    self.period = 5
    self.increment = True
    self.currentState = PulseInitialState()

  def updateState(self, newState):
    if type(self.currentState) != type(newState):
        self.currentState = newState
        self.currentState.context = self
        print("New State: ", self.currentState)

  def pulseColor(self, i, ledsStrip, pixels, exit):
    for slot in pixels:
      if slot['color'] == 'white':
        for pixel in slot['pixels']:
          ledsStrip[pixel] = (i, i, i)
      else:
        for pixel in slot['pixels']:
          ledsStrip[pixel] = (i, 0, i)

    ledsStrip.write()

    if exit:
      return

    if 0 <= i <= 128 and self.increment:
      if i == 128:
        self.increment = False
        i -= 1
      else:
        i += 1
    elif 0 <= i <= 128 and not self.increment:
      if i == 0:
        exit = True
        self.increment = True
        self.updateState(PulseInitialState())
      else:
        i -= 1

    self.timer.init(mode=Timer.ONE_SHOT, period=self.period, callback=lambda b:self.pulseColor(i=i, ledsStrip=ledsStrip, pixels=pixels, exit=exit))

  def animate(self, ledsStrip, pixels, duration=1):
    '''
    @params : {
      pixels: {
        {color : 'red', pixels: [0, 1, 2] }, 
        {color : 'white', pixels: [3, 4, 5, 6] }
      }
    }
    '''
    while duration > 0:
        self.updateState(PulseAnimationState())
        i=0
        self.timer.init(mode=Timer.ONE_SHOT, period=self.period, callback=lambda b:self.pulseColor(i=i, ledsStrip=ledsStrip, pixels=pixels, exit=False))

        duration -= 1