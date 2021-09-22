import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys
import Window
from GameObjects import GameObject
import GameObjects
import Types
from Types import *
import Draw
import  Controll
import threading
pygame.font.init()
def GetAnswer():
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
        if event.type == KEYDOWN and event.key == K_r:
            return True
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            sys.exit()
def WaintAnswer():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            if event.type == KEYDOWN and event.key == K_r:
                return False
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                sys.exit()

def Game():

    NewGame = Window.window(1000, 1000)
    pygame.display.set_caption('Тahk')
    Icon = pygame.image.load('ico.png')
    pygame.display.set_icon(Icon)

    obj = GameObjects.Tank(scale=Vector2(2, 2), tag="Hero",ReloadSpeed=0.2)
    obj.transform.position = Vector2(NewGame.BorderX/2, NewGame.BorderY/2)
    NewGame.AddObject(obj)
    #TestBot = GameObjects.Tank(scale=Vector2(2, 2), Color2=(255, 0, 0), Ai=obj, speed=0.003, AttackDistance=300,ReloadSpeed=3)
    #TestBot.transform.position = Vector2(NewGame.BorderX/2, NewGame.BorderY/2)
    #NewGame.AddObject(TestBot)
    Destroy = False
    ColdDown_thread = threading.Thread(target=NewGame.EnemySpawn, args=(obj,lambda :Destroy, ),daemon=True)
    ColdDown_thread.start()
    c = 0
    while (not NewGame.End):

        NewGame.Update()
        Controll.AllControll(obj, NewGame)
        NewGame.ObjectsDo()
        if(c == 3):
            #NewGame.UpdateCollider()
            c = 0
        c+=1
        if(GetAnswer() or NewGame.Score == 40):
            break
    Destroy = True
    return NewGame
while(True):
    End = Game()
    str = "Game Over" if End.Score < 40 else "Win"

    pygame.draw.polygon(End.Surfuse,(255,255,255), ((End.BorderX/2-100,End.BorderY/2-50),(End.BorderX/2-100,End.BorderY/2+50),
                                              (End.BorderX/2+100,End.BorderY/2+50),(End.BorderX/2+100,End.BorderY/2-50)))
    pygame.draw.aalines(End.Surfuse, (0, 0, 0),True,
                        ((End.BorderX / 2 - 100, End.BorderY / 2 - 50), (End.BorderX / 2 - 100, End.BorderY / 2 + 50),
                         (End.BorderX / 2 + 100, End.BorderY / 2 + 50), (End.BorderX / 2 + 100, End.BorderY / 2 - 50)))
    f = pygame.font.Font(None, 48)
    text = f.render(str, True,
                    (255, 0, 0))
    End.Surfuse.blit(text, (End.BorderX/2-89,End.BorderY/2-40))

    f = pygame.font.Font(None, 28)
    text = f.render('Press R to restart', True,
                    (255, 0, 0))
    End.Surfuse.blit(text, (End.BorderX / 2-80, End.BorderY / 2+10))
    pygame.display.flip()
    if(WaintAnswer()):
        break





