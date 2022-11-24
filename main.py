from cmu_112_graphics import *
from classdec import *
from bullet import *
from helper import *
from terrain import *
from time import *

def appStarted(app):
    app.timerDelay=10
    app.timePassed=0
    app.bulletList=[]
    app.playerBulletList=[]
    app.enemyList=[]
    app.powerupList=[]
    app.terrainList=[]
    #tentative, test only!!!!
    app.character=Player(3,"Yuyuko",app.width/2,app.height-10,5,1,1)
    app.isFocus=False
    app.enemy=Enemy(5,"Reimu",114514,app.width/2,50,5,1)
    testBullet(app.width/2,10,2,90,5,1,1919810,app.bulletList)
    testCircularTerrain(300,300,50,app.terrainList)
    app.mode="Start"
    app.cleared=True
    app.scroll=0
    app.keyHoldDict=dict()
    app.keyHoldDict["Up"]=False
    app.keyHoldDict["Down"]=False
    app.keyHoldDict["Left"]=False
    app.keyHoldDict["Right"]=False
    app.score=0
    app.pattern2gen=False
    app.characterImage=app.loadImage('Yuyuko_char.png')
    app.enemyImage=app.loadImage('Reimu_enemy.png')

def checkMovements(app):
    if app.keyHoldDict["Up"] and checkTerrain(app.character,app.terrainList) not in (4,5,7):
        if app.isFocus:
            app.character.y-=0.2*app.character.speed
        else:
            app.character.y-=app.character.speed
    if app.keyHoldDict["Down"] and checkTerrain(app.character,app.terrainList) not in (3,6,8):
        if app.isFocus:
            app.character.y+=0.2*app.character.speed
        else:
            app.character.y+=app.character.speed
    if app.keyHoldDict["Left"] and checkTerrain(app.character,app.terrainList) not in (2,5,6):
        if app.isFocus:
            app.character.x-=0.2*app.character.speed
        else:
            app.character.x-=app.character.speed
    if app.keyHoldDict["Right"] and checkTerrain(app.character,app.terrainList) not in (1,7,8):
        if app.isFocus:
            app.character.x+=0.2*app.character.speed
        else:
            app.character.x+=app.character.speed

def drawPowerups(app,canvas):
    for powerup in app.powerUpList:
        if powerup.type=="invincible":
            canvas.create_oval(powerup.x-10,powerup.y-10,powerup.x+10,powerup.y+10,fill="blue")
        elif powerup.type=="power":
            canvas.create_oval(powerup.x-10,powerup.y-10,powerup.x+10,powerup.y+10,fill="red")
        elif powerup.type=="track":
            canvas.create_oval(powerup.x-10,powerup.y-10,powerup.x+10,powerup.y+10,fill="purple")

def drawCharacters(app,canvas):
    canvas.create_image(app.character.x,app.character.y,image=ImageTk.PhotoImage(app.characterImage))
    canvas.create_oval(app.character.x-app.character.radius,app.character.y-app.character.radius,
    app.character.x+app.character.radius,app.character.y+app.character.radius,fill="white")
    canvas.create_image(app.enemy.x,app.enemy.y,image=ImageTk.PhotoImage(app.enemyImage))
    canvas.create_oval(app.enemy.x-app.enemy.radius,app.enemy.y-app.enemy.radius,
    app.enemy.x+app.enemy.radius,app.enemy.y+app.enemy.radius,fill="magenta")

def Start_redrawAll(app,canvas):
    canvas.create_text(300,300,font="Helvetica", text="Press any key to start")

def Start_keyPressed(app,event):
    app.mode="Game"

def Game_redrawAll(app,canvas):
    drawCharacters(app,canvas)
    canvas.create_text(300,50,font="Arial 26", text=app.enemy.health)
    drawTerrain(app,canvas)
    drawBullets(app,canvas)

def Game_keyPressed(app,event):
    if event.key=="Space":
        app.character.isFiring=not app.character.isFiring
    if event.key=="z":
        app.isFocus=not app.isFocus
    if event.key in ("Up","Down","Left","Right"):
        app.keyHoldDict[event.key]=True
    if event.key=="1":
        pattern1(300,50,10,8,2,1,100,0,app.bulletList)
        pattern1(100,50,10,8,2,1,100,5,app.bulletList)
        pattern1(500,50,10,8,2,1,100,5,app.bulletList)
    if event.key=="2":
        app.pattern2gen=True
        app.pattern2start=app.timePassed
        app.pattern2count=5
        app.pattern2gencount=0
        """count=5
        startTime=app.timePassed
        for i in range(count):
            while(app.timePassed<startTime+i*1000):
                print(app.timePassed)
                pass
        app.bulletList.append(bullet(300,100,2,90,8,1,114))
        """
def Game_keyReleased(app,event):
    if event.key in ("Up","Down","Left","Right"):
        app.keyHoldDict[event.key]=False
        
def Game_timerFired(app):
    app.timePassed+=app.timerDelay
    #pattern 2 generation. Somehow this only works in timerFired function so sorry if this looks messy
    if app.pattern2gen:
        if app.timePassed>app.pattern2start+1000*app.pattern2gencount:
            app.bulletList.append(bullet(300,100,2,90,8,1,114))
            app.pattern2gencount+=1
        if app.pattern2gencount>app.pattern2count:
            app.pattern2gen=False
    checkMovements(app)
    if app.character.isFiring:
        firePlayerBullet(app.character,True,app.playerBulletList)
    for Bullet in app.bulletList:
        if not Bullet.freeze:
            dx,dy=polar2cart(Bullet.direction,Bullet.speed)
            Bullet.x+=dx
            Bullet.y+=dy
        if checkCollision(app.character,Bullet,app.bulletList):
            print("Collision Detected")
        if checkGraze(app.character,Bullet) and not Bullet.grazed:
            print("Graze Detected")
            Bullet.grazed=True
    for playerBullet in app.playerBulletList:
        checkEnemyCollision(app.enemy,playerBullet,app.playerBulletList,app)
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
    
