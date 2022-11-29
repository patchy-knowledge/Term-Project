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
    app.keyHoldDict=dict()
    app.keyHoldDict["Up"]=False
    app.keyHoldDict["Down"]=False
    app.keyHoldDict["Left"]=False
    app.keyHoldDict["Right"]=False
    app.score=0
    app.pattern2gen=False
    app.characterImage=app.loadImage('Yuyuko_char.png')
    app.enemyImage=app.loadImage('Reimu_enemy.png')
    app.enemyBulletImage=app.loadImage('Reimu_shot.png')
    app.stageBackground=app.loadImage('Stage_Background_Alt.png')
    app.playerBulletImage=app.loadImage('Yuyuko_shot.png')
    app.grazeCount=0
    app.pattern2start=None
    app.stage=2
    app.initialized=False

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
        newDir=random.randint(app.enemy.direction-5,app.enemy.direction+5)
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
def drawBullets(app,canvas):
    for bullet in app.bulletList:
        canvas.create_image(bullet.x,bullet.y,image=ImageTk.PhotoImage(app.enemyBulletImage))
    for playerBullet in app.playerBulletList:
        canvas.create_image(playerBullet.x,playerBullet.y,image=ImageTk.PhotoImage(app.playerBulletImage))

def stage1(app):
    #to-do: load Reimu's bullet image
    if app.timePassed<15000:
        if app.timePassed%100==0:
            randomBullet(app,2,5,1,114)
    elif 15000<=app.timePassed<=15050: 
        app.enemy=Enemy(2,"Hakurei Reimu",191981,300,50,10)
    elif app.timePassed>15050:
        if app.enemy is not None:
            if app.timePassed%100==0:
                bossBullet(app,3,5,5,114514)
            if 20000<=app.timePassed<=23000:
                if app.timePassed%600==0:
                    pattern1(app.enemy.x,app.enemy.y,5,5,2,1,1000,random.randint(-10,10),app)
            if 23000<app.timePassed<30000:
                if app.timePassed%75==0:
                    bossBullet(app,3,5,5,114514)
            if 30000<=app.timePassed<=35000:
                if app.pattern2start==None:
                    app.pattern2start=app.timePassed
                    app.pattern2gencount=0
                    app.xyList=[]
                    for i in range(10):
                        app.xyList.append((100+i*40+random.randint(-10,10),100+random.randint(-20,20)))
                pattern2(app,app.xyList,5,90,5,1,114,100,50)
        else:
            #reset stage
            app.stage=2
            app.timePassed=0
            app.pattern2start=None
            app.initialized=False

def stage2(app):
    #to do: load Marisa's bullet image
    #to do: modify drawEnemy
    if not app.initialized:
        app.enemyImage=app.loadImage('Marisa_enemy.png')
        app.enemyBulletImage=app.loadImage('Marisa_shot.png')
    if app.timePassed<20000:
        if app.timePassed%75==0:
            randomBullet(app,4,4,10,114514)
    elif 20000<app.timePassed<20050:
        app.enemy=Enemy(3,"Kirisame Marisa",114514,300,50,10)
    elif app.timePassed>20050:
        if app.enemy is not None:
            if app.timePassed%66==0:
                bossBullet(app,4,4,5,114514)
            if 23000<app.timePassed<30000:
                if app.pattern2start is None:
                    app.pattern2start=app.timePassed
                    app.pattern2gencount=0
                    app.xyList=[]
                    for i in range(15):
                        app.xyList.append((100+random.randint(-20,20),40*i))
                pattern2(app,app.xyList,3,0,4,1,1000,100,50)
                if app.timePassed%500==0:
                    pattern1(app.enemy.x,app.enemy.y,3,4,3,1,1000,random.randint(-20,20),app)
        else:
            #reset stage
            app.stage=3
            app.timePassed=0
            app.pattern2start=None
            app.initialized=False

def stage3(app):
    #to do: draw tenshi's bullet image, tenshi resource
    #to do: change drawEnemy
    if not app.initialized:
        app.enemyImage=app.loadImage('Tenshi_enemy.png')
        app.enemyBulletImage=app.loadImage('Tenshi_shot.png')
    if app.timePassed<15000:
        if app.timePassed%66==0:
            randomBullet(app,2,5,1,1145)
        elif 15000<=app.timePassed<=15050:
            app.enemy=Enemy(1.5,"Hinanawi Tenshi",198893,300,50,10)
        elif app.timePassed>15050:
            if app.enemy is not None:
                if app.timePassed%50==0:
                    bossBullet(app,3,5,5,1145)
                if 20000<app.timePassed<25000 or 30000<app.timePassed<35000:
                    if app.pattern2start is None:
                        app.pattern2start=app.timePassed
                        app.pattern2gencount=0
                        app.xyList=[]
                        for i in range(15):
                            app.xyList.append((30+35*i+random.randint(-10,10),100))
                    pattern2(app,app.xyList,2,90,5,10,114,150,50)
                    if app.timePassed%400==0:
                        pattern1(app.enemy.x,app.enemy.y,2.5,5,2,10,100,random.randint(-10,10),app)
        else:
            #ends
            app.mode="End"
            
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
        app.xyList=[(100,100),(200,100),(300,100),(400,100),(500,100)]
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
    checkMovements(app)
    if app.character.isFiring:
        firePlayerBullet(True,app)
    bulletTick(app)
    playerBulletTick(app)
    clean(app,app.bulletList,app.playerBulletList) 
    stage2(app)
    print(app.timePassed)
runApp(height=600,width=800)
    
