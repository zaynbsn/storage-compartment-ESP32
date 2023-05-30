from machine import Pin, SoftI2C, PWM
from leds.ledStates import *
from time import sleep

class Led:
    def __init__(self, led):
        self.led = led

        #self.setup()

        self.readerName = 'default'
        self.badgeId = 1

        self.currentState = InitialState()
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