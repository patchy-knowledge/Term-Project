from classdec import *
from cmu_112_graphics import *
from helper import *

bulletList=[]
playerBulletList=[]

#test function for bullet
def testBullet(x,y,speed,direction,radius,damage,lifetime):
    bulletList.append(bullet(x,y,speed,direction,radius,damage,lifetime))

def checkCollision(character,bullet):
    if distance(character.x,character.y,bullet.x,bullet.y)<=character.radius+bullet.radius:
        bulletList.remove(bullet)
        character.health-=bullet.damage
        return True
    return False

def checkGraze(character,bullet):
    if character.radius+bullet.radius<distance(character.x,character.y,bullet.x,bullet.y)<=character.radius+bullet.radius+10:
        return True
    return False

def clean(app):
    for bullet in bulletList:
        if bullet.x>app.width or bullet.x<0 or bullet.y<0 or bullet.y>app.height:
            bulletList.remove(bullet)

def pattern1(x,y,density,size,speed,damage,lifetime,offset):
    count=180//density
    for i in range(1,count):
        bulletList.append(bullet(x,y,speed,i*density+offset,size,damage,lifetime))

