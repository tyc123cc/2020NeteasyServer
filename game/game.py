# -*- coding: utf-8 -*-

import gameConf
from map.map01 import Map01
import time
from threading import Timer
from navigate import Navigate
from vector import Vector2
from prop import Prop
import sys


class Game:
    def __init__(self,host,map,roomID,players,startTime):
        self.host = host
        self.map = 0
        self.enemies = 0
        self.navi1 = 0
        self.navi2 = 0
        self.navi3 = 0
        if map == 1:
            self.map = Map01()
            for player in players:
                player.map = Map01()
            self.enemies = self.map.enemy
            self.navi1 = Navigate(Map01(),1)
            self.navi2 = Navigate(Map01(),1)
            self.navi3 = Navigate(Map01(),1)
        self.roomID = roomID
        self.players = players
        self.ready = False
        self.startTime = startTime

        self.props = []
        self.emptyPropsID = []

        self.deathEnemy = 0
        self.maxEnemy = 10

        self.enemyTime = 0

        self.gameEnd = False
        self.dissolve = False

    @staticmethod
    def addEXP(LV,EXP,value):
        EXP += value
        if EXP >= 1000:
            EXP -= 1000
            LV+= 1
        return (LV - 1) * 10 + 100, LV, EXP

    def generatePropID(self):
        if len(self.props) == 0 and len(self.emptyPropsID) == 0:
            return 1
        if len(self.emptyPropsID) > 0:
            return self.emptyPropsID.pop()
        else:
            return len(self.props) + 1


    def getEnemy(self,index):
        if index == 0:
            return None
        return self.enemies[index - 1]

    def damageEnemy(self,EnemyID,damage):
        enemy = self.getEnemy(EnemyID)
        if enemy:
            if enemy.state != gameConf.ENEMY_STATE_DEATH:
                enemy.damage(damage)
                if enemy.state == gameConf.ENEMY_STATE_DEATH:
                    self.deathEnemy += 1
                    if self.deathEnemy >= self.maxEnemy:
                        self.endGame()

    def endGame(self):
        self.gameEnd = True

    def getPlayer(self,arg):
        for player in self.players:
            if isinstance(arg,int):
                if player.userID == arg:
                    return player
            elif isinstance(arg,str):
                if player.username == arg:
                    return player

    def reconnect(self,username,user):
        for player in self.players:
            if player.username == username:
                player.user = user

    def couldStart(self):
        for player in self.players:
            if player.process < 1:
                return False
        return True

    def changeAtk(self,username,atk):
        player = self.getPlayer(username)
        player.setAttack(atk)
        if atk != gameConf.ATTACK_IDLE and atk != gameConf.ATTACK_RELOAD and atk!= gameConf.ATTACK_THROW:
            if player.curAmmo <= 0:
                return
            player.curAmmo -= 1
        if atk == gameConf.ATTACK_RELOAD:
            player.reload()
            t = Timer(3.3,self.__playerUnShoot,(player,))
            t.start()
        if atk == gameConf.ATTACK_SINGLE:
            t = Timer(0.3,self.__playerUnShoot,(player,))
            t.start()
        if atk == gameConf.ATTACK_THROW:
            t = Timer(1.0,self.__playerUnShoot,(player,))
            t.start()

    def changeRot(self,username,clientTime,rotY,rotSpeed,lookY,startTime):
        player = self.getPlayer(username)
        delay = time.time() - startTime - player.user.timeDif - clientTime
        #rot = rotY + rotSpeed * delay
        #self.__repairPos(player, delay)
        rot = rotY
        player.setRotation(rot,lookY)
       # player.setMove(player.move, delay)
        return rot

    def changeMotion(self,username,clientTime,motion,startTime):
        player = self.getPlayer(username)
        delay = time.time() - startTime - player.user.timeDif - clientTime
        #self.__repairPos(player,delay)
        #pos = player.setMotion(motion,delay)
        pos = player.setMotion(motion,0)
        return pos

    def changeMove(self,username,clientTime,move,startTime):
        player = self.getPlayer(username)
        delay = time.time() - startTime - player.user.timeDif - clientTime
        #self.__repairPos(player, delay)
        #pos = player.setMove(move,delay)
        pos = player.setMove(move, 0)
        return pos

    def __repairPos(self,player,delay):
        playerMove = player.move
        if playerMove == gameConf.MOVE_IDLE:
            return player.pos
        elif playerMove == gameConf.MOVE_RUN:
            return player.back(delay)
        elif playerMove == gameConf.MOVE_BACK:
            return player.run(delay)
        elif playerMove == gameConf.MOVE_LEFT:
            return player.right(delay)
        elif playerMove == gameConf.MOVE_RIGHT:
            return player.left(delay)
        elif playerMove == gameConf.MOVE_RUN_LEFT:
            return player.run_right(delay)
        elif playerMove == gameConf.MOVE_RUN_RIGHT:
            return player.run_left(delay)
        elif playerMove == gameConf.MOVE_BACK_LEFT:
            return player.back_right(delay)
        elif playerMove == gameConf.MOVE_BACK_RIGHT:
            return player.back_left(delay)

    def pickupProp(self,username,propID):
        player = self.getPlayer(username)
        self.removeProp(propID)
        player.cure(20,10)

    def removeProp(self,propID):
        for i in range(0,len(self.props)):
            if self.props[i].id == propID:
                return self.props.pop(i)

    def sendAllPlayerWithPropMsg(self):
        msg = "GP" + str(len(self.props)) + " "
        for prop in self.props:
            ID = prop.id
            posx = prop.pos.x
            posy = prop.pos.y
            msg += str(ID) + " " + str(posx) + " " + str(posy) + " "
        self.sendAllPlayer(msg)

    def sendAllPlayerWithPlayerProcess(self):
        msg = "GL" + str(len(self.players)) + " "
        for player in self.players:
            playerID = player.userID
            username = player.username
            process = player.process
            msg += str(playerID) + " " + username + " " + str(process) + " "
        self.sendAllPlayer(msg)

    def sendAllPlayerWithPlayerMsg(self):
        msg = "GU" + str(len(self.players)) + " " + str(time.time() - self.startTime) + " "
        for player in self.players:
            playerID = player.userID
            username = player.username
            pos = player.pos
            rot = player.rotation.y
            look = player.lookupPos.y
            motion = player.motion
            if motion == gameConf.MOTION_DEATH:
                move = int(player.resurgenceTime)
            else:
                move = player.move
            attack = player.attack
            HP = player.hp
            curAmmo = player.curAmmo
            bagAmmo = player.bagAmmo
            LV = player.lv
            EXP = player.exp
            msg += str(playerID) + " " + username + " " + str(pos.x) + " " + str(pos.z) + " " + str(rot) + \
                   " " + str(look) + " " + str(motion) + " " + str(move) + " " + str(attack) + " " + \
                str(HP) + " " + str(curAmmo) + " " + str(bagAmmo) + " " + str(LV) + " " + str(EXP) + " "
        self.sendAllPlayer(msg)

    def sendAllPlayerWithEnemyMsg(self):
        msg = "GE" + str(time.time()) + " "
        for enemy in self.enemies:
            id = enemy.id
            hp = enemy.hp
            pos = enemy.pos
            nextPos = enemy.nextPos
            state = enemy.state
            attackTarget = enemy.attackTarget
            msg += str(id) + " " + str(hp) + " " + str(pos.x) + " " + str(pos.y) + " " + str(nextPos.x) + " " + \
                str(nextPos.y) + " " + str(state) + " " + str(attackTarget) + " "
        msg += str(self.deathEnemy) + " " + str(self.maxEnemy)
        self.sendAllPlayer(msg)

    def sendAllPlayer(self,msg):
        for player in self.players:
            if not player.user.lost:
                self.host.sendClient(player.user.hid,msg)

    def sendPlayer(self,username,msg):
        for player in self.players:
            if player.username == username:
                self.host.sendClient(player.user.hid,msg)
                return

    # 每隔一段时间根据角色状态对角色进行位移
    def __playerMove(self,player):
        if player.motion == gameConf.MOTION_DEATH:
            player.resurgence()
        elif player.move == gameConf.MOVE_IDLE:
            player.idle()
        elif player.move == gameConf.MOVE_RUN:
            player.run()
        elif player.move == gameConf.MOVE_BACK:
            player.back()
        elif player.move == gameConf.MOVE_LEFT:
            player.left()
        elif player.move == gameConf.MOVE_RIGHT:
            player.right()
        elif player.move == gameConf.MOVE_RUN_LEFT:
            player.run_left()
        elif player.move == gameConf.MOVE_RUN_RIGHT:
            player.run_right()
        elif player.move == gameConf.MOVE_BACK_LEFT:
            player.back_left()
        elif player.move == gameConf.MOVE_BACK_RIGHT:
            player.back_right()

    def __playerUnShoot(self,player):
        #if player.attack == gameConf.ATTACK_SINGLE:
            #if time.time() - player.singleTime >= 0.3:
                #player.setAttack(gameConf.ATTACK_IDLE)
        player.setAttack(gameConf.ATTACK_IDLE)
        #print("singleEnd")
        pass

    def __enemyProcess(self,enemy):
        if self.enemyTime == 0:
            self.enemyTime = time.time()
        enemyPos = enemy.pos
        navi = 0
        if enemy.id == 1:
            navi = self.navi1
        if enemy.id == 2:
            navi = self.navi2
        if enemy.id == 3:
            navi = self.navi3
        if (enemy.state == gameConf.ENEMY_STATE_IDLE or enemy.state == gameConf.ENEMY_STATE_MOVE):
            minNodeNum = sys.maxint
            minPath = []
            for player in self.players:
                if player.motion == gameConf.MOTION_DEATH:
                    continue
                playerPos = Vector2(player.pos.x,player.pos.z)
                if Vector2.distance(enemyPos,playerPos) <= enemy.range:
                    enemy.setState(gameConf.ENEMY_STATE_ATTACK)
                    enemy.attackTarget = player.userID
                    player.damage(10)
                    return
                hasPath,path = navi.navi(enemyPos,playerPos)
                if hasPath and len(path) < minNodeNum:
                    minNodeNum = len(path)
                    minPath = path
            if minNodeNum > 2 and minNodeNum < sys.maxint and (playerPos.y > enemyPos.y or playerPos.x > enemyPos.x):
                enemy.nextPos = minPath[2]
                enemy.setState(gameConf.ENEMY_STATE_MOVE)
                enemy.move(time.time() - self.enemyTime)
            elif minNodeNum > 1 and minNodeNum < sys.maxint:
                enemy.nextPos = minPath[1]
                enemy.setState(gameConf.ENEMY_STATE_MOVE)
                enemy.move(time.time() - self.enemyTime)
            else:
                enemy.setState(gameConf.ENEMY_STATE_IDLE)
        elif enemy.state == gameConf.ENEMY_STATE_DEATH and not enemy.setProp:
            enemy.setProp = True
            id = self.generatePropID()
            self.props.append(Prop(enemyPos,int(id)))

    def restoreMap(self):
        for p in self.players:
            p.map.restore()
            for player in self.players:
                if player.userID != p.userID and player.motion != gameConf.MOTION_DEATH:
                    pos = Vector2(player.pos.x,player.pos.z)
                    p.map.setPlayer(pos,1)
            for enemy in self.enemies:
                if enemy.state != gameConf.ENEMY_STATE_DEATH:
                    p.map.setPlayer(enemy.pos,1)
        for enemy in self.enemies:
            self.restoreEnemyMap(enemy.id)
            pass

    def restoreEnemyMap(self,enemyid):
        navi = 0
        if enemyid == 1:
            navi = self.navi1
        elif enemyid == 2:
            navi = self.navi2
        elif enemyid == 3:
            navi = self.navi3
        navi.restoreMap()
        for enemy in self.enemies:
            if enemy.id != enemyid and enemy.state != gameConf.ENEMY_STATE_DEATH:
                navi.setPlayer(enemy.pos, 2)
        for player in self.players:
            if player.motion != gameConf.MOTION_DEATH:
                pos = Vector2(player.pos.x, player.pos.z)
                navi.setMoveable(pos,1)

    def process(self):
        if self.ready:
            for player in self.players:
                self.__playerMove(player)
            for enemy in self.enemies:
                self.__enemyProcess(enemy)
            self.enemyTime = time.time()
            self.restoreMap()