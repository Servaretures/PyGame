import pygame
import Draw
import GameObjects
import Types
class window:

    def __init__(self, borderX = 600, borderY = 600, fpsRate = 60, DeleteBorder = 10):
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
    def ShowScore(self):
        f = pygame.font.Font(None,36)
        text = f.render('Score:' + str(self.Score), True,
                  (255, 0, 0))
        self.Surfuse.blit(text, (0, 0))
    def Update(self):
        pygame.event.get()
        self.Surfuse.fill(Draw.WHITE)
        Draw.DrawObjects(self.Surfuse,self.GameObjects)
        self.ShowScore()
        pygame.display.update()
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
                if(y != x and x.collider != None and y.collider != None and x.collider.isCollide(y.collider) and (x.Tag == "Bullet" or y.Tag == "Bullet")):
                    Blow = GameObjects.Blow(scale=Types.Vector2(10, 10))
                    Blow.transform.position = x.transform.position
                    self.AddObject(Blow)
                    self.DeleteObject(x)
                    self.DeleteObject(y)
                    if(x.Tag == "Tank" or y.Tag == "Tank"):
                        self.Score += 1
                    if(x.Tag == "Hero" or y.Tag == "Hero"):
                        self.End = True