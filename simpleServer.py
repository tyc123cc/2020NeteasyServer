# -*- coding: utf-8 -*-

import sys

sys.path.append('./common')
sys.path.append('./sql')
sys.path.append('./common_server')
sys.path.append('./network')
sys.path.append('./lobby')
sys.path.append('./game')

from network.simpleHost import SimpleHost
from dispatcher import Dispatcher
from sql import Sql
import conf
from parse import Parse
import time
from lobby.lobby import Lobby
from game.game import Game
from game.player import Player
from game.vector import *
from multiprocessing import Process,Queue
import gameConf
import thread
import time
import datetime


class SimpleServer(object):

    def __init__(self):
        super(SimpleServer, self).__init__()

        self.entities = {}
        self.host = SimpleHost()
        self.dispatcher = Dispatcher()
        self.parse = Parse()
        self.sql = Sql()
        self.lobby = Lobby()
        self.gameMsg = {}
        self.startTime = time.time()

        self.runGame = {}

        self.lastTime = 0
        self.lastClientTime = 0

        return

    def connect(self, port):
        self.host.startup(port)

    def __dealMsg(self, clientID, msg):
        msgType = self.parse.parseType(msg)
        msg = msg[1:]
        if msgType == conf.MSG_REGISTER:
            # 用户注册
            self.__dealRegister(clientID, msg)
        if msgType == conf.MSG_LOGIN:
            # 用户登录
            self.__dealLogin(clientID, msg)
        if msgType == conf.MSG_LOBBY:
            # 用户执行与大厅有关操作
            self.__dealLobby(clientID, msg)
        if msgType == conf.MSG_RECONNECT:
            # 用户重登
            self.__dealReconnect(clientID, msg)
        if msgType == conf.MSG_GAME:
            # 游戏相关操作
            self.__dealGame(clientID, msg)
        if msgType == conf.MSG_SYNCHRONIZATION:
            self.__dealSyn(clientID, msg)

    # <editor-fold desc="时间戳同步">

    # 处理同步信息
    def __dealSyn(self, clientID, msg):
        type = self.parse.parseSynType(msg)
        msg = msg[1:]
        if type == conf.MSG_SYN_DELAY:
            self.__dealSynDelay(clientID, msg)
        elif type == conf.MSG_SYN_TIME:
            self.__dealSynTime(clientID, msg)

    def __dealSynTime(self, clientID, msg):
        delay, clientTime = self.parse.parseSynTime(msg)
        timeDif = time.time() - self.startTime - clientTime - delay / 2
        self.host.getClient(clientID)[1].delay = delay / 2
        self.host.getClient(clientID)[1].timeDif = timeDif
        self.host.sendClient(clientID,"ST" + str(timeDif))

    def __dealSynDelay(self, clientID, msg):
        self.host.sendClient(clientID, "SD" + msg)

    # </editor-fold>

    # <editor-fold desc="重连信息">

    # 处理用户重连信息
    def __dealReconnect(self, clientID, username):
        res, user = self.host.getClient(clientID)
        if res != 0:
            return
        hasUser = False
        for client in self.host.clients:
            if client.username == username:
                self.__dealReconnect_DataMigrate(client, user, username)
                hasUser = True
        if not hasUser:
            self.__reconnect_Relax(clientID, username)

    # 将重连前的数据转移到新客户端上
    def __dealReconnect_DataMigrate(self, oldClient, newClient, username):
        if oldClient.userState != conf.USER_STATE_GAME:
            # 用户断线前不在游戏，直接让用户进入大厅
            self.__reconnect_Relax(newClient.hid, username)

    # 用户断线前不在游戏中，直接让用户进入大厅
    def __reconnect_Relax(self, clientID, username):
        for client in self.host.clients:
            if client.username == username and client.hid != clientID:
                # 挤掉原有用户
                if client.userState == conf.USER_STATE_ROOM:
                    self.lobby.quitRoom(client.room, client.userID_Room)
                client.userID = 0
                client.username = ""
                client.userState = 0
                client.room = 0
                client.userID_Room = 0
                self.host.sendClient(client.hid, 'QA')
                self.host.closeClient(client.hid)

        # 向客户端反馈登录成功
        clientMsg = self.sql.getUserMsg(username)
        userID = clientMsg[0]
        HP = clientMsg[1]
        ammo = clientMsg[2]
        LV = clientMsg[3]
        EXP = clientMsg[4]
        # 向客户端发送用户数据
        self.host.sendClient(clientID, 'ER' + str(userID) + ' ' + str(username) \
                             + ' ' + str(HP) + ' ' + str(ammo) + ' ' + str(LV) + ' ' + str(EXP))
        # 将用户信息添加到服务端上
        res, user = self.host.getClient(clientID)
        if res != 0:
            return
        user.userID = userID
        user.username = str(username)
        user.userState = conf.USER_STATE_LOBBY

    # </editor-fold>

    # <editor-fold desc="游戏主体部分">

    def tickGame(self):
        for roomIndex in self.runGame.keys():
            self.gaming(self.runGame[roomIndex])
            self.sending(self.runGame[roomIndex])

    def sending(self, runGame):
        if runGame.ready:
            runGame.sendAllPlayerWithPlayerMsg()
            runGame.sendAllPlayerWithEnemyMsg()
        else:
            runGame.sendAllPlayerWithPlayerProcess()

    def __dealGame(self, clinetID, msg):
        temp = msg.split(' ')
        roomID = int(temp[0])
        msg = msg[len(temp[0]) + 1:]
        self.gameMsg[roomID].append(msg)

    def gaming(self, runGame):
        runGame.process()
        roomID = runGame.roomID
        while len(self.gameMsg[roomID]) > 0:
            msg = self.gameMsg[roomID][0]
            self.__dealGameMsg(runGame, msg)
            self.gameMsg[roomID].remove(msg)

    def __dealGameMsg(self, runGame, msg):
        type = self.parse.parseGameType(msg)
        msg = msg[1:]
        if type == conf.MSG_GAME_UPDATE:
            self.__dealGameMSG_Update(runGame, msg)
        elif type == conf.MSG_GAME_LOAD:
            self.__dealGameMSG_Load(runGame, msg)

    def __dealGameMSG_Update(self, runGame, msg):
        type = self.parse.parseGame_UpdateType(msg)
        msg = msg[1:]
        if type == conf.MSG_GAME_UPDATE_CHANGEMOTION:
            self.__dealGameMsg_Update_ChangeMotion(runGame, msg)
        elif type == conf.MSG_GAME_UPDATE_CHANGEMOVE:
            self.__dealGameMsg_Update_ChangeMove(runGame, msg)
        elif type == conf.MSG_GAME_UPDATE_CHANGEROT:
            self.__dealGameMsg_Update_ChangeRot(runGame, msg)
        elif type == conf.MSG_GAME_UPDATE_CHANGEATTACK:
            self.__dealGameMSG_Update_ChangeAttack(runGame, msg)
        elif type == conf.MSG_GAME_UPDATE_DAMAGE:
            self.__dealGameMSG_Update_Damage(runGame,msg)

    def __dealGameMSG_Update_Damage(self,runGame,msg):
        enemyID,damage = self.parse.parseGame_Update_Damage(msg)
        #runGame.getEnemy(enemyID).damage(damage)
        runGame.getEnemy(enemyID).setState(gameConf.ENEMY_STATE_DIZZY)

    def __dealGameMSG_Update_ChangeAttack(self,runGame,msg):
        username,attack,isHit,pos,hitTarget = self.parse.parseGame_Update_ChangeAttack(msg)
        runGame.changeAtk(username,attack)
        playerID = runGame.getPlayer(username).userID
        if isHit:
            enemy = runGame.getEnemy(hitTarget)
            if enemy:
                enemy.damage(20)
            message = "GA" + str(playerID) + " " + str(pos.x) + " " + str(pos.y) + " " + str(pos.z) + \
                      " " + str(hitTarget)
            runGame.sendAllPlayer(message)

    def __dealGameMsg_Update_ChangeRot(self, runGame, msg):
        username, clientTime, rotY, rotSpeed, lookPosY = self.parse.parseGame_Update_ChangeRot(msg)
        rot = runGame.changeRot(username,clientTime,rotY,rotSpeed,lookPosY,self.startTime)
        playerID = runGame.getPlayer(username).userID
        message = "GUR" + str(playerID) + " " + str(time.time() - self.startTime) + " " + str(rot) + " " + \
                    str(rotSpeed) + " " + str(lookPosY)
        #runGame.sendAllPlayer(message)

    def __dealGameMsg_Update_ChangeMotion(self, runGame, msg):
        username, clientTime, motion = self.parse.parseGame_Update_ChangeMotion(msg)
        pos = runGame.changeMotion(username, clientTime, motion, self.startTime)
        playerID = runGame.getPlayer(username).userID
        message = "GUV" + str(playerID) + " " + str(time.time() - self.startTime) + " " + str(pos.x) + " " + \
                  str(pos.y) + " " + str(pos.z) + " " + str(motion)
        #runGame.sendAllPlayer(message)

    def __dealGameMsg_Update_ChangeMove(self, runGame, msg):
        username, clientTime, move = self.parse.parseGame_Update_ChangeMove(msg)
        pos = runGame.changeMove(username, clientTime, move, self.startTime)
        playerID = runGame.getPlayer(username).userID
        message = "GUV" + str(playerID) + " " + str(time.time() - self.startTime) + " " + str(pos.x) + " " + \
                  str(pos.y) + " " + str(pos.z) + " " + str(move)
        #runGame.sendAllPlayer(message)

    def __dealGameMSG_Load(self, runGame, msg):
        playerID, process = self.parse.parseGame_Load(msg)
        player = runGame.getPlayer(playerID)
        player.process = process
        if (runGame.couldStart()):
            runGame.ready = True
            runGame.sendAllPlayer("GLREADY")

    # </editor-fold>

    # <editor-fold desc="大厅信息处理">

    # 处理大厅信息，包括获取房间数据，创建房间，加入房间等
    def __dealLobby(self, clientID, msg):
        msgType = self.parse.parseLobbyType(msg)
        msg = msg[1:]
        if msgType == conf.MSG_UNMEANING:
            return
        elif msgType == conf.MSG_LOBBY_CREATEROOM:
            # 创建房间
            self.__dealLobby_CreateRoom(clientID, msg)
        elif msgType == conf.MSG_LOBBY_JOINROOM:
            # 加入房间
            self.__dealLobby_JoinRoom(clientID, msg)
        elif msgType == conf.MSG_LOBBY_QUITROOM:
            # 退出房间
            self.__dealLobby_QuitRoom(clientID, msg)
        elif msgType == conf.MSG_LOBBY_GETROOMMSG:
            # 获得大厅的房间数据
            self.__dealLobby_GetRoomMsg(clientID, msg)
        elif msgType == conf.MSG_LOBBY_READY:
            # 用户准备/取消准备
            self.__dealLobby_Ready(clientID, msg)
        elif msgType == conf.MSG_LOBBY_START:
            # 用户开始游戏
            self.__dealLobby_Start(clientID, msg)

    # 创建房间
    def __dealLobby_CreateRoom(self, clientID, msg):
        map, maxUserNum = self.parse.parseLobby_CreateRoom(msg)
        room = self.lobby.createRoom()
        room.map = int(map)
        room.limitUserNum = int(maxUserNum)
        room.houseOwner = 1
        res, client = self.host.getClient(clientID)
        if res != 0:
            return
        self.lobby.joinRoom(room.roomID, client)
        self.__sendRoomMsg(room.roomID)

    # 加入房间
    def __dealLobby_JoinRoom(self, clientID, msg):
        roomID = int(msg)
        res, user = self.host.getClient(clientID)
        if res != 0:
            return
        res, userID_Room = self.lobby.joinRoom(roomID, user)
        if res:
            self.__sendRoomMsg(roomID)
        else:
            # 加入房间失败
            self.host.sendClient(clientID, 'BJFAIL')

    # 退出房间
    def __dealLobby_QuitRoom(self, clientID, msg):
        roomID = int(msg)
        res, user = self.host.getClient(clientID)
        if res != 0:
            return
        userID_Room = user.userID_Room
        self.lobby.quitRoom(roomID, userID_Room)
        self.host.sendClient(clientID, 'BQOK')
        self.__sendRoomMsg(roomID)

    # 获得大厅的所有房间信息
    def __dealLobby_GetRoomMsg(self, clientID, msg):
        roomMsg = ''
        for index in self.lobby.rooms.keys():
            room = self.lobby.rooms[index]
            # 不返回已开始游戏的房间
            if room.started:
                continue
            roomID = room.roomID
            map = room.map
            nowUserNum = room.nowUserNum
            limitUserNum = room.limitUserNum
            roomMsg += str(roomID) + ' ' + str(map) + ' ' + str(nowUserNum) + ' ' + str(limitUserNum) + ' '
        self.host.sendClient(clientID, 'BG' + roomMsg)

    # 用户准备/取消准备
    def __dealLobby_Ready(self, clientID, msg):
        room = self.lobby.getRoom(int(msg))
        res, user = self.host.getClient(clientID)
        if res != 0:
            return
        userID_Room = user.userID_Room
        room.ready[userID_Room] = not room.ready[userID_Room]
        self.__sendRoomMsg(room.roomID)

    # 用户开始游戏
    def __dealLobby_Start(self, clientID, msg):
        room = self.lobby.getRoom(int(msg))
        if room.couldStart():
            # self.host.sendClient(clientID,'BSOK')
            self.__start(room)
        else:
            self.host.sendClient(clientID, 'BSFAIL')

    # 创建一个游戏线程
    def __start(self, room):
        players = []
        msg = "GS" + str(room.roomID) + " " + str(room.map) + " " + str(room.nowUserNum) + " "
        # 初始化房间内的所有用户信息
        for userID in room.users.keys():
            user = room.users[userID]
            msg += str(userID) + " " + user.username + " "
            userId, HP, ammo, LV, EXP = self.sql.getUserMsg(user.username)
            p = Player(user, HP, ammo, LV, EXP)
            if userID == 1:
                p.pos = Vector3(50, 0, 50)
            elif userID == 2:
                p.pos = Vector3(40, 0, 40)
            elif userID == 3:
                p.pos = Vector3(60, 0, 60)
            msg += str(p.pos.x) + " " + str(p.pos.y) + " " + str(p.pos.z) + " "
            msg += str(p.rotation.x) + " " + str(p.rotation.y) + " " + str(p.rotation.z) + " "
            players.append(p)
        newGame = Game(self.host, room.map, room.roomID, players,self.startTime)
        room.started = True
        for userID_Room in room.users.keys():
            client = room.users[userID_Room]
            clientID = client.hid
            client.userState = conf.USER_STATE_GAME
            self.host.sendClient(clientID, msg)
        self.gameMsg[room.roomID] = []
        self.runGame[room.roomID] = newGame
        # thread.start_new_thread(self.gaming, (newGame,))
        # thread.start_new_thread(self.sending, (newGame,))

    # 将房间信息发送给客户端
    def __sendRoomMsg(self, roomID):
        msg = 'BR'
        room = self.lobby.getRoom(roomID)
        if room == -1:
            return
        roomID = str(room.roomID)
        map = str(room.map)
        nowUserNum = str(room.nowUserNum)
        limitUserNum = str(room.limitUserNum)
        msg += roomID + ' ' + map + ' ' + nowUserNum + ' ' + limitUserNum + ' '
        for userID_Room in room.users.keys():
            user = room.users[userID_Room]
            ready = room.ready[userID_Room]
            userID_Room = str(user.userID_Room)
            username = user.username
            msg += userID_Room + ' ' + username + ' ' + str(ready) + ' '
        for userID_Room in room.users.keys():
            clientID = room.users[userID_Room].hid
            self.host.sendClient(clientID, msg)

    # </editor-fold>

    # <editor-fold desc="登录界面处理">

    # 处理用户注册信息
    def __dealRegister(self, clientID, msg):
        # 解析注册信息
        username, password = self.parse.parseRegister(msg)
        if self.sql.insert(username, password):
            # 向客户端反馈注册成功
            self.host.sendClient(clientID, 'ROK')
        else:
            # 向客户端反馈注册失败
            self.host.sendClient(clientID, 'RFAIL')

    # 处理用户登录信息
    def __dealLogin(self, clientID, msg):
        # 解析登录信息
        username, password = self.parse.parseLogin(msg)
        if self.sql.checkPassword(username, password):
            for client in self.host.clients:
                if client and client.username == username:
                    # 挤掉原有用户
                    client.userID = 0
                    client.username = ""
                    client.userState = 0
                    client.room = 0
                    client.userID_Room = 0
                    self.host.sendClient(client.hid, 'QA')
                    self.host.closeClient(client.hid)

            # 向客户端反馈登录成功
            clientMsg = self.sql.getUserMsg(username)
            userID = clientMsg[0]
            HP = clientMsg[1]
            ammo = clientMsg[2]
            LV = clientMsg[3]
            EXP = clientMsg[4]
            # 向客户端发送用户数据
            self.host.sendClient(clientID, 'LOK ' + str(userID) + ' ' + str(username) \
                                 + ' ' + str(HP) + ' ' + str(ammo) + ' ' + str(LV) + ' ' + str(EXP))
            # 将用户信息添加到服务端上
            res, user = self.host.getClient(clientID)
            if res != 0:
                return
            user.userID = userID
            user.username = str(username)
            user.userState = conf.USER_STATE_LOBBY


        else:
            # 向客户端反馈登录失败
            self.host.sendClient(clientID, 'LFAIL')

    # </editor-fold>

    def __clearClient(self, client):
        for pos in xrange(len(self.host.clients)):
            if self.host.clients[pos] and self.host.clients[pos].hid == client.hid:
                self.host.clients[pos] = None
                client.close()
                print "断开连接", client.hid
                del client
                self.host.count -= 1
                return

    def tick(self):
        self.host.process()
        for index in xrange(len(self.host.queue)):
            event = self.host.read()
            eventType = event[0]
            clientID = event[1]
            clientMsg = event[2]
            if eventType == conf.NET_CONNECTION_DATA:  # 收到消息
                msgs = self.parse.simple(clientMsg)
                for msg in msgs:
                    if msg == conf.MSG_UNMEANING:
                        # 收到无意义信息 忽视
                        continue
                    self.__dealMsg(clientID, msg)
            elif eventType == conf.NET_CONNECTION_LEAVE:
                # 用户断线
                res, client = self.host.getClient(clientID)
                if res != 0:
                    return
                pos = int(clientMsg)
                if client.userState == conf.USER_STATE_ROOM:
                    # 用户掉线前若在房间内，则退出房间
                    roomID = client.room
                    self.lobby.quitRoom(roomID, client.userID_Room)
                    self.__sendRoomMsg(roomID)
                elif client.userState == conf.USER_STATE_GAME:
                    # 用户掉线前在游戏中，则将用户标记为离线状态，不进行清理
                    client.lost = True
                    return
                self.__clearClient(client)
        self.tickGame()

        return


def checkConnect(host):
    pass
    # t = time.time()
    # while 1:
    #    print(time.time() - t)
    #    time.sleep(0.001)


server = SimpleServer()
server.connect(12345)
thread.start_new_thread(checkConnect, (server.host,))
while (1):
    server.tick()
    time.sleep(0.1)
