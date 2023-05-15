from time import sleep_ms
from machine import Pin, SPI
from libs.mfrc522 import MFRC522

class NFCBoard:
    def __init__(self, sda, sck, mosi, miso, rid='board'):
        self.rid = rid
        self.spi = SPI(baudrate=100000, polarity=0, phase=0, sck=sck, mosi=mosi, miso=miso)
        self.sda = sda

    def read(self):
        self.reader = MFRC522(self.spi, self.sda)
        uid = ""
        (stat, tag_type) = self.reader.request(self.reader.REQIDL)
        if stat == self.reader.OK:
            (stat, raw_uid) = self.reader.anticoll()
            if stat == self.reader.OK:
                uid = ("0x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3]))
                print(self.rid, uid)
                sleep_ms(100)

    def readTest(self):
        self.reader = MFRC522(self.spi, self.sda)
        uid = ""
        (stat, tag_type) = self.reader.request(self.reader.REQIDL)
        if stat == self.reader.OK:
            (stat, raw_uid) = self.reader.anticoll()
            if stat == self.reader.OK:
                uid = ("0x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3]))
                print(self.rid, uid)
                sleep_ms(100)
                return True
        return False