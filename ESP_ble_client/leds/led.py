from machine import Pin, SoftI2C, PWM
from leds.ledStates import *
from time import sleep

class Led:
    def __init__(self, pins=[23,22,21]):
        self.pwm_pins = pins
        self.RED = 0
        self.GREEN = 1
        self.BLUE = 2
        self.pwms = []

        self.setup()

        self.readerName = 'default'
        self.badgeId = 1

        self.currentState = InitialState()
        self.currentState.context = self

    def setup(self):
        self.pwms = [
                        PWM(Pin(self.pwm_pins[self.RED])),
                        PWM(Pin(self.pwm_pins[self.GREEN])),
                        PWM(Pin(self.pwm_pins[self.BLUE]))
                    ]

        [pwm.freq(60) for pwm in self.pwms]

    def updateState(self, newState):
        if type(self.currentState) != type(newState):
            self.currentState = newState
            self.currentState.context = self
            print("New State: ", self.currentState)

    def checkState(self):
        pass

    def turnOnLed(self):
        self.currentState.turnOnLed()
    
    def turnOffLed(self):
        self.pwms[self.RED].duty(0)
        self.pwms[self.GREEN].duty(0)
        self.pwms[self.BLUE].duty(0)

    def deinit_pwm_pins(self):
        self.pwms[self.RED].deinit()
        self.pwms[self.GREEN].deinit()
        self.pwms[self.BLUE].deinit()