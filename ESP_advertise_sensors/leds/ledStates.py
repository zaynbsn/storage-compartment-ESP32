class LedStatesProtocol:
    def __init__(self):
        pass

    def getRGB(self):
        pass
class LedInitialState(LedStatesProtocol):
    def __init__(self):
        pass

    def getRGB(self):
        return (0, 0, 0)  
class WhiteState(LedStatesProtocol):
    def __init__(self):
        pass

    def getRGB(self):
        return (255, 255, 255)
class RedState(LedStatesProtocol):
    def __init__(self):
        pass

    def getRGB(self):
        return (128, 0, 128)
class WhitePulseState(LedStatesProtocol):
    def __init__(self):
        pass

    def getRGB(self):
        # return (255, 255, 255)
        return (0, 0, 0)
class RedPulseState(LedStatesProtocol):
    def __init__(self):
        pass

    def getRGB(self):
        # return (255, 0, 0)
        return (0, 0, 0)
class GreenState(LedStatesProtocol):
    def __init__(self):
        pass

    def getRGB(self):
        return (0, 255, 0) #green
class BlueState(LedStatesProtocol):
    def __init__(self):
        pass

    def getRGB(self):
        return (0, 0, 255)
