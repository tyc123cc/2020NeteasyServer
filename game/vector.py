# -*- coding: utf-8 -*-

import math


class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @staticmethod
    def distance(one,other):
        return math.sqrt(math.pow(one.x - other.x,2) + math.pow(one.y - other.y,2))

    def __repr__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"

    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return Vector2(self.x * other, self.y * other)

    def __div__(self, other):
        return Vector2(self.x / other, self.y / other)

    def __eq__(self, other):
        if self.x == other.x and self.y == other.y:
            return True
        else:
            return False

    def __ne__(self, other):
        if self.x == other.x and self.y == other.y:
            return False
        else:
            return True


    # 旋转向量
    def rotate(self, angle):
        radian = float(angle) / 180 * math.pi
        x = self.x * math.cos(radian) + self.y * math.sin(radian)
        y = -self.x * math.sin(radian) + self.y * math.cos(radian)
        self.x = x
        self.y = y

    # 返回旋转后的值（不改变该向量）
    def rawRotate(self,angle):
        radian = float(angle) / 180 * math.pi
        x = self.x * math.cos(radian) + self.y * math.sin(radian)
        y = -self.x * math.sin(radian) + self.y * math.cos(radian)
        return Vector2(x,y)


class Vector3:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return "(" + str(self.x) + "," + str(self.y) + "," + str(self.z) + ")"

    def __add__(self, other):
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other):
        return Vector3(self.x * other, self.y * other, self.z * other)

if __name__ == '__main__':
    v = Vector2(1, 1)
    v1 = Vector2(1, 2)
    print(Vector2.distance(v,v1))
