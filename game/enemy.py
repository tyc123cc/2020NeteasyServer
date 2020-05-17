# -*- coding: utf-8 -*-

import gameConf
from vector import Vector2
from threading import Timer

class Enemy:
    def __init__(self,id,pos,range,spawn):
        self.id = id
        self.hp = 100
        self.pos = pos
        self.nextPos = pos

        self.range = range
        self.speed = 2
        self.spawn = spawn
        self.state = gameConf.ENEMY_STATE_IDLE
        self.attackTarget = 0

        self.setProp = False;

    def setState(self,state):
        self.state = state
        if state != gameConf.ENEMY_STATE_DEATH:
            self.setProp = False
        if state == gameConf.ENEMY_STATE_ATTACK:
            t = Timer(1, self.AttackCD, ())
            t.start()
        if state == gameConf.ENEMY_STATE_DIZZY:
            t = Timer(3, self.dizzyEnd, ())
            t.start()

    def dizzyEnd(self):
        if self.state == gameConf.ENEMY_STATE_DIZZY:
            self.setState(gameConf.ENEMY_STATE_IDLE)

    def AttackCD(self):
        if self.state == gameConf.ENEMY_STATE_ATTACK:
            self.setState(gameConf.ENEMY_STATE_IDLE)

    def move(self,time):
        needTime = Vector2.distance(self.nextPos,self.pos) / self.speed
        self.pos = self.pos + (self.nextPos - self.pos) * (time / needTime)


    def damage(self,damage):
        self.hp -= damage
        if self.hp <= 0 :
            self.setState(gameConf.ENEMY_STATE_DEATH)
            # 10秒后复活
            t = Timer(10, self.__resurgence, ())
            t.start()

    def __resurgence(self):
        self.state = gameConf.ENEMY_STATE_IDLE
        self.hp = 100
        self.pos = self.spawn.pos

