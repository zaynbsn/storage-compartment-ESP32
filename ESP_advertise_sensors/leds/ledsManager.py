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

    def turnOnLeds(self):
        # violet (129, 14, 219)
        # orange (220, 90, 0)
        self.ledStrip.write()

    def turnOffLeds(self):
        self.ledStrip.fill((0, 0, 0))
        self.ledStrip.write()
    
    def run(self):
        self.changeLedsColors()
        self.turnOnLeds()