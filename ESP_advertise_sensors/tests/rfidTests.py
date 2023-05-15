from time import sleep

class RfidTests:
    
    def __init__(self):
        pass
    
    def runRfidTests(self, board):
        return board.readTest()