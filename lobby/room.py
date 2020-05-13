# -*- coding: utf-8 -*-
import sys
sys.path.append('../common')

import conf

# 房间类  包含房间具体信息
class Room:

    def __init__(self, roomID):
        self.roomID = roomID
        self.users = {}
        self.ready = {}
        self.map = 0
        self.limitUserNum = 0
        self.nowUserNum = 0
        self.houseOwner = 1
        self.started = False

    # 修改地图
    def changeMap(self,mapID):
        self.map = mapID

    # 新用户加入房间
    def joinUser(self,user):
        # 房间人数已满
        if self.nowUserNum == self.limitUserNum or self.started:
            return False
        self.nowUserNum += 1
        self.users[self.nowUserNum] = user
        self.ready[self.nowUserNum] = False
        user.userState = conf.USER_STATE_ROOM
        user.room = self.roomID
        user.userID_Room = self.nowUserNum
        return True

    # 用户退出房间
    def removeUser(self,userID_Room):
        self.users[userID_Room].room = 0
        self.users[userID_Room].userID_Room = 0
        self.users[userID_Room].usersState = conf.USER_STATE_LOBBY
        for i in range(userID_Room,self.nowUserNum):
            self.users[i] = self.users[i + 1]
            self.users[i].userID_Room = i
            self.ready[i] = self.ready[i + 1]
        self.users.pop(self.nowUserNum)
        self.ready.pop(self.nowUserNum)
        self.nowUserNum -= 1
        # 房主退出后房主自动转给新的1号玩家
        if userID_Room == self.houseOwner and self.nowUserNum > 0:
            self.houseOwner = 1
            self.ready[1] = False

    # 用户准备/取消准备
    def ready(self,userID_Room):
        self.ready[userID_Room] = not self.ready[userID_Room]

    # 判断房间是否可以开始游戏
    def couldStart(self):
        # 全部玩家准备完毕即可开始游戏
        for i in self.ready.keys():
            if i != 1 and self.ready[i] is False:
                return False
        return True
