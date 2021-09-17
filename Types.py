import math
import time
def ShootColdDown(Time,gameObject):
    gameObject.IsShootReady = False
    time.sleep(Time)
    gameObject.IsShootReady = True
class Vector2:
    def __init__(self,x,y):
        self.x = x
        self.y = y
    def ToArray(self):
        return [self.x, self.y]
    def __add__(self, other):
        return  Vector2(self.x + other.x,self.y + other.y)
    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)
    def __mul__(self, other):
        return Vector2(self.x * other.x, self.y * other.y)
    @staticmethod
    def Distance(Point1,Point2):
        return math.sqrt( (Point2.x-Point1.x)**2 + (Point2.y - Point1.y)**2 )
    @staticmethod
    def Forward(transform):
        x = math.cos(transform.rotation)
        y = math.sin(transform.rotation)
        return Vector2(x,y)
    @staticmethod
    def LookAt(objPos, Target):
        Vector = Vector2(Target.x - objPos.x,Target.y-objPos.y)
        return math.atan2(Vector.y,Vector.x)

    @staticmethod
    def LocalToGloablPoint(Point, Origin, Child=None):
        ret = []
        B = Point
        A = Vector2(0,0)
        relativeX = B.x - A.x
        relativeY = B.y - A.y
        Angle = Origin.transform.rotation
        rotatedX = math.cos(Angle) * relativeX - math.sin(Angle) * relativeY
        rotatedY = math.sin(Angle) * relativeX + math.cos(Angle) * relativeY
        ret += [rotatedX, rotatedY]
        return ret

    @staticmethod
    def LocalToGloabl(Points, Origin, Child = None):
        if(Child == None):
            Child = Vector2(0,0)
        ret = []
        for Point in Points.vertexes:
            B = Point*Origin.transform.scale
            A = Vector2(0,0)
            relativeX = B.x - A.x
            relativeY = B.y - A.y
            Angle = Origin.transform.rotation
            rotatedX = math.cos(Angle) * relativeX - math.sin(Angle) * relativeY
            rotatedY = math.sin(Angle) * relativeX + math.cos(Angle) * relativeY
            ret += [rotatedX,rotatedY]
        return ret


MeshBox = (Vector2(-1,-1), Vector2(-1,1), Vector2(1,1), Vector2(1,-1))
MeshGun = (Vector2(0,-1), Vector2(0,1), Vector2(2,1), Vector2(2,-1))
MeshCircle = 1.0

class Transform:
    def __init__(self,position,rotation,scale):
        self.position = position
        self.rotation = rotation
        self.scale = scale
    def GlobalPos(self,GameObject):
        Central = Vector2.LocalToGloablPoint(self.position, GameObject)
        return Vector2(GameObject.transform.position.x + Central[0], GameObject.transform.position.y + Central[1])
class Mesh:
    def __init__(self,vertexes,color):
        self.vertexes = vertexes
        self.color = color
class Collider:
    def isCollide(self, other):
        return self.map[type(other)](other)

class CircleCollider(Collider):
    def __init__(self, R, parent=None):
        self.parent = parent
        self.R = R
        self.map = {
            CircleCollider: self.InsideCircle,
            RectCollider: self.InsdieRect,
            PointCollider: self.InsidePoint
        }
    def InsideCircle(self, other):
        pass
    def InsidePoint(self, other):
        pass
    def InsdieRect(self, other):
        pass

class RectCollider(Collider):
    def __init__(self, LeftUpperPoint, RightBottomPoint, parent = None):
        self.parent = parent
        self.LeftUpperPoint = LeftUpperPoint
        self.RightBottomPoint = RightBottomPoint
        self.map = {
            CircleCollider: self.InsideCircle,
            RectCollider: self.InsdieRect,
            PointCollider: self.InsidePoint
        }
    def InsideCircle(self, other):
        pass
    def InsidePoint(self, other):
        pass
    def InsdieRect(self, other):
        pass



class PointCollider(Collider):
    def __init__(self, parent = None):
        self.parent = parent
        self.map = {
            CircleCollider: self.InsideCircle,
            RectCollider: self.InsdieRect,
            PointCollider: self.InsidePoint
        }
    def InsideCircle(self, other):
        return True if Vector2.Distance(self.parent.transform.position,other.parent.transform.position) < other.R else False
    def InsidePoint(self, other):
        return True if self.parent.transform.position == other.parent.transform.position else False
    def InsdieRect(self, other):
        #if(Vector2.Distance(self.parent.transform.position,other.parent.transform.position) > other.LeftUpperPoint.x - other.LeftUpperPoint.y):
            #return False
        B = self.parent.transform.position
        A = other.parent.transform.position
        relativeX = B.x - A.x
        relativeY = B.y - A.y
        Angle = other.parent.transform.rotation
        rotatedX = math.cos(Angle) * relativeX - math.sin(Angle) * relativeY
        rotatedY = math.sin(Angle) * relativeX + math.cos(Angle) * relativeY
        return False
