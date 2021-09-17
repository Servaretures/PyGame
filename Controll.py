import math
import threading
import GameObjects
import pygame
import Types

def KeyboardControl(gameObject):
    k = pygame.key.get_pressed()
    k = pygame.key.get_pressed()
    if (k[pygame.K_w]):
        gameObject.transform.position = gameObject.transform.position + Types.Vector2.Forward(
            gameObject.transform) * Types.Vector2(gameObject.speed, gameObject.speed)
    elif (k[pygame.K_s]):
        gameObject.transform.position = gameObject.transform.position - Types.Vector2.Forward(
            gameObject.transform) * Types.Vector2(gameObject.speed, gameObject.speed)
    if (k[pygame.K_a]):
        gameObject.transform.rotation -= gameObject.RotSpeed
    elif (k[pygame.K_d]):
        gameObject.transform.rotation += gameObject.RotSpeed

def KeyboardControll(gameObject, speed,RotSpeed):
    k = pygame.key.get_pressed()
    if(k[pygame.K_w]):
        gameObject.transform.position = (gameObject.transform.position + Types.Vector2.Forward(gameObject.transform))* Types.Vector2(speed,speed)
    elif(k[pygame.K_s]):
        gameObject.transform.position = (gameObject.transform.position - Types.Vector2.Forward(gameObject.transform))* Types.Vector2(speed,speed)
    if(k[pygame.K_a]):
        gameObject.transform.rotation -= RotSpeed
    if (k[pygame.K_d]):
        gameObject.transform.rotation += RotSpeed

def MouseControll(obj):
    pos = obj.ChildObjects[obj.Tower].transform.position + obj.transform.position
    Mouse = pygame.mouse.get_pos()
    Vector = Types.Vector2(Mouse[0] - pos.x,Mouse[1]-pos.y)
    obj.ChildObjects[obj.Tower].transform.rotation = math.atan2(Vector.y,Vector.x)
def ShootControll(obj, window):
    if(pygame.mouse.get_pressed()[0] and obj.IsShootReady):
        bul = GameObjects.Bullet()
        bul.transform.position = obj.ChildObjects[obj.Tower].transform.GlobalPos(obj)
        bul.transform.rotation = obj.ChildObjects[obj.Tower].transform.rotation
        bul.transform.position += Types.Vector2.Forward(bul.transform) * Types.Vector2(25,25)
        window.AddObject(bul)
        ColdDown_thread = threading.Thread(target=Types.ShootColdDown, args=(obj.ReloadSpeed,obj))
        ColdDown_thread.start()
        pass
def AllControll(obj,window):
    KeyboardControl(obj)
    MouseControll(obj)
    ShootControll(obj,window)

