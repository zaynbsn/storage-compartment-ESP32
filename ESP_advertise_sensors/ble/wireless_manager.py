from systemStates import *
class CommunicationCallback:
    def __init__(self):
        pass
    
    def connectionCallback(self):
        print("connected")
    
    def disconnectionCallback(self):
        print("disconnected")
    
    def didReceiveCallback(self, value):
        print("received: " + value)

class WirelessManager:
    
    def __init__(self, bleCallback = None, wsCallback = None):
        self.bleCallback = bleCallback
        self.bleCallback.wirelessManager = self
        self.wsCallback = wsCallback
        self.homee = None

        self.receivedState = SystemInitialState()
        
        if self.bleCallback != None:
            from ble.ble_simple_peripheral import bluetooth, BLESimplePeripheral
            self.ble = bluetooth.BLE()
            self.blePeripheral = BLESimplePeripheral(self.ble, name=self.bleCallback.bleName)
            self.blePeripheral.on_write(self.bleCallback.didReceiveCallback)

    def isConnected(self):
        if self.bleCallback != None:
            return self.blePeripheral.is_connected()

    def sendDataToBLE(self, data):
        if self.bleCallback != None:
            if self.blePeripheral.is_connected():
                self.blePeripheral.send(data)