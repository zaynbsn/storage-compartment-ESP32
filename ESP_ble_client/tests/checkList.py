from time import sleep
from tests.ledTests import LedTests


class CheckInitialState():

  def __init__(self):
    self.ledTests = LedTests()
    
  def runAllTests(self, leds):
      print('Bonjour, les tests vont commencer.')
      sleep(1)
      self._runLedTests(leds)
      sleep(1)
      #rfid tests
      sleep(1)

  def _runLedTests(self, leds):
    print('Verification des leds')
    for led in leds:
        self.ledTests.runLedTests(led)
    print('Leds OK')

  def _runRfidTests(self, rfids):
    print('Verification des rfids')
    #testing rfids