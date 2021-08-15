import random
from Node import *
from genEnv import *
from gridImage import *


def getLatency(injectionRate):
    xMax = 8  # GRID X
    yMax = 8  # GRID y
    maxClkCnt = 1000
    pktGenType = 'toMemoryEdge'
    pktGenRate = injectionRate
    dirA = ['E', 'W', 'N', 'S']
    totalLatency = 0
    maxLatency = 0
    totalHopCnt = 0
    maxHopCnt = 0
    rcvdPktPerSource = []
    rcvdLatPerSource = []
    for src in range(xMax*yMax):
        rcvdPktPerSource.append(0)
        rcvdLatPerSource.append(0)

    myGen = GenEnv()
    nodeList = []
    # Create Node structure
    for x in range(xMax):
        for y in range(yMax):
            nodeList.append(Node(x, y, xMax, yMax, pktGenType, pktGenRate))
            # Following line changes packet type to BC
    #        nodeIdx = x*yMax+y
    #        nodeList[nodeIdx].changePacketType()

    # Connect Node to other members:
    cntArray = {}
    for x in range(xMax):
        cntArray[x] = {}
        for y in range(yMax):
            cntArray[x][y] = {}
            for dir in dirA:
                cntArray[x][y][dir] = 0
                nodeIdx = x*yMax + y
                if dir == 'E':
                    nodeList[nodeIdx].connectNode(dir, x+1, y)
                if dir == 'W':
                    nodeList[nodeIdx].connectNode(dir, x-1, y)
                if dir == 'N':
                    nodeList[nodeIdx].connectNode(dir, x, y+1)
                if dir == 'S':
                    nodeList[nodeIdx].connectNode(dir, x, y-1)

    for i in range(maxClkCnt):
        time = myGen.getTime()
        myGen.incTime()
        # Generated an item per node
        for x in range(xMax):
            for y in range(yMax):
                nodeIdx = x*yMax+y
                nodeList[nodeIdx].genItem(time)
                # dequeue an item if required
                for dir in dirA:
                    nodeIdx = x*yMax+y
                    (result, myPacket, nextX,
                     nextY) = nodeList[nodeIdx].moveItem(dir)
                    if result == 0:
                        continue
                    (dX, dY) = myPacket.getCordinate(yMax)
                    if (nextX >= xMax) | (nextX < 0):
                        print("Error. Item reached to limit without delivery")
                        print("dx:%d, dy:%d, next X: %d, next Y:%d" %
                              (dX, dY, nextX, nextY))
                        continue
                    if (nextY >= yMax) | (nextY < 0):
                        print("Error. Item reached to limit without delivery")
                        print("dx:%d, dy:%d, next X: %d, next Y:%d" %
                              (dX, dY, nextX, nextY))
                        continue

                    cntArray[x][y][dir] += 1
                    nodeIdx = nextX*yMax+nextY
                    myPacket.incHopCnt()  # Increment hop count
                    newPacket = nodeList[nodeIdx].addItem(myPacket)
                    if newPacket:
                        latency = time - newPacket.getTime()
                        rcvdPktPerSource[newPacket.getSa()] += 1
                        rcvdLatPerSource[newPacket.getSa()] += latency
                        if (latency < 0):
                            print("Error. Received a packet with negative latency")
                        else:
                            if (latency > maxLatency):
                                maxLatency = latency
                            if (newPacket.getHopCnt() > maxHopCnt):
                                maxHopCnt = newPacket.getHopCnt()
                            totalLatency += latency
                            totalHopCnt += newPacket.getHopCnt()

    totalTxCnt = 0
    totalRxCnt = 0
    totalPendCnt = 0
    for x in range(xMax):
        for y in range(yMax):
            myIdx = x*yMax+y
            totalTxCnt += nodeList[myIdx].getTxCnt()
            totalRxCnt += nodeList[myIdx].getRxCnt()
            totalPendCnt += nodeList[myIdx].getPendCnt()
    return (totalLatency/totalRxCnt, maxLatency)
