import pygame
from pygame.locals import *
import sys
import Window
from GameObjects import GameObject
import GameObjects
import Types
from Types import *
import Draw
import  Controll
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
    NewGame = Window.window(800, 800)


    obj = GameObjects.Tank(scale=Vector2(2, 2), tag="Hero")
    NewGame.AddObject(obj)

    TestBot = GameObjects.Tank(scale=Vector2(2, 2), Color2=(255, 0, 0), Ai=obj, speed=0.003, AttackDistance=300,
                               ReloadSpeed=3)
    TestBot.transform.position = Vector2(100, 100)
    NewGame.AddObject(TestBot)

    # TestBlow = GameObjects.Blow(scale=Vector2(10,10))
    # NewGame.AddObject(TestBlow)
    ####Test
    ####
    while (not NewGame.End):
        NewGame.Update()
        Controll.AllControll(obj, NewGame)
        NewGame.ObjectsDo()
        NewGame.UpdateCollider()
        if(GetAnswer()):
            break
    return NewGame
while(True):
    End = Game()

    pygame.draw.polygon(End.Surfuse,(255,255,255), ((End.BorderX/2-100,End.BorderY/2-50),(End.BorderX/2-100,End.BorderY/2+50),
                                              (End.BorderX/2+100,End.BorderY/2+50),(End.BorderX/2+100,End.BorderY/2-50)))
    pygame.draw.aalines(End.Surfuse, (0, 0, 0),True,
                        ((End.BorderX / 2 - 100, End.BorderY / 2 - 50), (End.BorderX / 2 - 100, End.BorderY / 2 + 50),
                         (End.BorderX / 2 + 100, End.BorderY / 2 + 50), (End.BorderX / 2 + 100, End.BorderY / 2 - 50)))
    f = pygame.font.Font(None, 48)
    text = f.render('Game Over', True,
                    (255, 0, 0))
    End.Surfuse.blit(text, (End.BorderX/2-89,End.BorderY/2-40))

    f = pygame.font.Font(None, 28)
    text = f.render('Press R to restart', True,
                    (255, 0, 0))
    End.Surfuse.blit(text, (End.BorderX / 2-80, End.BorderY / 2+10))
    pygame.display.update()
    if(WaintAnswer()):
        break





