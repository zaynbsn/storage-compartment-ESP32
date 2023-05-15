import machine

class accel():
    def __init__(self, i2c, addr=0x68):
        self.iic = i2c
        self.addr = addr
        self.iic.start()
        self.iic.writeto(self.addr, bytearray([107, 0]))
        self.iic.stop()

    def get_raw_values(self):
        self.iic.start()
        a = self.iic.readfrom_mem(self.addr, 0x3B, 14)
        self.iic.stop()
        return a

    def get_ints(self):
        b = self.get_raw_values()
        c = []
        for i in b:
            c.append(i)
        return c

    def bytes_toint(self, firstbyte, secondbyte):
        if not firstbyte & 0x80:
            return firstbyte << 8 | secondbyte
        return - (((firstbyte ^ 255) << 8) | (secondbyte ^ 255) + 1)

    def get_values(self):
        raw_ints = self.get_raw_values()
        vals = {}
        vals["AcX"] = self.bytes_toint(raw_ints[0], raw_ints[1])
        vals["AcY"] = self.bytes_toint(raw_ints[2], raw_ints[3])
        vals["AcZ"] = self.bytes_toint(raw_ints[4], raw_ints[5])
        vals["Tmp"] = self.bytes_toint(raw_ints[6], raw_ints[7]) / 340.00 + 36.53
        vals["GyX"] = self.bytes_toint(raw_ints[8], raw_ints[9])
        vals["GyY"] = self.bytes_toint(raw_ints[10], raw_ints[11])
        vals["GyZ"] = self.bytes_toint(raw_ints[12], raw_ints[13])
        return vals  # returned in range of Int16
        # -32768 to 32767
    
    def get_acc_values(self):
        raw_ints = self.get_raw_values()
        vals = []
        vals.append(self.bytes_toint(raw_ints[0], raw_ints[1]))
        vals.append(self.bytes_toint(raw_ints[2], raw_ints[3]))
        vals.append(self.bytes_toint(raw_ints[4], raw_ints[5]))
        return vals

    def val_test(self):  # ONLY FOR TESTING! Also, fast reading sometimes crashes IIC
        from time import sleep
        while 1:
            print(self.get_values())
            sleep(0.05)

################             ################
################ use exemple ################
################             ################

# from machine import Pin, SoftI2C, sleep
# from accelerometer import accel
# from math import fabs


# i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
# mpu = accel(i2c)

# def shaking():
#     values = mpu.get_acc_values()
#     sumOfValues = 0
#     for i in range(0,len(values)):
#         sumOfValues += fabs(values[i])
#     return sumOfValues >= 31000

# def zoning(x,y,z, xTarget,yTarget,zTarget, tolerance = 2000):
#     minX = xTarget - tolerance
#     maxX = xTarget + tolerance
#     minY = yTarget - tolerance
#     maxY = yTarget + tolerance
#     minZ = zTarget - tolerance
#     maxZ = zTarget + tolerance
#     if minX <= x <= maxX and minY <= y <= maxY and minZ <= z <= maxZ:
#         return True
#     else:
#         return False

# isDoorOpen = False
# cooldown = 0

# while True:
#     wirelessManager.process()
#     if not isDoorOpen:  
#         # print('Distance:', distance, 'cm')
#         if shaking():
#             print("la porte s'ouvre", distance, "cm")
#             if wirelessManager.isConnected():
#                     wirelessManager.sendDataToWS("shaking")
#             isDoorOpen = True
#         else:
#             pass
#     else:
#         cooldown+=1
#         #print(cooldown)
    
#     if cooldown >= 20:
#         isDoorOpen = False
#         cooldown = 0
#     sleep_ms(200)