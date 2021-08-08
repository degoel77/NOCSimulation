#Node class keeps x and y. 
import random
from genEnv import *
class Node:
    def __init__(self, x=0, y=0, xMax=0, yMax=0, type='UR', packetGenRate=1):
        self.x = x
        self.y = y
        self.xMax = xMax
        self.yMax = yMax
        self.eList =[]
        self.wList =[]
        self.nList =[]
        self.sList =[]
        self.outItemCnt = 0
        self.inItemCnt = 0
        self.packetGen = PacketGen(type, packetGenRate, x, y, xMax, yMax)

    #Can Move this function outside.
    def genItem(self, time):
        Packet = self.packetGen.genPacket(time)
        if (Packet):
            self.outItemCnt +=1
            self.addItem(Packet)
            return 1
        else:
            return None

    def connectNode(self, dir='E', x=0, y=0):
        if dir == 'E':
            self.eNx = x
            self.eNy = y
        elif dir == 'W':
            self.wNx = x
            self.wNy = y
        elif dir == 'N':
            self.nNx = x
            self.nNy = y
        else:
            self.sNx = x
            self.sNy = y

    def addItem (self, packet):
        if (packet.getType() == 'BC') & (packet.getDir() == 'FPASS'):
            (x,y) = (int(self.xMax/2), int(self.yMax/2))
        elif(packet.getType() == 'BC') & (packet.getDir() != 'FPASS'):
            bcRootX = int(self.xMax/2)
            bcRootY = int(self.yMax/2)
            ##Following is a way to broadcast in 2D MESH
            if (self.y > bcRootY): ## Y is greater than root
                if (self.y != self.yMax-1):
                    self.nList.append(packet.copyPacket())
            elif (self.y < bcRootY): ## Y is smaller than root
                if (self.y != 0):
                    self.sList.append(packet.copyPacket())
            else: ## X is equal to rootX
                self.nList.append(packet.copyPacket())
                self.sList.append(packet.copyPacket())
                if (self.x > bcRootX):
                    if (self.x != self.xMax-1):
                        self.eList.append(packet.copyPacket())
                elif (self.x < bcRootX):
                    if (self.x != 0):
                        self.wList.append(packet.copyPacket())
                else:
                    self.eList.append(packet.copyPacket())
                    self.wList.append(packet.copyPacket())

            self.inItemCnt +=1
            return packet
        else:
            (x,y) = packet.getCordinate(self.yMax)

        if (x>self.x):
            self.eList.append(packet)
        elif (x == self.x):
            if (y>self.y):
                self.nList.append(packet)
            elif (y==self.y):
                if (packet.getType() == 'BC') & (packet.getDir() == 'FPASS'):
                    packet.changeDir()
                    self.addItem(packet)
                else:
                    self.inItemCnt +=1
                    return packet
            else:
                self.sList.append(packet)
        else:
            self.wList.append(packet)
        return None

    def moveItem (self, dir='E'):
        if dir =='E':
            if len(self.eList):
                packet = self.eList.pop(0)
                return(1, packet, self.eNx, self.eNy)
            else:
                return (0,0,0,0)
        if dir =='W':
            if len(self.wList):
                packet = self.wList.pop(0)
                return(1, packet, self.wNx, self.wNy)
            else:
                return (0,0,0,0)
        if dir =='N':
            if len(self.nList):
                packet = self.nList.pop(0)
                return(1, packet, self.nNx, self.nNy)
            else:
                return (0,0,0,0)
        if dir =='S':
            if len(self.sList):
                packet = self.sList.pop(0)
                return(1, packet, self.sNx, self.sNy)
            else:
                return (0,0,0,0)

    #Get generated element count
    def getTxCnt(self):
        return self.outItemCnt

    #Get received element count
    def getRxCnt(self):
        return self.inItemCnt

    #Get pending element count
    def getPendCnt(self):
        return len(self.eList)+len(self.wList)+len(self.nList)+len(self.sList)

    #Print Node
    def printNode(self):
        print("Node: X: %d, y:%d"%(self.x,self.y))
        print("Node: E(x,y): (%d, %d), W(x,y):(%d,%d), N(x,y):(%d,%d), S(x,y):(%d,%d)"%(self.eNx,self.eNy, self.wNx, self.wNy, self.nNx, self.nNy, self.sNx, self.sNy))
        print("Transmitted element count:%d, Received element count: %d "% (self.outItemCnt, self.inItemCnt))
        print("Pending Items in the list: %d "% (len(self.eList)+len(self.wList)+len(self.nList)+len(self.sList)))

    #Change Packet Gen type to BC
    def changePacketType (self):
        self.packetGen.changePacketType('BC')


