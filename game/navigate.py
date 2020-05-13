# -*- coding: utf-8 -*-

from vector import Vector2
from map.map01 import Map01
from map.testMap import TestMap

class Navigate:
    class Node:
        def __init__(self,pos,g,target,last):
            self.pos = pos
            self.g = g
            self.h = abs(target.x - pos.x) + abs(target.y - pos.y)
            self.f = self.g + self.h
            self.lastNode = last

        def update(self,g,last):
            self.g = g
            self.f = self.g + self.h
            self.lastNode = last

    def __init__(self,map,interval):
        self.map = map
        self.interval = interval
        self.width = map.getMapWidth()
        self.length = map.getMapLength()

    def restoreMap(self):
        self.map.restore()

    def setPlayer(self,pos,radius):
        self.map.setPlayer(pos,radius)

    def setMoveable(self,pos,radius):
        self.map.setMoveable(pos,radius)

    # A*算法
    def navi(self,start,target):
        openList = []
        closeList = []
        startNode = self.Node(Vector2(int(start.x),int(start.y)),0,target,None)
        openList.append(startNode)
        hasPath = False
        path = []
        count = 0
        while len(openList) > 0:
            count += 1
            if count > 100:
                break
            minNode = self.findMinNode(openList,closeList,target)
            openList.remove(minNode)
            closeList.append(minNode)
            if Vector2.distance(minNode.pos,target) < self.interval:
                hasPath = True
                self.createPath(path,minNode)
                break
        return hasPath,path

    def createPath(self,path,node):
        path.insert(0,node.pos)
        if node.lastNode:
            self.createPath(path,node.lastNode)


    def findMinNode(self,openList,closeList,target):
        minF = float('inf')
        minOpenNode = None
        for openNode in openList:
            if openNode.f < minF:
                minF = openNode.f
                minOpenNode = openNode
        neighbor = self.getNeighbor(minOpenNode,target,closeList)
        for nei in neighbor:
            if self.nodeInList(nei,openList):
                # 邻居已经在open表中，判断是否需要更新f值
                node = self.findNodeInList(nei,openList)
                if nei.f < node.f:
                    node.update(nei.g,nei.lastNode)
            else:
                openList.append(nei)
        return minOpenNode


    def getNeighbor(self,node,target,closeList):
        neighbor = []
        pos = node.pos
        if pos.x + self.interval < self.length:
            newPos = Vector2(pos.x + self.interval,pos.y)
            neighbor.append(self.Node(pos = newPos,g = node.g + self.interval,target = target,last = node))
        if pos.y + self.interval < self.width:
            newPos = Vector2(pos.x,pos.y + self.interval)
            neighbor.append(self.Node(pos = newPos,g = node.g + self.interval,target = target,last = node))
        if pos.x - self.interval >= 0:
            newPos = Vector2(pos.x - self.interval,pos.y)
            neighbor.append(self.Node(pos = newPos,g = node.g + self.interval,target = target,last = node))
        if pos.y - self.interval >= 0:
            newPos = Vector2(pos.x,pos.y - self.interval)
            neighbor.append(self.Node(pos = newPos,g = node.g + self.interval,target = target,last = node))
        if pos.x + self.interval < self.length and pos.y + self.interval < self.width:
            newPos = Vector2(pos.x + self.interval, pos.y + self.interval)
            neighbor.append(self.Node(pos=newPos, g=node.g + self.interval * 1.4, target=target,last = node))
        if pos.x + self.interval < self.length and pos.y - self.interval >= 0:
            newPos = Vector2(pos.x + self.interval, pos.y - self.interval)
            neighbor.append(self.Node(pos=newPos, g=node.g + self.interval * 1.4, target=target,last = node))
        if pos.x - self.interval >= 0 and pos.y + self.interval < self.width:
            newPos = Vector2(pos.x - self.interval, pos.y + self.interval)
            neighbor.append(self.Node(pos=newPos, g=node.g + self.interval * 1.4, target=target,last = node))
        if pos.x - self.interval >= 0 and pos.y - self.interval >= 0:
            newPos = Vector2(pos.x - self.interval, pos.y - self.interval)
            neighbor.append(self.Node(pos=newPos, g=node.g + self.interval * 1.4, target=target,last = node))
        i = 0
        while i < len(neighbor):
            if neighbor[i].pos != target and (self.isObstacle(neighbor[i]) or self.nodeInList(neighbor[i],closeList)):
                neighbor.remove(neighbor[i])
                i -= 1
            i += 1
        return neighbor

    def nodeInList(self,node,list):
        for n in list:
            if n.pos == node.pos:
                return True
        return False

    def findNodeInList(self,node,list):
        for n in list:
            if n.pos == node.pos:
                return n
        return None

    def isObstacle(self,node):
        if node.pos.x > self.length or node.pos.x < 0 or node.pos.y > self.width or node.pos.y < 0:
            return True
        if self.map.getMap()[node.pos.x][node.pos.y] == 1:
            return True
        else:
            return False

if __name__ == '__main__':
    nav = Navigate(TestMap(),1)
    hasPath,path = nav.navi(Vector2(0,0),Vector2(1,5))
    if hasPath:
        for node in path:
            print node

