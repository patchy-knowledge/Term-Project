from classdec import *
from cmu_112_graphics import *
from helper import *
import time

#test function for bullet
def testBullet(x,y,speed,direction,radius,damage,lifetime,bulletList):
    bulletList.append(bullet(x,y,speed,direction,radius,damage,lifetime))

def checkCollision(character,bullet,bulletList):
    if distance(character.x,character.y,bullet.x,bullet.y)<=character.radius+bullet.radius:
        bulletList.remove(bullet)
        character.health-=bullet.damage
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

def clean(app,bulletList,playerBulletList):
    for bullet in bulletList:
        if bullet.x>600-bullet.radius or bullet.x<0 or bullet.y<0 or bullet.y>600-bullet.radius:
            bulletList.remove(bullet)
    for playerBullet in playerBulletList:
        if playerBullet.x>app.width or playerBullet.x<0 or playerBullet.y<0 or playerBullet.y>app.height:
            playerBulletList.remove(playerBullet)

#test only
def firePlayerBullet(character,track,playerBulletList):
    for i in range(character.power):
        if i==0:
            playerBulletList.append(playerShot(character.x,character.y,10,-90,3,50,114514,track))
        else:
            playerBulletList.append(playerShot(character.x+i*10,character.y,10,-90,3,50,114514,track))
            playerBulletList.append(playerShot(character.x-i*10,character.y,10,-90,3,50,114514,track))

def pattern1(x,y,density,size,speed,damage,lifetime,offset,app):
    count=180//density
    for i in range(1,count):
        app.bulletList.append(bullet(x,y,speed,i*density+offset,size,damage,lifetime))

def pattern2(app,x,y,speed,direction,size,damage,lifetime,count,timeLapse):
    app.pattern2count=count
    if app.timePassed>app.pattern2start+timeLapse*app.pattern2gencount:
        app.bulletList.append(bullet(x,y,speed,direction,size,damage,lifetime))
        app.pattern2gencount+=1
        if app.pattern2gencount>app.pattern2count-1:
            app.pattern2gen=False

def drawBullets(app,canvas):
    for bullet in app.bulletList:
        canvas.create_oval(bullet.x-bullet.radius,bullet.y-bullet.radius,
        bullet.x+bullet.radius,bullet.y+bullet.radius,fill="yellow")
    for playerBullet in app.playerBulletList:
        canvas.create_oval(playerBullet.x-playerBullet.radius,playerBullet.y-playerBullet.radius,
        playerBullet.x+playerBullet.radius,playerBullet.y+playerBullet.radius,fill="red")
