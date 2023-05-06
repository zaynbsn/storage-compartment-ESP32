class BLEState:
    def description(self):
        pass

class BLENotConnectedState:

    def description(self):
        return "Err - Connexion failed"

class BLEConnectedState:

    def description(self):
        return "Connected"

class BLEAckFailedState:

    def description(self):
        return "Err - Ack failed"

class BLEAckSuccessState:

    def description(self):
        return "Ack suceeded"

class BLEWaitingForACKState:

    def description(self):
        return "Ack waiting"

class BLEIsReadyState:

    def description(self):
        return "BLE is ready"
