import pygame
from pygame.locals import *
from math import *
from bullets import *
from spriteloader import *
from settings import *
pygame.init()

def clamp(source, min, max):
	if (source > max):
		return max
	elif (source < min):
		return min
	else:
		return source

health = PLAYER_HEALTH

playerpos = [300,500]
playerrot = 0

shotlastturn = False

def setPlayerPos(x,y):
	playerpos = [x,y]

def setPlayerRot(deg):
	playerrot = radians(deg)

def drawPlayer(scrn):
	scrn.blit(IMG_PLAYER, (playerpos[0]-IMG_PLAYER.get_width()/2, playerpos[1]-IMG_PLAYER.get_height()/2))

def updatePlayer(keys,dt,bullets):
	global shotlastturn

	if (keys[K_z] and not shotlastturn):
		bullets.append(PlayerBullet((playerpos[0], playerpos[1]), (0,-PLAYER_BULLET_SPEED)))
		shotlastturn = True
	elif not keys[K_z]:
		shotlastturn = False

	horizontal = PLAYER_HORIZONTAL_SPEED * (keys[K_RIGHT]-keys[K_LEFT])
	vertical =  (keys[K_DOWN]*PLAYER_BACKWARD_SPEED-keys[K_UP]*PLAYER_FORWARD_SPEED)
	playerpos[0] += horizontal*dt
	playerpos[1] += vertical*dt
	playerpos[0] = clamp(playerpos[0], 0, 600)
	playerpos[1] = clamp(playerpos[1], 0, 600)
