from time import sleep
from ble_simple_central import *
from bleStates import *
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

  def updateState(self, newState):
    self.state = newState
    # ALERT si besoin
    if type(newState) in BluetoothManager.stateEmitingAlert:
      self.alertDelegate.newAlertState(self)

  def _on_scan(self, addr_type, addr, name):
    if addr_type is not None:
      print("Found peripheral:", addr_type, addr, name)
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

  def is_connected(self):
      return self.central.is_connected()
      
  def disconnect(self):
    self.central.disconnect()
    self.updateState(BLENotConnectedState())
    print("Disconnected")

  def _on_rx(self, v):
    print("RX", bytes(v))
    if type(self.state) ==  BLEWaitingForACKState:
      if bytes(v) == 'ACK':
        self.updateState(BLEAckSuccessState)

  def receive(self):
    self.central.on_notify(self._on_rx)

  def send(self, v):
    with_response = False
    if self.central.is_connected():
      print("TX", v)
      self.central.write(v, self.with_response)
      sleep(1 if with_response else 0)

  def checkAcknowledge(self):
    if self.is_connected():
      self.updateState(BLEWaitingForACKState())
      self.send('ACK')