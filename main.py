from cmu_112_graphics import *
from classdec import *
from bullet import *
from helper import *
from terrain import *

def appStarted(app):
    app.timerDelay=10
    app.bulletList=[]
    app.playerBulletList=[]
    app.enemyList=[]
    app.powerupList=[]
    app.terrainList=[]
    #tentative, test only!!!!
    app.character=Player(10,"Yuyuko",app.width/2,app.height-10,5,1,1)
    app.isFocus=False
    app.enemy=Enemy(5,"Reimu",114514,app.width/2,10,30,1)
    testBullet(app.width/2,10,2,90,5,1,1919810,app.bulletList)
    testCircularTerrain(300,300,50,app.terrainList)

def drawCharacters(app,canvas):
    canvas.create_oval(app.character.x-app.character.radius,app.character.y-app.character.radius,
    app.character.x+app.character.radius,app.character.y+app.character.radius,fill="white")
    canvas.create_oval(app.enemy.x-app.enemy.radius,app.enemy.y-app.enemy.radius,
    app.enemy.x+app.enemy.radius,app.enemy.y+app.enemy.radius,fill="magenta")

def redrawAll(app,canvas):
    drawCharacters(app,canvas)
    canvas.create_text(300,50,font="Arial 26", text=app.enemy.health)
    drawTerrain(app,canvas)
    drawBullets(app,canvas)

def keyPressed(app,event):
    if event.key=="Space":
        app.character.isFiring=not app.character.isFiring
    if event.key=="z":
        app.isFocus=not app.isFocus
    if event.key=="Up" and app.character.y>=10 and checkTerrain(app.character,app.terrainList) not in (4,5,7):
        if app.isFocus:
            app.character.moveY(-1*app.character.speed/5)
        else:
            app.character.moveY(-1*app.character.speed)
    if event.key=="Down" and app.character.y<=app.height-10 and checkTerrain(app.character,app.terrainList) not in (3,6,8):
        if app.isFocus:
            app.character.moveY(app.character.speed/5)
        else:
            app.character.moveY(app.character.speed)
    if event.key=="Left" and app.character.x>=10 and checkTerrain(app.character,app.terrainList) not in (2,5,6):
        if app.isFocus:
            app.character.moveX(-1*app.character.speed/5)
        else:
            app.character.moveX(-1*app.character.speed)
    if event.key=="Right" and app.character.x<=app.width-10 and checkTerrain(app.character,app.terrainList) not in (1,7,8):
        if app.isFocus:
            app.character.moveX(app.character.speed/5)
        else:
            app.character.moveX(app.character.speed)
    #test bullet pattern
    if event.key=="1":
        pattern1(300,50,10,8,2,1,100,0,app.bulletList)
        pattern1(100,50,10,8,2,1,100,5,app.bulletList)
        pattern1(500,50,10,8,2,1,100,5,app.bulletList)
        
def timerFired(app):
    if app.character.isFiring:
        firePlayerBullet(app.character,True,app.playerBulletList)
    for bullet in app.bulletList:
        if not bullet.freeze:
            dx,dy=polar2cart(bullet.direction,bullet.speed)
            bullet.x+=dx
            bullet.y+=dy
        if checkCollision(app.character,bullet,app.bulletList):
            print("Collision Detected")
        if checkGraze(app.character,bullet) and not bullet.grazed:
            print("Graze Detected")
            bullet.grazed=True
    for playerBullet in app.playerBulletList:
        checkEnemyCollision(app.enemy,playerBullet,app.playerBulletList)
        if playerBullet.tracking:
            dx1=app.enemy.x-playerBullet.x
            dy1=app.enemy.y-playerBullet.y
            theta=cart2polar(dx1,dy1)[0]
            if theta<0:
                playerBullet.direction=theta
            else:
                playerBullet.direction=180+theta
        dx,dy=polar2cart(playerBullet.direction,playerBullet.speed)
        playerBullet.x+=dx
        playerBullet.y+=dy

    clean(app,app.bulletList,app.playerBulletList) 

runApp(height=600,width=600)
    
