from cmu_112_graphics import *
from classdec import *
from bullet import *
from helper import *

def appStarted(app):
    app.timerDelay=10
    #tentative, test only!!!!
    app.character=Player(10,"Yuyuko",app.width/2,app.height-10,5,1,1)
    app.isFocus=False
    testBullet(app.width/2,10,2,90,5,114514,1919810)
    
def redrawAll(app,canvas):
    canvas.create_oval(app.character.x-1.5*app.character.radius,app.character.y-1.5*app.character.radius,
    app.character.x+1.5*app.character.radius,app.character.y+1.5*app.character.radius,fill="white")
    canvas.create_text(300,50,font="Arial 26", text=app.character.health)
    for bullet in bulletList:
        canvas.create_oval(bullet.x-1.5*bullet.radius,bullet.y-1.5*bullet.radius,
        bullet.x+1.5*bullet.radius,bullet.y+1.5*bullet.radius,fill="yellow")

def keyPressed(app,event):
    if event.key=="z":
        app.isFocus=not app.isFocus
    if event.key=="Up" and app.character.y>=10:
        if app.isFocus:
            app.character.moveY(-1*app.character.speed/5)
        else:
            app.character.moveY(-1*app.character.speed)
    if event.key=="Down" and app.character.y<=app.height-10:
        if app.isFocus:
            app.character.moveY(app.character.speed/5)
        else:
            app.character.moveY(app.character.speed)
    if event.key=="Left" and app.character.x>=10:
        if app.isFocus:
            app.character.moveX(-1*app.character.speed/5)
        else:
            app.character.moveX(-1*app.character.speed)
    if event.key=="Right" and app.character.x<=app.width-10:
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
    for bullet in bulletList:
        dx,dy=polar2cart(bullet.direction,bullet.speed)
        bullet.x+=dx
        bullet.y+=dy
        if checkCollision(app.character,bullet):
            print("Collision Detected")
    clean(app) 

runApp(height=600,width=600)
    
