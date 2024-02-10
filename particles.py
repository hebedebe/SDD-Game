import pygame
from pygame import Vector2

import random


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

        if self.size <= 0:
            self.kill = True
            self.size = 0

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


class Spark(Particle):
    def __init__(self, pos, length, direction, colour="white"):
        super().__init__(pos, colour)
        self.length = length
        self.direction = direction
        self.width = 5

    def update(self, delta_time):
        width_shrink_speed = 10
        length_shrink_speed = 10
        self.width = pygame.math.lerp(self.width, 0, delta_time * width_shrink_speed)
        self.length = pygame.math.lerp(self.length, 0, delta_time * length_shrink_speed)

        if self.length <= 0.3 and self.width <= 0.3:
            self.kill = True

    def draw(self, display, world):
        front_tip = world.worldToScreenPosition(self.pos + (self.direction * self.length))
        back_tip = world.worldToScreenPosition(self.pos - (self.direction * self.length))
        left = world.worldToScreenPosition(self.pos + (self.direction.rotate(-90) * self.width))
        right = world.worldToScreenPosition(self.pos + (self.direction.rotate(90) * self.width))

        pygame.draw.polygon(display, self.colour,
                            [
                                front_tip,
                                right,
                                back_tip,
                                left
                            ])


def emitCircle(pos, count, colour, velocity_min, velocity_max):
    particles = []

    angle_step = 360 // count
    for step in range(count):
        angle = step * angle_step
        direction = Vector2(0, 1).rotate(angle)
        particle = Particle(
            pos,
            colour
        )
        particle.velocity = direction * random.randint(velocity_min, velocity_max)
        # particle.gravity = Vector2(0, 0)
        particle.size_per_second = -10
        particles.append(particle)

    return particles


def worldEmitCircle(world, pos, count, colour, velocity_min, velocity_max):
    particles = emitCircle(pos, count, colour, velocity_min, velocity_max)
    for p in particles:
        world.addParticle(p)
