from time import sleep
from tests.ledTests import LedTests


class CheckInitialState():

  def __init__(self):
    self.ledTests = LedTests()
    
  def runAllTests(self, ledManager):
      print('Bonjour, les tests vont commencer.')
      sleep(1)
      self._runLedTests(ledManager)
      sleep(1)

  def _runLedTests(self, ledManager):
    print('Verification des leds')
    self.ledTests.runLedTests(ledManager)
    print('Leds OK')

  def _runRfidTests(self, rfids):
    print('Verification des rfids')
    #testing rfids