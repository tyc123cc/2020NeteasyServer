# -*- coding: utf-8 -*-

import sqlite3
import os


class Sql(object):

    def __init__(self):
        pass

    def createTable(self):
        # 创建用户表
        if not os.path.exists("game.db"):
            conn = sqlite3.connect('game.db')
            c = conn.cursor()
            c.execute('''CREATE TABLE USER
            (ID              INTEGER PRIMARY KEY     AUTOINCREMENT,
             USERNAME        VARCHAR(20) NOT NULL UNIQUE ,
             PASSWORD        VARCHAR(20));''')
            print "User Table created successfully"
            # 创建数据表
            c.execute('''CREATE TABLE DATA
            (ID              INTEGER PRIMARY KEY UNIQUE ,
             HP              INT,
             AMMO            INT,
             LV              INT,
             EXP             INT
             );''')
            print "Data Table created successfully"
            conn.commit()
            conn.close()

    # 插入用户数据，当新用户注册时调用
    def insert(self, username, password):
        if not os.path.exists("game.db"):
            self.createTable()
        if not self.checkUsername(username):
            return False
        conn = sqlite3.connect('game.db')
        c = conn.cursor()
        c.execute("INSERT INTO USER (USERNAME,PASSWORD) \
                              VALUES ('" + username + "','" + password + "')");
        conn.commit()
        print "Records insert to user successfully";
        userid = self.getID(username)
        if userid == 0:
            c.execute("DELETE from USER where username = '" + username + "';")
            conn.commit()
            conn.close()
            return False
        c.execute("INSERT INTO DATA (ID,HP,AMMO,LV,EXP) \
               VALUES (" + str(userid) + ",100,100,1,0 )");
        conn.commit()
        print "Records insert to data successfully";
        conn.close()
        return True

    # 更新用户数据，当用户结束一局游戏时调用
    def update(self, username, HP, ammo, LV, EXP):
        if not os.path.exists("game.db"):
            self.createTable()
        userid = self.getID(username)
        if userid == 0:
            return False
        conn = sqlite3.connect('game.db')
        c = conn.cursor()
        c.execute("UPDATE DATA set \
                    HP = '" + str(HP) + "',AMMO = '" + str(ammo) + "',LV = '" + str(LV) + "',EXP = '" + str(EXP) + "' \
                    where ID = " + str(userid))
        conn.commit()
        print "Update Successfully"
        conn.close()
        return True

    # 删除数据库
    def __deleteSQL(self):
        if not os.path.exists("game.db"):
            os.remove("user.db")
        if not os.path.exists("game.db"):
            return True
        else:
            return False

    # 通过用户名获取用户ID
    def getID(self, username):
        if not os.path.exists("game.db"):
            self.createTable()
        conn = sqlite3.connect('game.db')
        c = conn.cursor()
        cursor = c.execute("SELECT ID FROM USER WHERE USERNAME = '" + username + "'");
        userid = 0
        for row in cursor:
            userid = row[0]
        conn.close()
        return userid

    # 通过用户名获得DATA表中的数据
    def getUserMsg(self, username):
        userId = self.getID(username)
        HP = 0
        ammo = 0
        LV = 0
        EXP = 0
        conn = sqlite3.connect('game.db')
        c = conn.cursor()
        cursor = c.execute("SELECT HP,AMMO,LV,EXP FROM DATA WHERE ID = " + str(userId));
        for row in cursor:
            HP = row[0]
            ammo = row[1]
            LV = row[2]
            EXP = row[3]
        conn.close()
        return userId, HP, ammo, LV, EXP

    # 检查用户名与密码是否匹配
    def checkPassword(self, username, password):
        if not os.path.exists("game.db"):
            self.createTable()
        conn = sqlite3.connect('game.db')
        c = conn.cursor()
        userPassword = ""
        cursor = c.execute("SELECT  PASSWORD FROM USER WHERE USERNAME = '" + username + "'");
        for row in cursor:
            userPassword = row[0]
        conn.close()
        if userPassword == '':
            return False
        elif userPassword == password:
            return True
        else:
            return False

    # 检查用户名是否可用
    def checkUsername(self, username):
        if not os.path.exists("game.db"):
            self.createTable()
        conn = sqlite3.connect('game.db')
        if username.strip() == '':
            return False
        c = conn.cursor()
        cursor = c.execute("SELECT  USERNAME FROM USER WHERE USERNAME = '" + username + "'");
        name = ''
        for row in cursor:
            name = row[0]
        conn.close()
        if name == '':
            return True
        else:
            return False

if __name__ == '__main__':
    sql = Sql()
    print sql.update('wy123',100,100,1,0)
