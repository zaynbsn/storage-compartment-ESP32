class SlotManager:
    def __init__(self, slots):
        self.slots = slots

    def updateSlotsStates(self):
        for slot in self.slots:
            self.slots[slot].checkState()

    def updateLedsStates(self):
        for slot in self.slots:
            self.slots[slot].updateLedState()

    def turnOnLeds(self):
        for slot in self.slots:
            self.slots[slot].turnOnLeds()

    def getSlotsStates(self):
        slotsStates = []
        for slot in self.slots:
            slotsStates.append(type(self.slots[slot].currentState))

        return slotsStates