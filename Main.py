import pygame

import Window
from GameObjects import GameObject
import GameObjects
import Types
from Types import *
import Draw
import  Controll

NewGame = Window.window(600, 600)
obj = GameObjects.Tank(scale=Vector2(2,2), tag= "Hero")
NewGame.AddObject(obj)

TestBot = GameObjects.Tank(scale=Vector2(2,2), Color2 = (255,0,0),Ai = obj, speed= 0.003, AttackDistance=300, ReloadSpeed= 3)
TestBot.transform.position = Vector2(100,100)
NewGame.AddObject(TestBot)

while(True):
    NewGame.Update()
    Controll.AllControll(obj,NewGame)
    NewGame.ObjectsDo()



