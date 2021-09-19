import math
import time
import threading
def ShootColdDown(Time,gameObject):
    gameObject.IsShootReady = False
    time.sleep(Time)
    gameObject.IsShootReady = True
def BlowUp(gameObject):

    TimeTolIve = gameObject.Time
    FullScale = gameObject.transform.scale.x
    while(gameObject.Time > 0):
        gameObject.Time -= 0.1
        Calc = TimeTolIve/2
        if(gameObject.Time > Calc):
           EndSize = FullScale*(1-(gameObject.Time - Calc)/(TimeTolIve-Calc))
        else:
           EndSize = (FullScale * ((gameObject.Time) / (TimeTolIve - Calc)))
        gameObject.transform.scale = Vector2(EndSize,EndSize)
        time.sleep(0.1)


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
    def __truediv__(self, other):
        return Vector2(self.x / other.x, self.y / other.y)
    @staticmethod
    def Distance(Point1,Point2):
        return math.sqrt((Point2.x-Point1.x)**2 + (Point2.y - Point1.y)**2)
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
    def LocalToGloabl(Points, Origin):
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
    @staticmethod
    def Rotate(Angule,Points,Pos = [0,0]):
        ret = []
        if(type(Pos) != Vector2):
            Pos = Vector2(Pos[0],Pos[1])
        for Point in Points:
            B = Point
            A = Pos
            relativeX = B.x - A.x
            relativeY = B.y - A.y
            Angle = Angule
            rotatedX = math.cos(Angle) * relativeX - math.sin(Angle) * relativeY
            rotatedY = math.sin(Angle) * relativeX + math.cos(Angle) * relativeY
            ret += [Vector2(rotatedX, rotatedY)]
        return ret

MeshBox = (Vector2(-1,-1), Vector2(-1,1), Vector2(1,1), Vector2(1,-1))
MeshGun = (Vector2(0,-1), Vector2(0,1), Vector2(2,1), Vector2(2,-1))
MeshCircle = 1.0
class Ai:
    def __init__(self,Target,Me,Bullet,MoveDistance = 200, ShootDistance = 300):
        self.Target = Target
        self.Myself = Me
        self.MoveDistance = MoveDistance
        self.ShootDistance = ShootDistance
        self.Bullet = Bullet
    def AiMoveTo(self):
        Target = self.Target
        obj = self.Myself
        if (Vector2.Distance(Target.transform.position, obj.transform.position) > self.MoveDistance):
            To = Target.transform.position - obj.transform.position
            obj.transform.position += To * Vector2(obj.speed,obj.speed)
            obj.transform.rotation = Vector2.LookAt(obj.transform.position, Target.transform.position)
    def AiLookAt(self):
        Target = self.Target
        obj = self.Myself
        obj.ChildObjects[obj.Tower].transform.rotation = Vector2.LookAt(obj.transform.position, Target.transform.position)
    def Shoot(self,window):
        if(self.Myself.IsShootReady and Vector2.Distance(self.Myself.transform.position,self.Target.transform.position) < self.ShootDistance):
            obj = self.Myself
            bul = self.Bullet()
            bul.Tag = "EnBullet"
            bul.transform.position = obj.ChildObjects[obj.Tower].transform.GlobalPos(obj)
            bul.transform.rotation = obj.ChildObjects[obj.Tower].transform.rotation
            bul.transform.position += Vector2.Forward(bul.transform) * Vector2(25, 25)
            window.AddObject(bul)
            self.Myself.IsShootReady = False
            ColdDown_thread = threading.Thread(target=ShootColdDown, args=(obj.ReloadSpeed, obj),daemon=True)
            ColdDown_thread.start()
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
        }
    def InsideCircle(self, other):
        if(Vector2.Distance(self.parent.transform.position,other.parent.transform.position) > self.R + other.R):
            return False
        return True
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
        }
    def InsideCircle(self, other):
        pass
    def InsdieRect(self, other):
        if (Vector2.Distance(Vector2(0,0), self.LeftUpperPoint) > Vector2.Distance(Vector2(0,0), self.RightBottomPoint)):
            p1 = Vector2.Distance(Vector2(0,0), self.LeftUpperPoint)
        else:
            p1 =Vector2.Distance(Vector2(0,0), self.RightBottomPoint)

        if (Vector2.Distance(Vector2(0,0), other.LeftUpperPoint) > Vector2.Distance(Vector2(0,0), other.RightBottomPoint)):
            p2 = Vector2.Distance(Vector2(0,0), other.LeftUpperPoint)
        else:
            p2 = Vector2.Distance(Vector2(0,0), other.RightBottomPoint)

        if(Vector2.Distance(self.parent.transform.position,other.parent.transform.position) > p1 + p2):
            return False


        pos = self.parent.transform.position
        mesh1 = [self.LeftUpperPoint,self.RightBottomPoint]

        pos2 = other.parent.transform.position
        mesh2 = [other.LeftUpperPoint, other.RightBottomPoint]

        mesh1 = Vector2.Rotate(self.parent.transform.rotation, mesh1)
        mesh1 = [mesh1[0] +pos, mesh1[1] + pos]

        mesh2 = Vector2.Rotate(other.parent.transform.rotation, mesh2)
        mesh2 = [mesh2[0] + pos2, mesh2[1] + pos2]

        mesh1 = Vector2.Rotate(-self.parent.transform.rotation, mesh1,pos)
        mesh2 = Vector2.Rotate(-self.parent.transform.rotation, mesh2,pos)

        mesh2 = [mesh2[0] + pos, mesh2[1] + pos]
        mesh1 = [mesh1[0] + pos, mesh1[1] + pos]



        if(mesh2[0].x > mesh1[0].x and mesh2[0].y > mesh1[0].y and mesh2[0].x < mesh1[1].x and mesh2[0].y < mesh1[1].y):
            return True
        if (mesh2[1].x > mesh1[0].x and mesh2[1].y > mesh1[0].y and mesh2[1].x < mesh1[1].x and mesh2[1].y < mesh1[1].y):
            return True
        return False



