from map import Map
from enemy import Enemy
from enemySpawn import EnemySpawn
from vector import Vector2

class TestMap(Map):
    def __init__(self):
        super(TestMap, self).__init__()
        self._mapWidth = 6
        self._mapLength = 6
        self._moveLength = 6
        self._moveWidth = 6
        self._minX = 0
        self._minY = 0
        self._initMap()
        self._setObstacle(1, 1, 1, 5)
        self._setObstacle(0, 1, 5, 1)
        self._setObstacle(3, 3, 3, 1)


if __name__ == '__main__':
    m = TestMap()
    map = m.getMap()
    print m.getMapLength(),m.getMapWidth()
    for i in range(m.getMapLength()):
        for j in range(m.getMapWidth()):
            print(map[i][j]),
        print '\n',