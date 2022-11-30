from helper import *
from classdec import *

def checkPowerupPickup(powerup,app):
    if distance(app.character.x,app.character.y,powerup.x,powerup.y)<=20+app.character.radius+powerup.r:
        app.powerupList.remove(powerup)
        if powerup.type=="Invincible":
            #grants immunity for 5 seconds
            app.character.isInvincible=True
            app.character.timer=5000
        if powerup.type=="Track":
            app.character.canTrack=True
        if powerup.type=="Power":
            app.character.power+=0.25
        if powerup.type=="Extend":
            app.character.life+=1
        if powerup.type=="Bomb":
            app.character.bomb+=1

def cleanPowerup(app):
    for powerup in app.powerupList:
        if powerup.y>600:
            app.powerupList.remove(powerup)