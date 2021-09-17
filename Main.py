import pygame

import Window
from GameObjects import GameObject
import GameObjects
import Types
from Types import *
import Draw
import  Controll

NewGame = Window.window(600, 600)
#trans = Types.Transform(Vector2(300,300),0,Vector2(20,20))
#col = Types.RectCollider(Vector2(-20,-20), Vector2(20,20))
#mesh = Types.Mesh(Types.MeshBox, Draw.RED)
#obj = GameObject(trans,col,mesh)
obj = GameObjects.Tank(scale=Vector2(2,2))
NewGame.AddObject(obj)


while(True):
    NewGame.Update()
    Controll.AllControll(obj,NewGame)
    NewGame.ObjectsDo()



