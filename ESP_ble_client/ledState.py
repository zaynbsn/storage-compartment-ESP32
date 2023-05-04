class LedStateProtocol:
    def __init__(self) -> None:
        pass

    def __str__(self):
        pass
    
    def turnOnLed(self):
        pass
    
class InitialState(LedStateProtocol):
    def __init__(self) -> None:
        pass

    def __str__(self):
        return "InitialState"
    
    def turnOnLed(self):
        self.context.pwms[self.context.RED].duty(0)
        self.context.pwms[self.context.GREEN].duty(0)
        self.context.pwms[self.context.BLUE].duty(0)
    
class FullState(LedStateProtocol):
    def __init__(self) -> None:
        pass

    def __str__(self):
        return "FullState"
    
    def turnOnLed(self):
        self.context.pwms[self.context.RED].duty(0)
        self.context.pwms[self.context.GREEN].duty(255)
        self.context.pwms[self.context.BLUE].duty(0)
    
class EmptyState(LedStateProtocol):
    def __init__(self) -> None:
        pass

    def __str__(self):
        return "EmptyState"
    
    def turnOnLed(self):
        self.context.pwms[self.context.RED].duty(255)
        self.context.pwms[self.context.GREEN].duty(0)
        self.context.pwms[self.context.BLUE].duty(0)
    
class WrongItemState(LedStateProtocol):
    def __init__(self) -> None:
        pass

    def __str__(self):
        return "WrongItemState"
    
    def turnOnLed(self):
        self.context.pwms[self.context.RED].duty(0)
        self.context.pwms[self.context.GREEN].duty(0)
        self.context.pwms[self.context.BLUE].duty(255)