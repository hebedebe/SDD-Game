from asteroids import *
import pygame
from spriteloader import *
from settings import *
from player import *
from tqdm import tqdm
from pygame.locals import *
from enemies import *
import threading

pygame.init()

clock = pygame.time.Clock()

asteroids = []
bullets = []
enemies = []

width, height = 600, 600

running = True

window = pygame.display.set_mode((width, height))
scrn = pygame.Surface((width, height), pygame.SRCALPHA, 32)

mode = 0 #menu
threads = []

def update_enemies():
	threadclock = pygame.time.Clock()
	while running:
		#clock.tick(60)
		for x in enemies:
			for y in x:
				for b in y:
					b.update(dt, enemies)

for x in tqdm(range(ENEMY_X_PARTITIONS), desc="Generating enemy partitions"):
	enemies.append([])
	for y in range(ENEMY_Y_PARTITIONS):
		enemies[x].append([])

#for t in range(PARTITION_THREADS):
#	threads.append(threading.Thread(target=update_enemies, args=(t,)))

enemythread = threading.Thread(target=update_enemies, args=())

while running:
	clock.tick(60)
	dt = TIMESCALE#clock.tick(60)/1000
	window.fill(BACKGROUND_COLOUR)
	scrn.fill((0,0,0,0))
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			running = False
	keys = pygame.key.get_pressed()

	if mode == 0: #menu
		title = MENU_FONT.render('Click To Add Title', True, WHITE)
		titleRect = title.get_rect()
		titleRect.center = (width // 2, 60)

		start = DEFAULT_FONT.render('Z TO START', True, WHITE)
		startRect = start.get_rect()
		startRect.center = (width // 2, height - 120)

		scrn.blit(title, titleRect)
		scrn.blit(start, startRect)
		
		if keys[K_z]:
			setPlayerPos(width/2, height-60)
			mode = 1
			for i in range(20):
				e = Boid()
				p = find_partition(e.pos)
				enemies[p[0]][p[1]].append(e)

		if keys[K_x]:
			mode = 3
			for i in range(200):
				e = Boid()
				p = find_partition(e.pos)
				enemies[p[0]][p[1]].append(e)
			#enemythread.start()


	if mode == 1: #in game
		for b in bullets:
			if b.update(scrn, dt, asteroids):
				bullets.remove(b)

		for p in enemies:
			for p2 in p:
				for b in p2:
					b.update(playerpos, enemies)
					b.draw(scrn)

		updatePlayer(keys, dt, bullets)
		drawPlayer(scrn)

		if random.randint(0,6000) < ENEMY_SPAWN_CHANCE:
			#enemies.append(enemySwarm((random.randint(0,600), -100), (0,0), 50, 0))
			#print("spawned enemy swarm")
			pass


		for a in asteroids:
			a.update(scrn, dt)
			if (a.pos[1] > height+100):
				asteroids.remove(a)
		if random.randint(0,6000) < ASTEROID_SPAWN_CHANCE:
			asteroids.append(Asteroid(asteroid_types_small[random.randint(0,NUM_SMALL_ASTEROIDS-1)], (random.randint(0,width),-20), (0,random.randint(ASTEROID_MIN_SPEED, ASTEROID_MAX_SPEED))))

	if mode == 2: #death screen
		pass

	if mode == 3: #boid testing
		for p in enemies:
			for p2 in p:
				for b in p2:
					b.update(playerpos, enemies)
					b.draw(scrn)

	fps = DEBUG_FONT.render(str(int(clock.get_fps())), True, WHITE)
	fpsRect = fps.get_rect()
	fpsRect.topleft = (10, 10)
	scrn.blit(fps, fpsRect)

	window.blit(scrn, (0,0))
	pygame.display.flip()