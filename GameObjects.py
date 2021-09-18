import Controll
import  Types
import threading
class GameObject:
    ChildObjects = None
    def __init__(self,transform = None, collider = None, Mesh = None, ChildObjects = None, tag = None):
        self.transform = transform
        self.collider = collider
        self.mesh = Mesh
        self.ChildObjects = ChildObjects
        self.Tag = tag
    def Do(self,window = None):
        pass

class Tank(GameObject):
    def __init__(self,tag = "Tank",RotSpeed = 0.2,speed = 2 ,Color = (64,64,64),Color2 = (65,105,225),scale = Types.Vector2(1,1),ReloadSpeed = 1, Ai = None, AttackDistance = 200):
        self.Tower = 3
        self.transform = Types.Transform(Types.Vector2(300,300),0,Types.Vector2(10,5)*scale)
        self.collider = Types.RectCollider(Types.MeshBox[0]*self.transform.scale,Types.MeshBox[2]*self.transform.scale,self)
        self.mesh = Types.Mesh(Types.MeshBox,Color)
        self.speed = speed
        self.RotSpeed = RotSpeed
        self.Tag = tag
        self.IsShootReady = True
        self.ReloadSpeed = ReloadSpeed
        self.ai = None if Ai == None else Types.Ai(Ai,self,Bullet,AttackDistance)
        CObj1 = GameObject(transform=Types.Transform(Types.Vector2(-7,-4) * scale,0,Types.Vector2(3,1.5) * scale),
                           Mesh=Types.Mesh(Types.MeshBox,Color2))
        CObj2 = GameObject(transform=Types.Transform(Types.Vector2(-7,4)* scale, 0, Types.Vector2(3, 1.5)* scale),
                           Mesh=Types.Mesh(Types.MeshBox, Color2))
        CObj3 = GameObject(transform=Types.Transform(Types.Vector2(3, 0)* scale, 0, Types.Vector2(3.5,2)* scale),
                           Mesh=Types.Mesh(Types.MeshCircle, Color2))
        CObj4 = GameObject(transform=Types.Transform(Types.Vector2(3, 0)* scale, 0, Types.Vector2(7, 1.5)* scale),
                           Mesh=Types.Mesh(Types.MeshGun, Color2))
        CObj4.Tag = "Gun"
        self.ChildObjects = (CObj1,CObj2,CObj3,CObj4)
    def Do(self,window = None):
        if self.ai != None:
            self.ai.AiLookAt()
            self.ai.AiMoveTo()
            self.ai.Shoot(window)
class Bullet(GameObject):
    def __init__(self, tag="Bullet", speed=5, Color=(255, 0, 0),scale=Types.Vector2(1, 1)):
        self.transform = Types.Transform(Types.Vector2(300, 300), 0, Types.Vector2(3, 1) * scale)
        self.collider = Types.RectCollider(Types.MeshBox[0]*scale,Types.MeshBox[2]*scale,self)
        self.mesh = Types.Mesh(Types.MeshBox, Color)
        self.speed = speed
        self.Tag = tag
    def Do(self,window = None):
        self.transform.position += Types.Vector2.Forward(self.transform) * Types.Vector2(self.speed,self.speed)
class Blow(GameObject):
    def __init__(self,scale = Types.Vector2(7,7),Color = (255,0,0),Color2 = (255,255,0),Time = 0.7):
        self.Time = Time
        self.transform = Types.Transform(Types.Vector2(300, 300), 0, Types.Vector2(2, 2) * scale)
        self.collider = None
        self.mesh = Types.Mesh(Types.MeshCircle, Color)

        CObj1 = GameObject(transform=Types.Transform(Types.Vector2(0, 0) * scale, 0, Types.Vector2(1, 1) * scale),
                           Mesh=Types.Mesh(Types.MeshCircle, Color2))

        self.ChildObjects = (CObj1,)
        self.MaxScale = [self.transform.scale, CObj1.transform.scale]
        ColdDown_thread = threading.Thread(target=Types.BlowUp, args=(self,))
        ColdDown_thread.start()

    def Do(self,window = None):
        self.ChildObjects[0].transform.scale = self.MaxScale[1] * (self.transform.scale/self.MaxScale[0])
        if(self.Time <= 0):
            window.DeleteObject(self)


