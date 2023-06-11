from leds.ledStates import *
from leds.pulse import Pulse
# from libs.threading import Thread

class LedsManager:
    def __init__(self, ledStrip, leds):
        self.ledStrip = ledStrip
        self.leds = leds
        self.rgbs = [(0, 0, 0), (0, 0, 0), (0, 0, 0)]
        self.turnOffLeds()

    def getRGBs(self):  
        for i in range(len(self.leds)):
            self.rgbs[i] = (self.leds[i].getRGB())

    def changeLedsColors(self):
        self.getRGBs()

        self.ledStrip[0] = self.rgbs[0]
        self.ledStrip[1] = self.rgbs[0]
        self.ledStrip[2] = self.rgbs[0]
        # self.ledStrip[3] = self.rgbs[0]

        self.ledStrip[4] = self.rgbs[1]
        self.ledStrip[5] = self.rgbs[1]
        self.ledStrip[6] = self.rgbs[1]
        self.ledStrip[7] = self.rgbs[1]

        # self.ledStrip[8] = self.rgbs[2]
        self.ledStrip[9] = self.rgbs[2]
        self.ledStrip[10] = self.rgbs[2]
        self.ledStrip[11] = self.rgbs[2]

        pixels = []
        for led in self.leds:
            if type(led.currentState) == WhitePulseState:
                slot = {}
                slot['color'] = 'white'
                slot['pixels'] = led.pixels
                pixels.append(slot)
            elif type(led.currentState) == RedPulseState:
                slot = {}
                slot['color'] = 'red'
                slot['pixels'] = led.pixels
                pixels.append(slot)
        print(pixels)

        if len(pixels) > 0:
            # ledThread = Thread(target=Pulse.animate, args=(self.ledStrip, pixels, 1))
            # ledThread.start()
            Pulse.animate(ledsStrip=self.ledStrip, pixels=pixels, duration=5)

    def turnOnLeds(self):
        self.ledStrip.write()

    def turnOffLeds(self):
        self.ledStrip.fill((0, 0, 0))
        self.ledStrip.write()

    def run(self):
        self.changeLedsColors()
        self.turnOnLeds()