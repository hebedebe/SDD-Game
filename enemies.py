import pygame
from math import *
from settings import *
import random

def findDir(p1, p2):
    rel_x, rel_y = p2[0] - p1[0], p2[1] - p1[1]
    angle = atan2(rel_y, rel_x)
    return angle

def clamp(source, min, max):
	if (source > max):
		return max
	elif (source < min):
		return min
	else:
		return source

def dist(p1,p2):
    return (p1[0]-p2[0])**2 + (p1[1]-p2[1])**2

def lerp(a, b, c):
    return a+(b-a)*c

def find_partition(pos):
    x,y = pos[0], pos[1]
    x_partition = int((x/ENEMY_X_PARTITIONS)/6)
    y_partition = int((y/ENEMY_Y_PARTITIONS)/6)
    return [x_partition, y_partition]

def find_eligible_partitions(partition, partition_dist=1, wraparound = False):
    x_partition = partition[0]
    y_partition = partition[1]
    eligible_partitions = []
    for x in range(2*partition_dist+1):
        for y in range(2*partition_dist+1):
            eligible_partitions.append([x_partition+(x-partition_dist),y_partition+(y-partition_dist)])
    return eligible_partitions

class Boid():
    def __init__(self):
        self.pos = [random.randrange(0, 600), random.randrange(0, 600)]
        self.vel = [0,0]
        self.dir = radians(random.randrange(0,360))
    def update(self, playerpos, boids):
        interactions = 1
        groupdir = 0#self.dir
        centerofmass = [0,0]#self.pos
        eligible_partitions = find_eligible_partitions(find_partition(self.pos))
        for p in eligible_partitions:
            for b in boids[p[0]][p[1]]:
                direction = findDir(self.pos, b.pos)
                if (dist(self.pos, b.pos) > ENEMY_SIGHT_DIST or b is self or abs(direction) > ENEMY_FOV/2 or b.pos == self.pos):
                    continue
                interactions += 1

                #1. separation
                distance = dist(self.pos, b.pos)
                self.dir = lerp(self.dir, radians(-degrees(direction)), ENEMY_REPULSION/distance)

                #2. alignment
                groupdir += b.dir
                
                #3. cohesion
                centerofmass[0] += b.pos[0]
                centerofmass[1] += b.pos[1]

        groupdir /= interactions
        centerofmass[0] /= interactions
        centerofmass[1] /= interactions

        targetdir = lerp(groupdir, findDir(self.pos, centerofmass), ENEMY_CMASS_WEIGHTING)

        self.dir = lerp(self.dir, targetdir, ENEMY_ALIGNMENT_STRENGTH)+random.randint(-int(ENEMY_RANDOMNESS*1000), int(ENEMY_RANDOMNESS*1000))/1000

        playerdir = findDir(self.pos, playerpos)
        #if abs(self.dir-playerdir) <= ENEMY_FOV:
        self.dir = lerp(self.dir, playerdir, ENEMY_TARGET_WEIGHTING)

        self.vel[0] += cos(self.dir)*ENEMY_ACCELERATION
        self.vel[1] += sin(self.dir)*ENEMY_ACCELERATION

        #self.vel[0] = clamp(self.vel[0], -ENEMY_MAX_SPEED, ENEMY_MAX_SPEED)
        #self.vel[1] = clamp(self.vel[1], -ENEMY_MAX_SPEED, ENEMY_MAX_SPEED)

        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]

        self.vel[0] *= ENEMY_FRICTION
        self.vel[1] *= ENEMY_FRICTION

        if (self.pos[0] > 600):
            self.pos[0] = 0
        elif (self.pos[0] < 0):
            self.pos[0] = 600

        if (self.pos[1] > 600):
            self.pos[1] = 0
        elif (self.pos[1] < 0):
            self.pos[1] = 600

    def draw(self, scrn):
        pygame.draw.circle(scrn, ENEMY_COLOUR, self.pos, 2)
        #pygame.draw.line(scrn, DEBUG_COLOUR, self.pos, (self.pos[0]+cos(self.dir)*20, self.pos[1]+sin(self.dir)*20), 2)
        #pygame.draw.line(scrn, DEBUG_COLOUR_2, self.pos, (self.pos[0]+self.vel[0]*10, self.pos[1]+self.vel[1]*10), 2)