from time import sleep
from tests.ledTests import LedTests
from tests.rfidTests import RfidTests

class CheckInitialState():

  def __init__(self):
    self.ledTests = LedTests()
    self.rfidTests = RfidTests()

    
  def runAllTests(self, ledManager=None, rfids=None):
      print('Bonjour, les tests vont commencer.')
      # sleep(1)
      self._runLedTests(ledManager)
      sleep(1)
      self._runRfidTests(rfids)
      sleep(1)
      print("Tests terminés. Lecture des rfid en cours")

  def _runLedTests(self, ledManager):
    print('Verification des leds')
    self.ledTests.runLedTests(ledManager)
    print('Leds OK')

  def _runRfidTests(self, rfids):
    print('Verification des rfids')
    for boardId in rfids:
      res = False
      print('posez un badge sur le lecteur rfid :', rfids[boardId].rid)
      while res is not True:
        res = self.rfidTests.runRfidTests(rfids[boardId])