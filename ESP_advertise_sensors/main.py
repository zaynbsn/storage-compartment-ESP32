from machine import Pin, SoftI2C, sleep
from time import sleep_ms
from accelerometer import accel
from math import fabs
from time import sleep

i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
mpu = accel(i2c)

from wireless_manager import *

class BLECallback(CommunicationCallback):
    def __init__(self, bleName='homee'):
        self.wirelessManager = None
        self.bleName = bleName

    def didReceiveCallback(self, value):
        print("received: " + value)
        if value == 'ACK':
            self.wirelessManager.sendDataToBLE('ACK')

wirelessManager = WirelessManager(bleCallback=BLECallback())

def shaking():
    values = mpu.get_acc_values()
    sumOfValues = 0
    for i in range(0,len(values)):
        sumOfValues += fabs(values[i])
    return sumOfValues >= 31000

def zoning(x,y,z, xTarget,yTarget,zTarget, tolerance = 2000):
    minX = xTarget - tolerance
    maxX = xTarget + tolerance
    minY = yTarget - tolerance
    maxY = yTarget + tolerance
    minZ = zTarget - tolerance
    maxZ = zTarget + tolerance
    if minX <= x <= maxX and minY <= y <= maxY and minZ <= z <= maxZ:
        return True
    else:
        return False

isDoorOpen = False
cooldown = 0

while True:
    wirelessManager.process()
    if not isDoorOpen:  
        # print('Distance:', distance, 'cm')
        if shaking():
            print("la porte s'ouvre", distance, "cm")
            if wirelessManager.isConnected():
                    wirelessManager.sendDataToWS("shaking")
            isDoorOpen = True
        else:
            pass
    else:
        cooldown+=1
        #print(cooldown)
    
    if cooldown >= 20:
        isDoorOpen = False
        cooldown = 0
    sleep_ms(200)
