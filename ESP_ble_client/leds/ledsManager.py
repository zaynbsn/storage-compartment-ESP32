class LedsManager:
    def __init__(self, ledStrip, leds):
        self.ledStrip = ledStrip
        self.leds = leds
        self.RGB1 = (0,0,0)
        self.RGB2 = (0,0,0)
        self.RGB3 = (0,0,0)
        self.turnOffLeds()

    def getRGBs(self):
        self.RGB1 = self.leds[0].getRGB()
        self.RGB2 = self.leds[1].getRGB()
        self.RGB3 = self.leds[2].getRGB()

    def changeLedsColors(self):
        self.getRGBs()

        self.ledStrip[1] = self.RGB1
        self.ledStrip[2] = self.RGB1

        self.ledStrip[5] = self.RGB2
        self.ledStrip[6] = self.RGB2

        self.ledStrip[9] = self.RGB3
        self.ledStrip[10] = self.RGB3

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