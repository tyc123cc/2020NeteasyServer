# -*- coding: utf-8 -*-

from room import Room

# 大厅类，包含大厅中的房间大致信息
class Lobby:
    def __init__(self):
        self.rooms = {}
        self.roomsNum = 0
        self.bufferRooms = []

    def createRoom(self):
        if len(self.bufferRooms) > 0:
            roomID = self.bufferRooms[0]
            self.bufferRooms.pop(0)
        else:
            self.roomsNum += 1
            roomID = self.roomsNum
        room = Room(roomID)
        self.rooms[roomID] = room
        return room

    def getRoom(self,roomID):
        if not self.rooms.has_key(roomID):
            return -1
        return self.rooms[roomID]

    def joinRoom(self,roomID,user):
        room = self.getRoom(roomID)
        if room == -1:
            return False,0
        if room.joinUser(user):
            return True,room.nowUserNum
        else:
            return False,0

    def quitRoom(self,roomID,userID_Room):
        room = self.getRoom(roomID)
        if room == -1:
            return
        room.removeUser(userID_Room)
        # 房间无人，将该房间编号放入缓冲房间中
        if room.nowUserNum == 0:
            self.bufferRooms.append(roomID)
            self.rooms.pop(roomID)