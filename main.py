from cmu_112_graphics import *
from classdec import *
from bullet import *
from helper import *
from terrain import *

def appStarted(app):
    app.timerDelay=10
    #tentative, test only!!!!
    app.character=Player(10,"Yuyuko",app.width/2,app.height-10,5,1,1)
    app.isFocus=False
    testBullet(app.width/2,10,2,90,5,1,1919810)
    testRectTerrain(250,250,350,350)
    
def redrawAll(app,canvas):
    canvas.create_oval(app.character.x-app.character.radius,app.character.y-app.character.radius,
    app.character.x+app.character.radius,app.character.y+app.character.radius,fill="white")
    canvas.create_text(300,50,font="Arial 26", text=app.character.health)
    for terrain in terrainList:
        if isinstance(terrain,rectTerrain):
            canvas.create_rectangle(terrain.x1,terrain.y1,terrain.x2,terrain.y2,
            fill="white",outline="black")
        elif isinstance(terrain,circularTerrain):
            canvas.create_oval(terrain.x-terrain.r,terrain.y-terrain.r,
            terrain.x+terrain.r,terrain.y+terrain.r,fill="white",outline="black")
    for bullet in bulletList:
        canvas.create_oval(bullet.x-bullet.radius,bullet.y-bullet.radius,
        bullet.x+bullet.radius,bullet.y+bullet.radius,fill="yellow")
    for playerBullet in playerBulletList:
        canvas.create_oval(playerBullet.x-playerBullet.radius,playerBullet.y-playerBullet.radius,
        playerBullet.x+playerBullet.radius,playerBullet.y+playerBullet.radius,fill="red")

def keyPressed(app,event):
    if event.key=="Space":
        app.character.isFiring=not app.character.isFiring
    if event.key=="z":
        app.isFocus=not app.isFocus
    if event.key=="Up" and app.character.y>=10 and checkTerrain(app.character)!=4:
        if app.isFocus:
            app.character.moveY(-1*app.character.speed/5)
        else:
            app.character.moveY(-1*app.character.speed)
    if event.key=="Down" and app.character.y<=app.height-10 and checkTerrain(app.character)!=3:
        if app.isFocus:
            app.character.moveY(app.character.speed/5)
        else:
            app.character.moveY(app.character.speed)
    if event.key=="Left" and app.character.x>=10 and checkTerrain(app.character)!=2:
        if app.isFocus:
            app.character.moveX(-1*app.character.speed/5)
        else:
            app.character.moveX(-1*app.character.speed)
    if event.key=="Right" and app.character.x<=app.width-10 and checkTerrain(app.character)!=1:
        if app.isFocus:
            app.character.moveX(app.character.speed/5)
        else:
            app.character.moveX(app.character.speed)
    #test bullet pattern
    if event.key=="1":
        pattern1(300,50,10,8,2,1,100,0)
        pattern1(100,50,10,8,2,1,100,5)
        pattern1(500,50,10,8,2,1,100,5)
        
def timerFired(app):
    if app.character.isFiring:
        firePlayerBullet(app.character,False)
    for bullet in bulletList:
        if not bullet.freeze:
            dx,dy=polar2cart(bullet.direction,bullet.speed)
            bullet.x+=dx
            bullet.y+=dy
        if checkCollision(app.character,bullet):
            print("Collision Detected")
        if checkGraze(app.character,bullet) and not bullet.grazed:
            print("Graze Detected")
            bullet.grazed=True
    for playerBullet in playerBulletList:
        if not playerBullet.tracking:
            dx,dy=polar2cart(playerBullet.direction,playerBullet.speed)
            playerBullet.x+=dx
            playerBullet.y+=dy

    clean(app) 

runApp(height=600,width=600)
    
