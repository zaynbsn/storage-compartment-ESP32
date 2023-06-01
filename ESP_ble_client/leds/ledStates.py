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
        return (42, 169, 236) #blue
        # return (0, 255, 0)
class RedState(LedStatesProtocol):
    def __init__(self):
        pass

    def getRGB(self):
        return (255, 177, 59) #orange 
        # return (255, 0, 0)
class BlueState(LedStatesProtocol):
    def __init__(self):
        pass

    def getRGB(self):
        return (148, 127, 254) #purple
        # return (0, 0, 255)