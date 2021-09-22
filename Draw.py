import pygame
import Types
import copy
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (125, 125, 125)
LIGHT_BLUE = (64, 128, 255)
GREEN = (0, 200, 64)
YELLOW = (225, 225, 0)
PINK = (230, 50, 230)
RED = (255,0,0)
BLUE = (0,0,255)

def Draw(Surface,pos,Mesh,color,child = Types.Vector2(0,0)):
    Rect = []
    for x in range(0, int(len(Mesh)/2)):
        d = x*2
        Rect += [[(Mesh[d] + pos.ToArray()[0]),(Mesh[d+1] + pos.ToArray()[1])]]
    #wwpygame.draw.polygon(Surface, color, Rect)
    #pygame.draw.aalines(Surface, color,True, Rect)
    #OpenGl
    glLoadIdentity()
    glColor3f(color[0]/255, color[1]/255, color[2]/255)
    glBegin(GL_POLYGON)  # start drawing a rectangle
    glVertex2f(Rect[0][0], Rect[0][1])  # bottom left point
    glVertex2f(Rect[1][0], Rect[1][1])  # bottom right point
    glVertex2f(Rect[2][0], Rect[2][1])  # top right point
    glVertex2f(Rect[3][0], Rect[3][1])  # top left point
    glEnd()


def DrawCircle(Surface,Transform,Mesh,color):
    #pygame.draw.circle(Surface,color,Transform,Mesh)
    glLoadIdentity()
    glColor3f(color[0] / 255, color[1] / 255, color[2] / 255)
    glBegin(GL_POLYGON)
    for i in range(100):
        cosine = Mesh * math.cos(i * 2 * math.pi / 32) + Transform[0]
        sine = Mesh * math.sin(i * 2 * math.pi / 32) + Transform[1]
        glVertex2f(cosine, sine)
    glEnd()

def DrawObjects(Window,GameObjects):
    Surface = Window.Surfuse
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    for gameObject in GameObjects:
        if(gameObject.transform.position.x < 0 or gameObject.transform.position.y < 0 or gameObject.transform.position.y > Window.BorderY or
                gameObject.transform.position.x > Window.BorderX):
            continue
        if (type(gameObject.mesh.vertexes) == float):
            DrawCircle(Surface,gameObject.transform.position.ToArray() , gameObject.mesh.vertexes * gameObject.transform.scale.x,gameObject.mesh.color)
        else:
            me = Types.Vector2.LocalToGloabl(gameObject.mesh, gameObject)
            Draw(Surface, gameObject.transform.position, me, gameObject.mesh.color)

        if(gameObject.ChildObjects != None):
            for x in gameObject.ChildObjects:
                if(type(x.mesh.vertexes) == float):
                    DrawCircle(Surface,x.transform.GlobalPos(gameObject).ToArray(), x.mesh.vertexes*x.transform.scale.x, x.mesh.color)
                    continue

#####################################
                cop = copy.deepcopy(x)
                if(x.Tag != "Gun"):
                    cop.transform.rotation += gameObject.transform.rotation
                Pt = Types.Vector2.LocalToGloabl(cop.mesh, cop)
                Draw(Surface,cop.transform.GlobalPos(gameObject),Pt,cop.mesh.color)



