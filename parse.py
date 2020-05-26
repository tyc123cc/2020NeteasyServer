# -*- coding: utf-8 -*-

import sys

sys.path.append('./common')
import conf
from game.vector import Vector3


class Parse:

    def __init__(self):
        pass

    def simple(self,msg):
        if msg[0] != '@' or msg[-1] != '#':
            return conf.MSG_UNMEANING
        # 考虑服务器同时收到多条消息，将全部消息封装成列表，同时去除消息前缀与后缀
        msgs = msg.split('@')
        res = []
        for clientMsg in msgs:
            if clientMsg:
                res.append(clientMsg[:-1])
        return res

    # 解析类型
    def parseType(self, msg):
        if msg[0] == 'R':
            return conf.MSG_REGISTER
        elif msg[0] == 'L':
            return conf.MSG_LOGIN
        elif msg[0] == 'B':
            return conf.MSG_LOBBY
        elif msg[0] == 'E':
            return conf.MSG_RECONNECT
        elif msg[0] == 'G':
            return conf.MSG_GAME
        elif msg[0] == 'S':
            return conf.MSG_SYNCHRONIZATION
        else:
            return conf.MSG_UNMEANING

    def parseSynType(self,msg):
        if msg[0] == 'D':
            return conf.MSG_SYN_DELAY
        elif msg[0] == 'T':
            return conf.MSG_SYN_TIME
        else:
            return 0

    def parseSynTime(self,msg):
        msg = msg.split(' ')
        delay = float(msg[0])
        clientTime = float(msg[1])
        return delay,clientTime

    def parseGameType(self,msg):
        if msg[0] == 'U':
            return conf.MSG_GAME_UPDATE
        elif msg[0] == 'L':
            return conf.MSG_GAME_LOAD

    def parseGame_Update_ChangeMotion(self,msg):
        msg = msg.split(' ')
        username = msg[0]
        time = float(msg[1])
        motion = int(msg[2])
        return username,time,motion

    def parseGame_Update_ChangeMove(self,msg):
        msg = msg.split(' ')
        username = msg[0]
        time = float(msg[1])
        move = int(msg[2])
        return username,time,move

    def parseGame_Update_ChangeRot(self,msg):
        msg = msg.split(' ')
        username = msg[0]
        time = float(msg[1])
        rotY = float(msg[2])
        rotSpeed = float(msg[3])
        lookPosY = float(msg[4])
        return username,time,rotY,rotSpeed,lookPosY

    def parseGame_Update_ChangeAttack(self,msg):
        msg = msg.split(' ')
        username = msg[0]
        attack = int(msg[1])
        isHit = True
        if msg[2] == "0":
            isHit = False
        if isHit:
            pos = Vector3(float(msg[3]),float(msg[4]),float(msg[5]))
            hitTarget = int(msg[6])
            return username,attack,isHit,pos,hitTarget
        return username,attack,isHit,None,None

    def parseGame_Update_Damage(self,msgs):
        msg = msgs.split(' ')
        enemyID = int(msg[0])
        damage = int(msg[1])
        return enemyID,damage

    def parseGame_Update_Prop(self,msgs):
        msg = msgs.split(' ')
        username = msg[0]
        propID = int(msg[1])
        return username,propID

    def parseGame_Update_Back(self,msgs):
        msg = msgs.split(' ')
        username = msg[0]
        return username

    def parseGame_UpdateType(self,msg):
        if msg[0] == 'M':
            return conf.MSG_GAME_UPDATE_CHANGEMOTION
        elif msg[0] == 'V':
            return conf.MSG_GAME_UPDATE_CHANGEMOVE
        elif msg[0] == 'R':
            return conf.MSG_GAME_UPDATE_CHANGEROT
        elif msg[0] == 'A':
            return conf.MSG_GAME_UPDATE_CHANGEATTACK
        elif msg[0] == 'D':
            return conf.MSG_GAME_UPDATE_DAMAGE
        elif msg[0] == 'P':
            return conf.MSG_GAME_UPDATE_PROP
        elif msg[0] == 'B':
            return conf.MSG_GAME_UPDATE_BACK


    def parseGame_Load(self,msg):
        msgs = msg.split(' ')
        playerID = int(msgs[0])
        process = float(msgs[1])
        return playerID,process


    # 解析大厅类型中的具体类型
    def parseLobbyType(self,msg):
        if msg[0] == 'C':
            return conf.MSG_LOBBY_CREATEROOM
        elif msg[0] == 'J':
            return conf.MSG_LOBBY_JOINROOM
        elif msg[0] == 'Q':
            return conf.MSG_LOBBY_QUITROOM
        elif msg[0] == 'G':
            return conf.MSG_LOBBY_GETROOMMSG
        elif msg[0] == 'R':
            return conf.MSG_LOBBY_READY
        elif msg[0] == 'S':
            return conf.MSG_LOBBY_START;
        else:
            return conf.MSG_UNMEANING

    def parseLobby_CreateRoom(self,clientMsg):
        msg = clientMsg.split(' ')
        map = msg[0]
        maxUserNum = msg[1]
        return map,maxUserNum

    # 解析注册信息
    def parseRegister(self,msg):
        readname = True
        username = ''
        password = ''
        for ch in msg:
            if readname:
                if ch == ' ':
                    readname = False
                else:
                    username += ch
            else:
                password += ch
        return username, password

    # 解析登录信息
    def parseLogin(self, msg):
        # 登录信息解析方法与注册信息相同
        return self.parseRegister(msg)