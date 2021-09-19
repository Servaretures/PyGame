import pygame
import Draw
import GameObjects
import Types
import  time
import  random
class window:

    def __init__(self, borderX = 600, borderY = 600, fpsRate = 60, DeleteBorder = 10,EnemySpawnTime = 5):
        pygame.init()
        pygame.font.init()
        self.DeleteBorder = DeleteBorder
        self.Surfuse = pygame.display.set_mode((borderX, borderY))
        self.clock = pygame.time.Clock()
        pygame.display.update()
        self.FpsRate = fpsRate
        self.BorderX = borderX
        self.BorderY = borderY
        self.GameObjects = []
        self.Score = 0
        self.End = False
        self.EnemySpawnTime = EnemySpawnTime
    def ShowScore(self):
        f = pygame.font.Font(None,36)
        text = f.render('Score:' + str(self.Score), True,
                  (255, 0, 0))
        self.Surfuse.blit(text, (0, 0))
    def Update(self):
        pygame.event.get()
        self.Surfuse.fill(Draw.WHITE)
        Draw.DrawObjects(self,self.GameObjects)
        self.ShowScore()
        pygame.display.update()
        print(self.clock.get_fps())
        self.clock.tick(self.FpsRate)
    def AddObject(self,GameObject):
        self.GameObjects.append(GameObject)
    def DeleteObject(self, GameObject):
        self.GameObjects.remove(GameObject)
    def ObjectsDo(self):
        for obj in self.GameObjects:
            obj.Do(self)
            pos = obj.transform.position
            if((pos.x < -self.DeleteBorder or pos.x > self.BorderX + self.DeleteBorder or
            pos.y < -self.DeleteBorder or pos.y > self.BorderY + self.DeleteBorder) and obj.Tag != "Hero"):
                self.DeleteObject(obj)
    def UpdateCollider(self):
        for x in self.GameObjects:
            for y in self.GameObjects:
                if(((y.Tag == "EnBullet" and x.Tag =="Hero") or (y.Tag == "Bullet" and x.Tag =="Tank")) and x.collider.isCollide(y.collider)):
                    Blow = GameObjects.Blow(scale=Types.Vector2(10, 10))
                    Blow.transform.position = x.transform.position
                    self.AddObject(Blow)
                    self.DeleteObject(x)
                    self.DeleteObject(y)
                    if(x.Tag == "Tank" or y.Tag == "Tank"):
                        self.Score += 1
                    if(x.Tag == "Hero" or y.Tag == "Hero"):
                        self.End = True

    def EnemySpawn(self,Hero,Destory):
        c = 1
        x = self.BorderX + self.DeleteBorder
        y = self.BorderY + self.DeleteBorder
        _xy = -self.DeleteBorder
        while True:
            #or c == 5
            if(Destory() or c == 5):
                break
            print(c)
            for t in range(0,c):
                TestBot = GameObjects.Tank(scale=Types.Vector2(2, 2), Color2=(255, 0, 0), Ai=Hero, speed=0.003,AttackDistance=300,ReloadSpeed=3)
                TestBot.transform.position = Types.Vector2(x,random.randint(_xy,y) )
                self.AddObject(TestBot)
                TestBot = GameObjects.Tank(scale=Types.Vector2(2, 2), Color2=(255, 0, 0), Ai=Hero, speed=0.003,AttackDistance=300, ReloadSpeed=3)
                TestBot.transform.position = Types.Vector2(random.randint(_xy,x),y)
                self.AddObject(TestBot)
                TestBot = GameObjects.Tank(scale=Types.Vector2(2, 2), Color2=(255, 0, 0), Ai=Hero, speed=0.003,AttackDistance=300, ReloadSpeed=3)
                TestBot.transform.position = Types.Vector2(_xy,random.randint(_xy,y))
                self.AddObject(TestBot)
                TestBot = GameObjects.Tank(scale=Types.Vector2(2, 2), Color2=(255, 0, 0), Ai=Hero, speed=0.003,AttackDistance=300, ReloadSpeed=3)
                TestBot.transform.position = Types.Vector2(random.randint(_xy,x),_xy)
                self.AddObject(TestBot)
            c+=1
            time.sleep(self.EnemySpawnTime)
