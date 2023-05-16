class SlotManager:
    def __init__(self, slots):
        self.slots = slots

    def updateSlotsStates(self):
        for slot in self.slots:
            self.slots[slot].checkState()

    def updateLedsStates(self):
        for slot in self.slots:
            self.slots[slot].updateLedState()
