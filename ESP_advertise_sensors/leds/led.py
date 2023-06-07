from machine import Pin, SoftI2C, PWM
from leds.ledStates import *

class Led:
    def __init__(self, pixels):
        self.pixels = pixels
        self.currentState = LedInitialState()
        self.currentState.context = self

    def updateState(self, newState):
        if type(self.currentState) != type(newState):
            self.currentState = newState
            self.currentState.context = self
            print("New Led State: ", self.currentState)

    def getRGB(self):
        return self.currentState.getRGB()

    def turnOnLed(self):
        self.currentState.turnOnLed()