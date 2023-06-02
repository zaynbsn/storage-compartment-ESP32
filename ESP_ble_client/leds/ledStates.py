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
        # return (42, 169, 236) #blue
        return (0, 255, 0) #green
class RedState(LedStatesProtocol):
    def __init__(self):
        pass

    def getRGB(self):
        # return (255, 40, 0) #orange
        # return (128, 0, 128) #purple
        return (42, 169, 236) #blue
        # return (255, 0, 0)
class BlueState(LedStatesProtocol):
    def __init__(self):
        pass

    def getRGB(self):
        # return (128, 0, 128) #purple
        return (128, 0, 128) #purple
        # return (42, 169, 236) #blue
        # return (0, 0, 255)