from classdec import *
from cmu_112_graphics import *
from helper import *

#test function for bullet
def testBullet(x,y,speed,direction,radius,damage,lifetime,bulletList):
    bulletList.append(bullet(x,y,speed,direction,radius,damage,lifetime))

def checkCollision(character,bullet,bulletList):
    if distance(character.x,character.y,bullet.x,bullet.y)<=character.radius+bullet.radius:
        bulletList.remove(bullet)
        character.health-=bullet.damage
        return True
    return False

def checkEnemyCollision(enemy,pbullet,playerBulletList):
    if distance(enemy.x,enemy.y,pbullet.x,pbullet.y)<=enemy.radius+pbullet.radius:
        playerBulletList.remove(pbullet)
        enemy.health-=pbullet.damage
        return True
    return False

def checkGraze(character,bullet):
    if character.radius+bullet.radius<distance(character.x,character.y,bullet.x,bullet.y)<=character.radius+bullet.radius+10:
        return True
    return False

def clean(app,bulletList,playerBulletList):
    for bullet in bulletList:
        if bullet.x>app.width or bullet.x<0 or bullet.y<0 or bullet.y>app.height:
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

def pattern1(x,y,density,size,speed,damage,lifetime,offset,bulletList):
    count=180//density
    for i in range(1,count):
        bulletList.append(bullet(x,y,speed,i*density+offset,size,damage,lifetime))

