class BLEState:
    def description():
        pass

class BLENotConnectedState:

    def __str__(self):
        return "BLENotConnectedState"

    def description(self):
        return "Connexion failed"

class BLEConnectedState:

    def __str__(self):
        return "BLEConnectedState"

    def description(self):
        return "Connected"

class BLEAckFailedState:

    def __str__(self):
        return "BLEAckFailedState"

    def description(self):
        return "Ack failed"

class BLEAckSuccessState:

    def __str__(self):
        return "BLEAckSuccessState"

    def description(self):
        return "Ack suceeded"

class BLEWaitingForACKState:

    def __str__(self):
        return "BLEWaitingForACKState"

    def description(self):
        return "Ack waiting"

class BLEISReadyState:

    def __str__(self):
        return "BLEISReadyState"

    def description(self):
        return "BLE is ready"
