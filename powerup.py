from helper import *
from classdec import *

def checkPowerupPickup(character,powerup,powerupList):
    if distance(character.x,character.y,powerup.x,powerup.y)<=20+character.radius+powerup.r:
        powerupList.remove(powerup)
        if powerup.type=="invincible":
            #grants immunity for 15 seconds
            character.isInvincible=True
            character.timer=15000
        if powerup.type=="track":
            character.canTrack=True
        if powerup.type=="power":
            character.power+=1