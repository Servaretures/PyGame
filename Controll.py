import math
import threading
import GameObjects
import pygame
import Types
import time

def KeyboardControl(gameObject, window):
    k = pygame.key.get_pressed()
    w = gameObject.transform.position + Types.Vector2.Forward(
        gameObject.transform) * Types.Vector2(gameObject.speed, gameObject.speed)
    s = gameObject.transform.position - Types.Vector2.Forward(
            gameObject.transform) * Types.Vector2(gameObject.speed, gameObject.speed)
    if (k[pygame.K_w] and (w.x > 0 and w.y > 0 and w.x < window.BorderX and w.y < window.BorderY)):
        gameObject.transform.position = w
    elif (k[pygame.K_s] and (s.x > 0 and s.y > 0 and s.x < window.BorderX and s.y < window.BorderY)):
        #time.sleep(100000)
        gameObject.transform.position = s
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
    obj.ChildObjects[obj.Tower].transform.rotation = Types.Vector2.LookAt(pos,Types.Vector2(Mouse[0], Mouse[1]))
def ShootControll(obj, window):
    if(pygame.mouse.get_pressed()[0] and obj.IsShootReady):
        bul = GameObjects.Bullet()
        bul.transform.position = obj.ChildObjects[obj.Tower].transform.GlobalPos(obj)
        bul.transform.rotation = obj.ChildObjects[obj.Tower].transform.rotation
        bul.transform.position += Types.Vector2.Forward(bul.transform) * Types.Vector2(25,25)
        bul.mesh.color = (0,255,0)
        window.AddObject(bul)
        ColdDown_thread = threading.Thread(target=Types.ShootColdDown, args=(obj.ReloadSpeed,obj),daemon=True)
        ColdDown_thread.start()
        pass
def AllControll(obj,window):
    KeyboardControl(obj,window)
    MouseControll(obj)
    ShootControll(obj,window)
def AiControllTank(obj,Target):
    if(Types.Vector2.Distance(Target,obj.transform.position) > 100):
        To = Target - obj.transform.position
        obj.transform.position += To * Types.Vector2(obj.speed)
        obj.transform.rotation = Types.Vector2.LookAt(obj.transform.position,Target)
