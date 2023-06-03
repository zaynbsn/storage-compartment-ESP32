class LedStatesProtocol:
    def __init__(self):
        pass

    def getRGB(self):
        pass
class InitialState(LedStatesProtocol):
    def __init__(self):
        pass

    def getRGB(self):
        return (0, 0, 0)   
class WhiteState(LedStatesProtocol):
    def __init__(self):
        pass

    def getRGB(self):
        return (255, 255, 255) #green
class RedState(LedStatesProtocol):
    def __init__(self):
        pass

    def getRGB(self):
        return (255, 0, 0)
class WhiteWaveState(LedStatesProtocol):
    def __init__(self):
        pass

    def getRGB(self):
        return (255, 255, 255)
class RedWaveState(LedStatesProtocol):
    def __init__(self):
        pass

    def getRGB(self):
        return (255, 0, 0)

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
