class SlotStatesProtocol:
    def __init__(self):
        pass

    def __str__(self):
        pass

class InitialState(SlotStatesProtocol):
    def __init__(self):
        pass

    def __str__(self):
        return 'InitialState'

class NotHereState(SlotStatesProtocol):
    def __init__(self):
        pass

    def __str__(self):
        return 'NotHereState'
    
class HereOKState(SlotStatesProtocol):
    def __init__(self):
        pass

    def __str__(self):
        return 'HereOKState'
    
class HereNOKState(SlotStatesProtocol):
    def __init__(self):
        pass

    def __str__(self):
        return 'HereNOKState'