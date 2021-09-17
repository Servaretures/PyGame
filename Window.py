import pygame
import Draw
class window:

    def __init__(self, borderX = 600, borderY = 600, fpsRate = 60, DeleteBorder = 10):
        pygame.init()
        self.DeleteBorder = DeleteBorder
        self.Surfuse = pygame.display.set_mode((borderX, borderY))
        self.clock = pygame.time.Clock()
        pygame.display.update()
        self.FpsRate = fpsRate
        self.BorderX = borderX
        self.BorderY = borderY
        self.GameObjects = []
    def Update(self):
        pygame.event.get()
        self.Surfuse.fill(Draw.WHITE)
        Draw.DrawObjects(self.Surfuse,self.GameObjects)
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
            if(pos.x < -self.DeleteBorder or pos.x > self.BorderX + self.DeleteBorder or
            pos.y < -self.DeleteBorder or pos.y > self.BorderY + self.DeleteBorder):
                self.DeleteObject(obj)