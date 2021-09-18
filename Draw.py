import pygame
import Types
import copy
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
    pygame.draw.polygon(Surface, color, Rect)
    pygame.draw.aalines(Surface, color,True, Rect)
def DrawCircle(Surface,Transform,Mesh,color):
    pygame.draw.circle(Surface,color,Transform,Mesh)

def DrawObjects(Surface,GameObjects):
    for gameObject in GameObjects:
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



