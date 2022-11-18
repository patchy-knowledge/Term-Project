from classdec import *
from cmu_112_graphics import *
from helper import *

bulletList=[]

def testBullet(x,y,speed,direction,radius,damage,lifetime):
    bulletList.append(bullet(x,y,speed,direction,radius,damage,lifetime))

def checkCollision(character):
    for bullet in bulletList:
        if distance(character.x,character.y,bullet.x,bullet.y)<=character.radius+bullet.radius:
            return True
    return False

