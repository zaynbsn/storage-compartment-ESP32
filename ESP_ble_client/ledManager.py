from machine import Pin, SoftI2C, PWM

class LedManager:
    def __init__(self):
        self.pwm_pins = [23,22,21]
        
        self.RED = 0
        self.GREEN = 1
        self.BLUE = 2

        self.pwms = [PWM(Pin(self.pwm_pins[self.RED])),PWM(Pin(self.pwm_pins[self.GREEN])),
                        PWM(Pin(self.pwm_pins[self.BLUE]))] 
    
    def setup(self):
        [pwm.freq(1000) for pwm in self.pwms]

    def deinit_pwm_pins(self):
        self.pwms[self.RED].deinit()
        self.pwms[self.GREEN].deinit()
        self.pwms[self.BLUE].deinit()

    def displayRed(self):
        self.pwms[self.RED].duty_u16(65535)
        self.pwms[self.GREEN].duty_u16(0)
        self.pwms[self.BLUE].duty_u16(0)
        
    def displayGreen(self):
        self.pwms[self.RED].duty_u16(0)
        self.pwms[self.GREEN].duty_u16(65535)
        self.pwms[self.BLUE].duty_u16(0)
        
    def displayBlue(self):
        self.pwms[self.RED].duty_u16(0)
        self.pwms[self.GREEN].duty_u16(0)
        self.pwms[self.BLUE].duty_u16(65535)