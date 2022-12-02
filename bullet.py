from classdec import *
from cmu_112_graphics import *
from helper import *
import random

#test function for bullet
def testBullet(x,y,speed,direction,radius,damage,lifetime,app):
    app.bulletList.append(bullet(x,y,speed,direction,radius,damage,lifetime))

def checkCollision(character,bullet,app):
    if distance(character.x,character.y,bullet.x,bullet.y)<=character.radius+bullet.radius:
        app.bulletList.remove(bullet)
        return True
    return False

def checkEnemyCollision(enemy,pbullet,playerBulletList,app):
    if distance(enemy.x,enemy.y,pbullet.x,pbullet.y)<=enemy.radius+pbullet.radius:
        playerBulletList.remove(pbullet)
        enemy.health-=pbullet.damage
        app.score+=10
        return True
    return False

def checkGraze(character,bullet):
    if character.radius+bullet.radius<distance(character.x,character.y,bullet.x,bullet.y)<=character.radius+bullet.radius+25:
        return True
    return False

def bomb(app):
    if app.character.bomb>0:
        app.character.bomb-=1
        app.character.timer=2000
        app.character.isInvincible=True
        app.newBulletList=[]
        playerPattern1(app.character.x,app.character.y,3,5,3,150,114,-1.5,app)
        playerPattern1(app.character.x,app.character.y,3,5,5,150,114,0,app)
        for bullet in app.bulletList:
            if distance(bullet.x,bullet.y,app.character.x,app.character.y)>250:
                app.newBulletList.append(bullet)
        app.bulletList=app.newBulletList


def freeze(app,x,y,r):
    for bullet in app.bulletList:
        if distance(bullet.x,bullet.y,x,y)<r and not bullet.freeze:
            bullet.freeze=True
            bullet.timer=1000

def clean(app,bulletList,playerBulletList):
    for bullet in bulletList:
        if bullet.x>600-bullet.radius or bullet.x<0 or bullet.y<0 or bullet.y>600-bullet.radius:
            bulletList.remove(bullet)
    for playerBullet in playerBulletList:
        if playerBullet.x>600 or playerBullet.x<0 or playerBullet.y<0 or playerBullet.y>600:
            playerBulletList.remove(playerBullet)

#test only
def firePlayerBullet(track,app):
    if app.timePassed%30==0:
        for i in range(math.floor(app.character.power)):
            if i==0:
                app.playerBulletList.append(playerShot(app.character.x,app.character.y,10,-90,8,100*app.character.power,114514,track))
            else:
                app.playerBulletList.append(playerShot(app.character.x+i*10,app.character.y,10,-90,8,100*app.character.power,114514,track))
                app.playerBulletList.append(playerShot(app.character.x-i*10,app.character.y,10,-90,8,100*app.character.power,114514,track))

def pattern1(x,y,density,size,speed,damage,lifetime,offset,app):
    count=180//density
    for i in range(1,count):
        app.bulletList.append(bullet(x,y,speed,i*density+offset,size,damage,lifetime))

def playerPattern1(x,y,density,size,speed,damage,lifetime,offset,app):
    count=180//density
    for i in range(1,count):
        app.playerBulletList.append(playerShot(x,y,speed,180+i*density+offset,size,damage,lifetime,False))

def pattern2(app,xyList,speed,direction,size,damage,lifetime,count,timeLapse):
    app.pattern2count=count
    if app.timePassed>app.pattern2start+timeLapse*app.pattern2gencount:
        for x,y in xyList:
            app.bulletList.append(bullet(x,y,speed,direction,size,damage,lifetime))
            app.pattern2gencount+=1
        if app.pattern2gencount>app.pattern2count-len(xyList):
            app.pattern2gen=False

def randomBullet(app,speed,size,damage,lifetime):
    x=random.randint(10,590)
    y=random.randint(10,300)
    dx=app.character.x-x
    dy=app.character.y-y
    #minimum generation distance from player is 150
    while(distance(x,y,app.character.x,app.character.y)<150):
        x=random.randint(10,590)
        y=random.randint(10,300)
        dx=app.character.x-x
        dy=app.character.y-y
    if dx==0:
        direction=-90
    else: 
        direction=180/math.pi*math.atan(dy/dx)
    if direction<0:
        direction+=180
    app.bulletList.append(bullet(x,y,speed,direction,size,damage,lifetime))

def bossBullet(app,speed,size,damage,lifetime):
    dx=app.character.x-app.enemy.x
    dy=app.character.y-app.enemy.y
    if dx==0:
        direction=-90
    else:
        direction=180/math.pi*math.atan(dy/dx)
    if direction<0:
        direction+=180
    app.bulletList.append(bullet(app.enemy.x,app.enemy.y,speed,direction,size,damage,lifetime))

