from map import Map
from enemy import Enemy
from enemySpawn import EnemySpawn
from vector import Vector2

class Map01(Map):
    def __init__(self):
        super(Map01, self).__init__()
        self._mapWidth = 100
        self._mapLength = 100
        self._moveLength = 70
        self._moveWidth = 70
        self._minX = 15
        self._minY = 15
        self._initMap()
        self._setObstacle(75, 65, 3, 3)
        self._setObstacle(76, 56, 3, 3)
        self._setObstacle(71, 75, 3, 3)
        self._setObstacle(60, 78, 3, 3)
        self._setObstacle(34, 52, 3, 3)
        self._setObstacle(70, 36, 2, 1)

        enemySpwn1 = EnemySpawn(Vector2(75, 70))
        enemy1 = Enemy(1,enemySpwn1.pos,5,enemySpwn1)
        enemySpwn2 = EnemySpawn(Vector2(72, 80))
        enemy2 = Enemy(2,enemySpwn2.pos, 2, enemySpwn2)
        enemySpwn3 = EnemySpawn(Vector2(61, 82))
        enemy3 = Enemy(3,enemySpwn3.pos, 5, enemySpwn3)

        self.enemy = (enemy1,enemy2,enemy3)

    def restore(self):
        self._initMap()
        self._setObstacle(75, 65, 3, 3)
        self._setObstacle(76, 56, 3, 3)
        self._setObstacle(71, 75, 3, 3)
        self._setObstacle(60, 78, 3, 3)
        self._setObstacle(34, 52, 3, 3)
        self._setObstacle(70, 36, 2, 1)


if __name__ == '__main__':
    m = Map01()
    map = m.getMap()
    print m.getMapLength(),m.getMapWidth()
    for i in range(m.getMapWidth()):
        for j in range(m.getMapLength()):
            print(map[i][j]),
        print '\n',

