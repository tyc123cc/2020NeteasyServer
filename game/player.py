from vector import *
import gameConf
import time

class Player:
    def __init__(self,user,hp,ammo,lv,exp):
        self.user = user
        self.userID = user.userID_Room
        self.username = user.username
        self.pos = Vector3(0,0,0)
        self.lookAt = Vector2(0,1)
        self.rotation = Vector3(0,0,0)
        self.lookupPos = Vector3(0,2.3,1)
        self.speed = gameConf.SPEED_WALK

        self.map = 0

        self.startTime = 0
        self.endTime = 0

        self.ready = False
        self.process = 0

        self.hp = hp
        self.curAmmo = 30
        self.bagAmmo = ammo - 30
        self.lv = lv
        self.exp = exp

        self.motion = gameConf.MOTION_WALK
        self.move = gameConf.MOVE_IDLE
        self.attack = gameConf.ATTACK_IDLE

        self.singleTime = 0

    def damage(self,damage):
        self.hp -= damage

    def reload(self):
        if self.curAmmo + self.bagAmmo < 30:
            self.curAmmo += self.bagAmmo
            self.bagAmmo = 0
        else:
            self.bagAmmo -= 30 - self.curAmmo
            self.curAmmo = 30

    def setAttack(self,attack):
        self.attack = attack
        if attack == gameConf.ATTACK_SINGLE:
            self.singleTime = time.time()

    def setMotion(self,motion,delay):
        self.motion = motion
        pos = self.pos
        move = self.move
        if motion == gameConf.MOTION_RUN:
            self.speed = gameConf.SPEED_RUN
        elif motion == gameConf.MOTION_WALK:
            self.speed = gameConf.SPEED_WALK
        elif motion == gameConf.MOTION_CROUCH:
            self.speed = gameConf.SPEED_CROUCH
        if move == gameConf.MOVE_RUN:
            pos = self.run(delay)
        elif move == gameConf.MOVE_BACK:
            pos = self.back(delay)
        elif move == gameConf.MOVE_LEFT:
            pos = self.left(delay)
        elif move == gameConf.MOVE_RIGHT:
            pos = self.right(delay)
        elif move == gameConf.MOVE_RUN_LEFT:
            pos = self.run_left(delay)
        elif move == gameConf.MOVE_RUN_RIGHT:
            pos = self.run_right(delay)
        elif move == gameConf.MOVE_BACK_LEFT:
            pos = self.back_left(delay)
        elif move == gameConf.MOVE_BACK_RIGHT:
            pos = self.back_right(delay)
        return pos


    def setMove(self,move,delay):
        self.move = move
        pos = self.pos
        if move == gameConf.MOVE_RUN:
            pos = self.run(delay)
        elif move == gameConf.MOVE_BACK:
            pos = self.back(delay)
        elif move == gameConf.MOVE_LEFT:
            pos = self.left(delay)
        elif move == gameConf.MOVE_RIGHT:
            pos = self.right(delay)
        elif move == gameConf.MOVE_RUN_LEFT:
            pos = self.run_left(delay)
        elif move == gameConf.MOVE_RUN_RIGHT:
            pos = self.run_right(delay)
        elif move == gameConf.MOVE_BACK_LEFT:
            pos = self.back_left(delay)
        elif move == gameConf.MOVE_BACK_RIGHT:
            pos = self.back_right(delay)
        return pos

    def setRotation(self,rotY,lookY):
        self.rotation.y = rotY
        self.lookupPos.y = lookY
        self.setLook()

    def setLook(self,*angle):
        self.lookAt = Vector2(0,1)
        if len(angle) == 0:
            self.lookAt.rotate(self.rotation.y)
        elif len(angle) == 1:
            self.lookAt.rotate(angle[0])

    def obstacle(self,x,z):
        if self.map.getMap()[int(x)][int(z)] == 0:
            return False
        else:
            return True

    def idle(self):
        self.startTime = time.time()

    def run(self,*runTime):
        if len(runTime) == 1:
            pos = Vector2(self.pos.x, self.pos.z)
            pos += self.lookAt * self.speed * runTime[0]
            if not self.obstacle(pos.x,pos.y):
                self.pos = Vector3(pos.x, self.pos.y, pos.y)
            return self.pos
        pos = Vector2(self.pos.x,self.pos.z)
        endTime = time.time()
        pos += self.lookAt * self.speed * (endTime - self.startTime)
        self.startTime = time.time()
        if not self.obstacle(pos.x, pos.y):
            self.pos = Vector3(pos.x,self.pos.y,pos.y)

    def back(self,*runTime):
        if len(runTime) == 1:
            pos = Vector2(self.pos.x, self.pos.z)
            pos -= self.lookAt * self.speed * runTime[0]
            if not self.obstacle(pos.x, pos.y):
                self.pos = Vector3(pos.x, self.pos.y, pos.y)
            return self.pos
        pos = Vector2(self.pos.x, self.pos.z)
        endTime = time.time()
        pos -= self.lookAt * self.speed * (endTime - self.startTime)
        self.startTime = time.time()
        if not self.obstacle(pos.x, pos.y):
            self.pos = Vector3(pos.x, self.pos.y, pos.y)

    def left(self,*runTime):
        if len(runTime) == 1:
            pos = Vector2(self.pos.x, self.pos.z)
            direct = self.lookAt.rawRotate(-90)
            pos += direct * self.speed * runTime[0]
            if not self.obstacle(pos.x, pos.y):
                self.pos = Vector3(pos.x, self.pos.y, pos.y)
            return self.pos
        pos = Vector2(self.pos.x, self.pos.z)
        direct = self.lookAt.rawRotate(-90)
        endTime = time.time()
        pos += direct * self.speed * (endTime - self.startTime)
        self.startTime = time.time()
        if not self.obstacle(pos.x, pos.y):
            self.pos = Vector3(pos.x, self.pos.y, pos.y)

    def right(self,*runTime):
        if len(runTime) == 1:
            pos = Vector2(self.pos.x, self.pos.z)
            direct = self.lookAt.rawRotate(90)
            pos += direct * self.speed * runTime[0]
            if not self.obstacle(pos.x, pos.y):
                self.pos = Vector3(pos.x, self.pos.y, pos.y)
            return self.pos
        pos = Vector2(self.pos.x, self.pos.z)
        direct = self.lookAt.rawRotate(90)
        endTime = time.time()
        pos += direct * self.speed * (endTime - self.startTime)
        self.startTime = time.time()
        if not self.obstacle(pos.x, pos.y):
            self.pos = Vector3(pos.x, self.pos.y, pos.y)

    def run_left(self,*runTime):
        if len(runTime) == 1:
            pos = Vector2(self.pos.x, self.pos.z)
            direct = self.lookAt.rawRotate(-45)
            pos += direct * self.speed * runTime[0]
            if not self.obstacle(pos.x, pos.y):
                self.pos = Vector3(pos.x, self.pos.y, pos.y)
            return self.pos
        pos = Vector2(self.pos.x, self.pos.z)
        direct = self.lookAt.rawRotate(-45)
        endTime = time.time()
        pos += direct * self.speed * (endTime - self.startTime)
        self.startTime = time.time()
        if not self.obstacle(pos.x, pos.y):
            self.pos = Vector3(pos.x, self.pos.y, pos.y)

    def run_right(self,*runTime):
        if len(runTime) == 1:
            pos = Vector2(self.pos.x, self.pos.z)
            direct = self.lookAt.rawRotate(45)
            pos += direct * self.speed * runTime[0]
            if not self.obstacle(pos.x, pos.y):
                self.pos = Vector3(pos.x, self.pos.y, pos.y)
            return self.pos
        pos = Vector2(self.pos.x, self.pos.z)
        direct = self.lookAt.rawRotate(45)
        endTime = time.time()
        pos += direct * self.speed * (endTime - self.startTime)
        self.startTime = time.time()
        if not self.obstacle(pos.x, pos.y):
            self.pos = Vector3(pos.x, self.pos.y, pos.y)

    def back_left(self,*runTime):
        if len(runTime) == 1:
            pos = Vector2(self.pos.x, self.pos.z)
            direct = self.lookAt.rawRotate(45)
            pos -= direct * self.speed * runTime[0]
            if not self.obstacle(pos.x, pos.y):
                self.pos = Vector3(pos.x, self.pos.y, pos.y)
            return self.pos
        pos = Vector2(self.pos.x, self.pos.z)
        direct = self.lookAt.rawRotate(45)
        endTime = time.time()
        pos -= direct * self.speed * (endTime - self.startTime)
        self.startTime = time.time()
        if not self.obstacle(pos.x, pos.y):
            self.pos = Vector3(pos.x, self.pos.y, pos.y)

    def back_right(self,*runTime):
        if len(runTime) == 1:
            pos = Vector2(self.pos.x, self.pos.z)
            direct = self.lookAt.rawRotate(-45)
            pos -= direct * self.speed * runTime[0]
            if not self.obstacle(pos.x, pos.y):
                self.pos = Vector3(pos.x, self.pos.y, pos.y)
            return self.pos
        pos = Vector2(self.pos.x, self.pos.z)
        direct = self.lookAt.rawRotate(-45)
        endTime = time.time()
        pos -= direct * self.speed * (endTime - self.startTime)
        self.startTime = time.time()
        if not self.obstacle(pos.x, pos.y):
            self.pos = Vector3(pos.x, self.pos.y, pos.y)

if __name__ == '__main__':
    p = Player()
    p.setRotation(Vector3(5,0,7))
    p.back_right()
    print(p.rotation)
    print(p.lookAt)
    print(p.pos)