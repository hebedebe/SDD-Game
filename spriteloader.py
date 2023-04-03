import pygame
pygame.init()

def loadimg(name):
	return pygame.image.load(f"./sprites/{name}")

IMG_PLAYER = loadimg("player.png")
#IMG_ENEMY1 = loadimg("enemy1.png")
#IMG_ENEMY2 = loadimg("enemy2.png")
#IMG_ENEMY3 = loadimg("enemy3.png")
#IMG_BACKGROUND = loadimg("background.png")