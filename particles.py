import pygame
from pygame import Vector2


class Particle:
    def __init__(self, pos, colour="white"):
        self.pos = Vector2(pos)
        self.velocity = Vector2()
        self.drag = 0
        self.colour = colour
        self.size = 5
        self.size_per_second = 0
        self.gravity = Vector2(0, 800)
        self.kill = False

    def update(self, delta_time):
        self.velocity += self.gravity * delta_time
        self.velocity = self.velocity.lerp(Vector2(), self.drag * delta_time)
        self.pos += self.velocity * delta_time

        self.size += self.size_per_second * delta_time

    def draw(self, display, world):
        pygame.draw.circle(display, self.colour, world.worldToScreenPosition(self.pos), self.size)


class ExpandingCircleParticle(Particle):
    def __init__(self, pos, target_radius, colour):
        super().__init__(pos, colour)
        self.radius = target_radius / 2
        self.width = self.radius

        self.target_radius = target_radius
        self.target_width = 1

    def update(self, delta_time):
        rad_spd = 4 * 100 / self.target_radius
        wid_spd = rad_spd * 7 / 4

        self.radius = pygame.math.lerp(self.radius, self.target_radius, rad_spd * delta_time)
        self.width = pygame.math.lerp(self.width, self.target_width, wid_spd * delta_time)

        if self.width <= 1.5:
            self.kill = True

    def draw(self, display, world):
        pygame.draw.circle(display, self.colour, world.worldToScreenPosition(self.pos), self.radius, int(self.width))
