from time import sleep
from ble.bleSimpleCentral import *
from ble.bleStates import *
import bluetooth

class BluetoothManager():
  
  stateEmitingAlert = [BLENotConnectedState, BLEAckFailedState]

  def __init__(self, alertDelegate):
    self.ble = bluetooth.BLE()
    self.central = BLESimpleCentral(self.ble)
    self.not_found = False
    self.with_response = False
    self.alertDelegate = alertDelegate
    self.state = BLENotConnectedState()

  def getState(self):
    return self.state

  def updateState(self, newState):
    self.state = newState
    # ALERT si besoin
    if type(newState) in BluetoothManager.stateEmitingAlert:
      self.alertDelegate.newAlertState(self.state)

  def _on_scan(self, addr_type, addr, name):
    if addr_type is not None:
      print("Found peripheral:", addr_type, addr, name)
      if name == "homee":
          self.central.connect()
          self.updateState(BLEConnectedState())
          print('Connected')
    else:
      self.not_found = True
      print("No peripheral found.")
      self.updateState(BLENotConnectedState())

  def _scan(self):
    self.central.scan(callback=self._on_scan)

  def connect(self):
    self._scan()
    # Wait for connection...
    print("Scanning and connecting...")
    if self.not_found:
      if not self.central.is_connected():
        print("Fail to connect")
        self.updateState(BLENotConnectedState())
    self.receive()
    sleep(1)
    print("sleeping")
    self.checkAcknowledge()

  def is_connected(self):
      return self.central.is_connected()
      
  def disconnect(self):
    self.central.disconnect()
    self.updateState(BLENotConnectedState())
    print("Disconnected")

  def _on_rx(self, v):
    print("RX", bytes(v))
    if type(self.state) ==  BLEWaitingForACKState:
      if bytes(v).decode() == 'ACK':
        self.updateState(BLEAckSuccessState())
        self.updateState(BLEIsReadyState())
      else:
        self.updateState(BLEAckFailedState())

  def receive(self):
    self.central.on_notify(self._on_rx)

  def send(self, v, withResponse=False):
    with_response = withResponse
    if self.central.is_connected():
      print("TX", v)
      self.central.write(v, self.with_response)
      sleep(1 if with_response else 0)

  def checkAcknowledge(self, nbTry=3):
    count = 0
    while not self.is_connected():
      if count >= nbTry:
        print('no connexion to check ack')
        self.updateState(BLENotConnectedState())
        return
      print('waiting connexion')
      count += 1
      sleep(1)

    self.send('ACK')
    self.updateState(BLEWaitingForACKState())
    sleep(1)

  def checkBLE(self):
    if not self.is_connected():
      self.connect()
      sleep(1)
    if type(self.state) == BLEConnectedState:
      self.checkAcknowledge()
      sleep(1)
      if type(self.state) == BLEAckSuccessState:
        self.updateState(BLEIsReadyState())
      else:
        self.updateState(BLEAckFailedState())
    else:
      self.updateState(BLENotConnectedState())