
from abc import ABCMeta, abstractmethod

class Map(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        self._minX = 0
        self._minY = 0
        self._moveLength = 0
        self._moveWidth = 0
        self._mapLength = 0
        self._mapWidth = 0
        self._map = [[]]

    def _initMap(self):
        self._map = [[1 for i in range(self.getMapWidth())] for i in range(self.getMapLength())]
        for i in range(self._minX,self._minX + self._moveLength):
            for j in range(self._minY,self._minY + self._moveWidth):
                self._map[i][j] = 0



    def _setObstacle(self,startX,startY,width,length):
        for i in range(startX,startX + width):
            for j in range(startY,startY + length):
                if 0 < i < self._mapLength and 0 < j < self._mapWidth:
                    self._map[i][j] = 1

    def setPlayer(self,pos,radius):
        for i in range(int((pos.x - radius)),int((pos.x + radius))):
            for j in range(int((pos.y - radius)),int((pos.y + radius))):
                if 0 < i < self._mapLength and 0 < j < self._mapWidth:
                    self._map[i][j] = 1

    def setMoveable(self,pos,radius):
        for i in range(int((pos.x - radius)), int((pos.x + radius))):
            for j in range(int((pos.y - radius)), int((pos.y + radius))):
                if 0 < i < self._mapLength and 0 < j < self._mapWidth:
                    self._map[i][j] = 0

    @abstractmethod
    def restore(self):
        pass

    def getMinX(self):
        return self._minX

    def getMinY(self):
        return self._minY

    def getMoveLength(self):
        return self._moveLength

    def getMoveWidth(self):
        return self._moveWidth

    def getMapLength(self):
        return self._mapLength

    def getMapWidth(self):
        return self._mapWidth

    def getMap(self):
        return self._map;
