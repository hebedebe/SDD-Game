import pygame
from math import *
import random
from settings import *

pygame.init()

def dist(p1,p2):
    return (p1[0]-p2[0])**2 + (p1[1]-p2[1])**2

class PlayerBullet():
    def __init__(self, pos, vel):
        self.pos = pos
        self.lastpos = pos
        self.vel = vel
        self.health = PLAYER_BULLET_HEALTH
    def update(self, scrn, dt, asteroids):
        self.pos = (self.pos[0]+self.vel[0]*dt, self.pos[1]+self.vel[1]*dt)
        #pygame.draw.rect(scrn, PLAYER_BULLET_COLOUR, pygame.Rect(self.pos[0]-BULLET_CHUNK_SIZE/2, self.pos[1]-BULLET_CHUNK_SIZE/2, BULLET_CHUNK_SIZE, BULLET_CHUNK_SIZE))
        #scrn.set_at((int(self.pos[0]), int(self.pos[1])), PLAYER_BULLET_COLOUR)
        pygame.draw.line(scrn, PLAYER_BULLET_COLOUR, (self.pos[0], self.pos[1]-BULLET_LENGTH), (self.pos[0], self.pos[1]), BULLET_WIDTH)
        for y in range(int(abs(self.pos[1]-self.lastpos[1]))+BULLET_LENGTH):
            pos = [self.pos[0], self.pos[1]+int(abs(self.pos[1]-self.lastpos[1])+BULLET_LENGTH)-y]
            for a in asteroids:
                if dist(pos, a.pos) <= BULLET_CHECK_DISTANCE and self.health > 0:
                    chunkstoremove = []
                    for c in a.chunks:
                        if c not in chunkstoremove and dist(pos,(a.pos[0]+c[0], a.pos[1]+c[1])) <= (BULLET_CHUNK_SIZE/2)**2:
                            chunkstoremove.append(c)
                            for c2 in a.chunks:
                                if c is not c2 and c2 not in chunkstoremove and dist(pos,(a.pos[0]+c2[0], a.pos[1]+c2[1])) <= (PLAYER_BULLET_EXPLOSION_SIZE/2+random.randint(-3,3))**2:
                                    chunkstoremove.append(c2)
                            self.health -= 1
                    for d in chunkstoremove:
                        a.chunks.remove(d)
        self.lastpos = self.pos
        return self.pos[1] + BULLET_LENGTH < 0 or self.health <= 0
