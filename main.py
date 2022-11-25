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
    app.character=Player(4,"Yuyuko",300,590,5,1,1)
    app.isFocus=False
    testCircularTerrain(300,300,50,app.terrainList)
    app.mode="Start"
    app.cleared=True
    app.scroll=0
    app.enemy=None
    app.enemy=Enemy(2,"Hakurei Reimu",11451,300,50,10,1)
    app.keyHoldDict=dict()
    app.keyHoldDict["Up"]=False
    app.keyHoldDict["Down"]=False
    app.keyHoldDict["Left"]=False
    app.keyHoldDict["Right"]=False
    app.score=0
    app.pattern2gen=False
    app.characterImage=app.loadImage('Yuyuko_char.png')
    app.enemyImage=app.loadImage('Reimu_enemy.png')
    app.stageBackground=app.loadImage('Stage_Background_Alt.png')
    app.grazeCount=0

def checkMovements(app):
    cx=app.character.x
    cy=app.character.y
    
    if app.keyHoldDict["Up"] and checkTerrain(app.character,app.terrainList) not in (4,5,7) and not cy<0:
        if app.isFocus:
            app.character.y-=0.2*app.character.speed
        else:
            app.character.y-=app.character.speed
    if app.keyHoldDict["Down"] and checkTerrain(app.character,app.terrainList) not in (3,6,8) and not cy>app.height:
        if app.isFocus:
            app.character.y+=0.2*app.character.speed
        else:
            app.character.y+=app.character.speed
    if app.keyHoldDict["Left"] and checkTerrain(app.character,app.terrainList) not in (2,5,6) and not cx<0:
        if app.isFocus:
            app.character.x-=0.2*app.character.speed
        else:
            app.character.x-=app.character.speed
    if app.keyHoldDict["Right"] and checkTerrain(app.character,app.terrainList) not in (1,7,8) and not cx>0.75*app.width:
        if app.isFocus:
            app.character.x+=0.2*app.character.speed
        else:
            app.character.x+=app.character.speed

def bulletTick(app):
    for Bullet in app.bulletList:
        if not Bullet.freeze:
            dx,dy=polar2cart(Bullet.direction,Bullet.speed)
            Bullet.x+=dx
            Bullet.y+=dy
        if not app.character.isInvincible:
            if checkCollision(app.character,Bullet,app.bulletList):
                print("Collision Detected")
        if checkGraze(app.character,Bullet) and not Bullet.grazed:
            Bullet.grazed=True
            app.grazeCount+=1

def enemyTick(app):
    if app.enemy.health<=0:
        app.enemy=None
    if app.enemy is not None:
        if app.enemy.x<100:
            if 10<app.enemy.y<100:
                app.enemy.direction=80
            elif app.enemy.y<10:
                app.enemy.direction=45
            else:
                app.enemy.direction=-45
        elif app.enemy.x>500:
            if 10<app.enemy.y<100:
                app.enemy.direction=100
            elif app.enemy.y<10:
                app.enemy.direction=135
            else:
                app.enemy.direction=-135
        if app.enemy.y<10:
            if 100<app.enemy.x<500:
                app.enemy.direction=10
        elif app.enemy.y>100:
            if 100<app.enemy.x<500:
                app.enemy.direction=190
        newDir=random.randint(app.enemy.direction-5,zapp.enemy.direction+5)
        app.enemy.direction=newDir
        dx,dy=polar2cart(app.enemy.direction,app.enemy.speed)
        app.enemy.x+=dx
        app.enemy.y+=dy

def playerBulletTick(app):
    for playerBullet in app.playerBulletList:
        if app.enemy is not None:
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
        
def drawPowerups(app,canvas):
    for powerup in app.powerUpList:
        if powerup.type=="invincible":
            canvas.create_oval(powerup.x-10,powerup.y-10,powerup.x+10,powerup.y+10,fill="blue")
        elif powerup.type=="power":
            canvas.create_oval(powerup.x-10,powerup.y-10,powerup.x+10,powerup.y+10,fill="red")
        elif powerup.type=="track":
            canvas.create_oval(powerup.x-10,powerup.y-10,powerup.x+10,powerup.y+10,fill="purple")

def drawScore(app,canvas):
    canvas.create_text(650,50,font='Arial 20',text=f"Score\n {app.score}")
    canvas.create_text(650,150,font='Arial 20',text=f"Graze\n {app.grazeCount}")
def drawCharacters(app,canvas):
    canvas.create_image(app.character.x,app.character.y,image=ImageTk.PhotoImage(app.characterImage))
    canvas.create_oval(app.character.x-app.character.radius,app.character.y-app.character.radius,
    app.character.x+app.character.radius,app.character.y+app.character.radius,fill="white")
    if app.enemy is not None:
        canvas.create_image(app.enemy.x,app.enemy.y,image=ImageTk.PhotoImage(app.enemyImage))
        canvas.create_oval(app.enemy.x-app.enemy.radius,app.enemy.y-app.enemy.radius,
        app.enemy.x+app.enemy.radius,app.enemy.y+app.enemy.radius,fill="magenta")

def Start_redrawAll(app,canvas):
    canvas.create_text(300,300,font="Helvetica", text="Press any key to start")

def Start_keyPressed(app,event):
    app.mode="Game"

def Game_redrawAll(app,canvas):
    canvas.create_image(300,300,image=ImageTk.PhotoImage(app.stageBackground))
    drawCharacters(app,canvas)
    if app.enemy is not None:
        canvas.create_text(300,50,font="Arial 26", text=app.enemy.health)
    drawTerrain(app,canvas)
    drawBullets(app,canvas)
    drawScore(app,canvas)

def Game_keyPressed(app,event):
    if event.key=="Space":
        app.character.isFiring=not app.character.isFiring
    if event.key=="z":
        app.isFocus=not app.isFocus
    if event.key in ("Up","Down","Left","Right"):
        app.keyHoldDict[event.key]=True
    if event.key=="1":
        pattern1(300,50,10,8,2,1,100,0,app)
        pattern1(100,50,10,8,2,1,100,5,app)
        pattern1(500,50,10,8,2,1,100,5,app)
    if event.key=="2":
        app.pattern2gen=True
        app.pattern2start=app.timePassed
        app.pattern2count=5
        app.pattern2gencount=0
    if event.key=="3":
        randomBullet(app,5,10,5,114)
        
def Game_keyReleased(app,event):
    if event.key in ("Up","Down","Left","Right"):
        app.keyHoldDict[event.key]=False
        
def Game_timerFired(app):
    app.timePassed+=app.timerDelay
    if app.enemy is not None:
        enemyTick(app)
    if app.pattern2gen:
        pattern2(app,300,100,5,90,5,1,114,10,200)
    checkMovements(app)
    if app.character.isFiring:
        firePlayerBullet(app.character,True,app.playerBulletList)
    bulletTick(app)
    playerBulletTick(app)
    clean(app,app.bulletList,app.playerBulletList) 
    '''if app.timePassed<3000:
        if app.timePassed%100==0:
            randomBullet(app,4,5,1,114)
    if 3000<=app.timePassed<=3050: 
        app.enemy=Enemy(2,"Hakurei Reimu",11451,300,50,10,1)
    '''
runApp(height=600,width=800)
    
