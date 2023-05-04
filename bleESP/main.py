from bluetooth_manager import *

# remplacer central par inbstance BTManager
ble = BluetoothManager()
ble.connect()
ble.receive()