from securityStates import *
from homeeSystem import HomeeSystem
from time import sleep_ms
from tests.checkList import *

homee = HomeeSystem.setup()
#CheckInitialState().runAllTests(ledManager=homee.ledManager)

while True:
  try:
    if type(homee.securityState) == SystemOKState:
      homee.run()
      sleep_ms(250)
    else:
      break

  except KeyboardInterrupt:
    homee.stop()
    raise