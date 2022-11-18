from cmu_112_graphics import *
from classdec import *
from bullet import *
from helper import *

def appStarted(app):
    #tentative, test only!!!!
    app.character=Player(10,"Yuyuko",app.width/2,app.height-10,10,1,1)
    app.isFocus=False
    testBullet(app.width/2,10,10,90,5,114514,1919810)
    
def redrawAll(app,canvas):
    canvas.create_oval(app.character.x-0.5*app.character.radius,app.character.y-0.5*app.character.radius,
    app.character.x+0.5*app.character.radius,app.character.y+0.5*app.character.radius,fill="white")
    for bullet in bulletList:
        canvas.create_oval(bullet.x-0.5*bullet.radius,bullet.y-0.5*bullet.radius,
        bullet.x+0.5*bullet.radius,bullet.y+0.5*bullet.radius,fill="yellow")

def keyPressed(app,event):
    if event.key=="z":
        app.isFocus=not app.isFocus
    if event.key=="Up":
        if app.isFocus:
            app.character.moveY(-1*app.character.speed/5)
        else:
            app.character.moveY(-1*app.character.speed)
    if event.key=="Down":
        if app.isFocus:
            app.character.moveY(app.character.speed/5)
        else:
            app.character.moveY(app.character.speed)
    if event.key=="Left":
        if app.isFocus:
            app.character.moveX(-1*app.character.speed/5)
        else:
            app.character.moveX(-1*app.character.speed)
    if event.key=="Right":
        if app.isFocus:
            app.character.moveX(app.character.speed/5)
        else:
            app.character.moveX(app.character.speed)

def timerFired(app):
    for bullet in bulletList:
        dx,dy=polar2cart(bullet.direction,bullet.speed)
        bullet.x+=dx
        bullet.y+=dy

    if checkCollision(app.character):
        print("collision detected")

runApp(height=600,width=600)
    
