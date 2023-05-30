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
class GreenState(LedStatesProtocol):
    def __init__(self):
        pass

    def getRGB(self):
        return (0, 255, 0)
class RedState(LedStatesProtocol):
    def __init__(self):
        pass

    def getRGB(self):
        return (255, 0, 0) 
class BlueState(LedStatesProtocol):
    def __init__(self):
        pass

    def getRGB(self):
        return (0, 0, 255)