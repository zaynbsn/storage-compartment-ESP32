class RfidManager:
    def __init__(self, boards):
        """
        @param: 
        boards est un dictionnaire { boardId: Rfid(), boardId: Rfid() ... }
        """
        self.boards = boards

    def readboard(self, rid=None):
        if not self.selectboard(rid):
            return None

        self.boards[rid].read()

    def selectboard(self, rid):
        if not rid in self.boards:
            return False

        return True
    
    def readAllBoards(self):
        for boardId in self.boards:
            self.boards[boardId].read()