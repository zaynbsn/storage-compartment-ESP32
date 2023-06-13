from securityStates import *
from omiSystem import OmiSystem
from time import sleep_ms
from tests.checkList import *

omi = OmiSystem.setup()
#CheckInitialState().runAllTests(ledManager=omi.ledManager)

try:
  while True:

    # if type(omi.securityState) == SystemOKState:
    omi.run()
    sleep_ms(250)
    # else:
    #   break

except KeyboardInterrupt:
  omi.stop()
  print('Bye')