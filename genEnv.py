import random

class GenEnv:
    def __init__(self):
        self.time = 0
    def incTime(self):
        self.time = self.time+1
    def decTime(self):
        self.time = self.time-1
    def getTime(self):
        return self.time
    def printTime(self):
        print("Simulation Time: %d"%self.time)

class Packet:
    def __init__(self, da=0, sa=0, type = 'UC', time=0, len=0, hopCnt=0):
        self.da = da
        self.sa = sa
        self.time = time
        self.pType = type
        self.len = len
        self.hopCnt = hopCnt
        if (type == 'BC'): ##Type is broadcast, set the pass to forward pass
            self.dir ='FPASS'
        else:
            self.dir = 'NORM'
    def incHopCnt(self):
        self.hopCnt +=1
    def getDa(self):
        return(self.da)
    def getSa(self):
        return(self.sa)
    def getTime(self):
        return(self.time)
    def getLen(self):
        return (self.len)
    def getHopCnt(self):
        return(self.hopCnt)
    def getCordinate (self, yMax):
        return (int(self.da/yMax), self.da%yMax)
    def getType(self):
        return(self.pType)
    def getDir(self):
        return (self.dir)
    def changeDir(self): ##Change the direction of broadcast packet.
        self.dir = 'NORM'
    def copyPacket (self):
        pkt = Packet(self.da, self.sa, self.pType, self.time, self.len, self.hopCnt)
        if pkt.getType() == 'BC':
            pkt.changeDir()
        return (pkt)



class PacketGen:
    ##Type: UR, PERM, NextNegihbor
    def __init__(self, type='UR', rate=1, x=0, y=0, xMax=4, yMax=4):
        self.type = type
        self.rateCredit = 1
        self.rate = rate
        self.pType = 'UC'
        self.x = x
        self.y = y
        self.sa = x*yMax + y
        self.xMax = xMax
        self.yMax = yMax

    def changePacketType (self, type='UC'):
        self.pType = type

    def genPacket(self, time):
        self.rateCredit += self.rate
        sa = self.sa
        len = 1 ##TODO: Change length with a random function
        if (self.rateCredit > 0): ##Positive Credit
            if (self.type == 'UR'):
                da = random.randint(0, self.xMax*self.yMax-1)
            elif (self.type == 'PERM'):
                newX = (self.x+self.xMax-1)%self.xMax
                newY = (self.y+self.yMax-1)%self.yMax
                da = newX*self.yMax+newY
            elif (self.type == 'M2O'):
                newX = self.xMax-1
                newY = self.yMax-1
                da = newX*self.yMax+newY
            elif (self.type == 'toMemoryEdge'):
                if (self.x == 0 or self.x == self.xMax-1):
                    return None
                if (self.y == 0 or self.y == self.yMax-1):
                    return None
                newX = 0 if (random.randint(0,1)==1) else self.xMax-1
                newY = random.randint (0,self.yMax-1)
                da = newX*self.yMax+newY
            else:
                da = 0
            self.rateCredit -= len
            return Packet(da, sa,self.pType, time, len, 0)
        else:
            return None






