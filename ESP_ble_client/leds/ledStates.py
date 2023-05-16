class LedStatesProtocol:
    def __init__(self) -> None:
        pass

    def __str__(self):
        pass
    
    def turnOnLed(self):
        pass
    
class InitialState(LedStatesProtocol):
    def __init__(self) -> None:
        pass

    def turnOnLed(self):
        self.context.pwms[self.context.RED].duty(255)
        self.context.pwms[self.context.GREEN].duty(255)
        self.context.pwms[self.context.BLUE].duty(255)
    
class GreenState(LedStatesProtocol):
    def __init__(self) -> None:
        pass

    def turnOnLed(self):
        self.context.pwms[self.context.RED].duty(0)
        self.context.pwms[self.context.GREEN].duty(255)
        self.context.pwms[self.context.BLUE].duty(0)
    
class RedState(LedStatesProtocol):
    def __init__(self) -> None:
        pass
    
    def turnOnLed(self):
        self.context.pwms[self.context.RED].duty(255)
        self.context.pwms[self.context.GREEN].duty(0)
        self.context.pwms[self.context.BLUE].duty(0)
    
class BlueState(LedStatesProtocol):
    def __init__(self) -> None:
        pass

    def turnOnLed(self):
        self.context.pwms[self.context.RED].duty(0)
        self.context.pwms[self.context.GREEN].duty(0)
        self.context.pwms[self.context.BLUE].duty(255)