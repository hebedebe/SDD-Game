from settings import *
import random
import numpy as np
import colorama
from copy import deepcopy
from colorama import Fore, Back
from tqdm import tqdm
import matplotlib.pyplot as plt
from perlin_numpy import (
    generate_fractal_noise_2d, generate_fractal_noise_3d,
    generate_perlin_noise_2d, generate_perlin_noise_3d
)
colorama.init()

generate_large = False
generate_medium = False
generate_small = True

asteroid_types_large = []
asteroid_types_medium = []
asteroid_types_small = []

print("Initialising asteroid module\n\n\n")

if (generate_large):
	for a in tqdm(range(NUM_LARGE_ASTEROIDS), desc="Generating large asteroid types"):
		np.random.seed(random.randrange(RANDOM_SEED_RANGE))
		noise = generate_fractal_noise_2d(ASTEROID_SHAPE_LARGE, ASTEROID_RESOLUTION, ASTEROID_OCTAVES)

		fixednoise = []
		falloff = []

		for x in range(len(noise)):
			fixednoise.append([])
			falloff.append([])
			xdist = abs(len(noise)/2-x)
			for y in range(len(noise)):
				ydist = abs(len(noise)/2-y)
				falloff[x].append(ydist+xdist)
				if noise[x,y]-((ydist+xdist)*ASTEROID_NOISE_MULTIPLIER)/len(noise) >= ASTEROID_NOISE_THRESHOLD+ydist/len(noise)+xdist/len(noise):
					fixednoise[x].append(1)
				else:
					fixednoise[x].append(0)
		generation_success = False
		for x in fixednoise:
			for y in x:
				if y > 0:
					generation_success = True
					break

		while not generation_success:
			print(f"\033[F\033[F{Fore.RED}Large asteroid shape generation failed. Retrying{Fore.RESET}\n")
			np.random.seed(random.randrange(RANDOM_SEED_RANGE))
			noise = generate_fractal_noise_2d(ASTEROID_SHAPE_LARGE, ASTEROID_RESOLUTION, ASTEROID_OCTAVES)

			fixednoise = []
			falloff = []
	
			for x in range(len(noise)):
				fixednoise.append([])
				falloff.append([])
				xdist = abs(len(noise)/2-x)
				for y in range(len(noise)):
					ydist = abs(len(noise)/2-y)
					falloff[x].append(ydist+xdist)
					if noise[x,y]-((ydist+xdist)*ASTEROID_NOISE_MULTIPLIER)/len(noise) >= ASTEROID_NOISE_THRESHOLD+ydist/len(noise)+xdist/len(noise):
						fixednoise[x].append(1)
					else:
						fixednoise[x].append(0)

			generation_success = False
			for x in fixednoise:
				for y in x:
					if y > 0:
						generation_success = True
						break
		asteroid_types_large.append(deepcopy(fixednoise))


if (generate_medium):
	for a in tqdm(range(NUM_MEDIUM_ASTEROIDS), desc="Generating medium asteroid types"):
		np.random.seed(random.randrange(RANDOM_SEED_RANGE))
		noise = generate_fractal_noise_2d(ASTEROID_SHAPE_MEDIUM, ASTEROID_RESOLUTION, ASTEROID_OCTAVES)

		fixednoise = []
		falloff = []

		for x in range(len(noise)):
			fixednoise.append([])
			falloff.append([])
			xdist = abs(len(noise)/2-x)
			for y in range(len(noise)):
				ydist = abs(len(noise)/2-y)
				falloff[x].append(ydist+xdist)
				if noise[x,y]-((ydist+xdist)*ASTEROID_NOISE_MULTIPLIER)/len(noise) >= ASTEROID_NOISE_THRESHOLD+ydist/len(noise)+xdist/len(noise):
					fixednoise[x].append(1)
				else:
					fixednoise[x].append(0)
		generation_success = False
		for x in fixednoise:
			for y in x:
				if y > 0:
					generation_success = True
					break

		while not generation_success:
			print(f"\033[F\033[F{Fore.RED}Medium asteroid shape generation failed. Retrying{Fore.RESET}\n")
			np.random.seed(random.randrange(RANDOM_SEED_RANGE))
			noise = generate_fractal_noise_2d(ASTEROID_SHAPE_MEDIUM, ASTEROID_RESOLUTION, ASTEROID_OCTAVES)

			fixednoise = []
			falloff = []
	
			for x in range(len(noise)):
				fixednoise.append([])
				falloff.append([])
				xdist = abs(len(noise)/2-x)
				for y in range(len(noise)):
					ydist = abs(len(noise)/2-y)
					falloff[x].append(ydist+xdist)
					if noise[x,y]-((ydist+xdist)*ASTEROID_NOISE_MULTIPLIER)/len(noise) >= ASTEROID_NOISE_THRESHOLD+ydist/len(noise)+xdist/len(noise):
						fixednoise[x].append(1)
					else:
						fixednoise[x].append(0)

			generation_success = False
			for x in fixednoise:
				for y in x:
					if y > 0:
						generation_success = True
						break
		asteroid_types_medium.append(deepcopy(fixednoise))


if (generate_small):
	for a in tqdm(range(NUM_SMALL_ASTEROIDS), desc="Generating small asteroid types"):
		np.random.seed(random.randrange(RANDOM_SEED_RANGE))
		noise = generate_fractal_noise_2d(ASTEROID_SHAPE_SMALL, ASTEROID_RESOLUTION, ASTEROID_OCTAVES)

		fixednoise = []
		falloff = []

		for x in range(len(noise)):
			fixednoise.append([])
			falloff.append([])
			xdist = abs(len(noise)/2-x)
			for y in range(len(noise)):
				ydist = abs(len(noise)/2-y)
				falloff[x].append(ydist+xdist)
				if noise[x,y]-((ydist+xdist)*ASTEROID_NOISE_MULTIPLIER)/len(noise) >= ASTEROID_NOISE_THRESHOLD+ydist/len(noise)+xdist/len(noise):
					fixednoise[x].append(1)
				else:
					fixednoise[x].append(0)
		generation_success = False
		for x in fixednoise:
			for y in x:
				if y > 0:
					generation_success = True
					break

		while not generation_success:
			print(f"\033[F\033[F{Fore.RED}Small asteroid shape generation failed. Retrying{Fore.RESET}\n")
			np.random.seed(random.randrange(RANDOM_SEED_RANGE))
			noise = generate_fractal_noise_2d(ASTEROID_SHAPE_SMALL, ASTEROID_RESOLUTION, ASTEROID_OCTAVES)

			fixednoise = []
			falloff = []
	
			for x in range(len(noise)):
				fixednoise.append([])
				falloff.append([])
				xdist = abs(len(noise)/2-x)
				for y in range(len(noise)):
					ydist = abs(len(noise)/2-y)
					falloff[x].append(ydist+xdist)
					if noise[x,y]-((ydist+xdist)*ASTEROID_NOISE_MULTIPLIER)/len(noise) >= ASTEROID_NOISE_THRESHOLD+ydist/len(noise)+xdist/len(noise):
						fixednoise[x].append(1)
					else:
						fixednoise[x].append(0)

			generation_success = False
			for x in fixednoise:
				for y in x:
					if y > 0:
						generation_success = True
						break
		asteroid_types_small.append(deepcopy(fixednoise))

print(f"{Fore.GREEN}Asteroid type generation complete{Fore.RESET}")

class Asteroid():
	def __init__(self,shape,pos,vel):
		self.pos = pos
		self.vel = vel
		self.chunks = []
		for x in range(int(len(shape)/ASTEROID_CHUNK_SIZE)):
			for y in range(int(len(shape[x])/ASTEROID_CHUNK_SIZE)):
				if shape[x*ASTEROID_CHUNK_SIZE][y*ASTEROID_CHUNK_SIZE] > 0:
					self.chunks.append((x*ASTEROID_CHUNK_SIZE,y*ASTEROID_CHUNK_SIZE))
	def update(self,scrn,dt):
		self.pos = (self.pos[0]+self.vel[0]*dt, self.pos[1]+self.vel[1]*dt)
		for c in self.chunks:
			pygame.draw.rect(scrn, ASTEROID_COLOUR, pygame.Rect(int(self.pos[0]+c[0]-ASTEROID_CHUNK_SIZE/2), int(self.pos[1]+c[1]-ASTEROID_CHUNK_SIZE/2), ASTEROID_CHUNK_SIZE, ASTEROID_CHUNK_SIZE))
			#scrn.set_at((int(self.pos[0]+c[0]), int(self.pos[1]+c[1])), ASTEROID_COLOUR)