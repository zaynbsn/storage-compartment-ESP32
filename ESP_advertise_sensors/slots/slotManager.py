class SlotManager:
    def __init__(self, slots):
        self.slots = slots

    def updateSlotsStates(self):
        for slot in self.slots:
            self.slots[slot].checkState()

    def updateLedsStates(self, omiState):
        for slot in self.slots:
            self.slots[slot].updateLedState(omiState)

    def turnOnLeds(self):
        for slot in self.slots:
            self.slots[slot].turnOnLeds()

    def getSlotsStates(self):
        slotsStates = []
        for slot in self.slots:
            slotsStates.append(type(self.slots[slot].currentState))

        return slotsStates

    def launchWarning(self):
        for slot in self.slots:
            self.slots[slot].warningSlot()

    def isAllSlotsFull(self):
        for slot in self.slots:
            if not self.slots[slot].checkIfFull():
                return False
        return True

    def isAllSlotEmpty(self):
        for slot in self.slots:
            if self.slots[slot].checkIfFull():
                return False
        return True