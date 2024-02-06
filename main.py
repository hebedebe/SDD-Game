import pygame
from pygame.locals import *
from pygame import Vector2

import pygame_gui as gui

import random

pygame.init()

FPS = 6000
TILE_SIZE = 16
CHUNK_SIZE = Vector2(20, 20)

width, height = 160 * 3, 180 * 2
display = pygame.display.set_mode((width, height), SCALED | FULLSCREEN)
clock = pygame.time.Clock()
delta_time = 0
ui_manager = gui.UIManager((width, height))
debug_box = gui.elements.UITextBox(
    "",
    Rect(0, 0, 200, 140),
    ui_manager
)


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

    def update(self):
        self.velocity += self.gravity * delta_time
        self.velocity = self.velocity.lerp(Vector2(), self.drag * delta_time)
        self.pos += self.velocity * delta_time

        self.size += self.size_per_second * delta_time

    def draw(self, world):
        pygame.draw.circle(display, self.colour, world.worldToScreenPosition(self.pos), self.size)


class ExpandingCircleParticle(Particle):
    def __init__(self, pos, target_radius, colour):
        super().__init__(pos, colour)
        self.radius = target_radius/2
        self.width = self.radius

        self.target_radius = target_radius
        self.target_width = 1

    def update(self):
        rad_spd = 4 * 100/self.target_radius
        wid_spd = rad_spd * 7/4

        self.radius = pygame.math.lerp(self.radius, self.target_radius, rad_spd * delta_time)
        self.width = pygame.math.lerp(self.width, self.target_width, wid_spd * delta_time)

        if self.width <= 1.5:
            self.kill = True

    def draw(self, world):
        pygame.draw.circle(display, self.colour, world.worldToScreenPosition(self.pos), self.radius, int(self.width))


class Chunk:
    def __init__(self, pos):
        self.pos = Vector2(pos)
        self.tiles = [[0 for y in range(int(CHUNK_SIZE.y))] for x in range(int(CHUNK_SIZE.x))]
        for i in range(5):
            self.tiles[
                random.randint(0, int(CHUNK_SIZE.x) - 1)
            ][
                random.randint(0, int(CHUNK_SIZE.y) - 1)
            ] = 1


class World:
    def __init__(self):
        self.chunks = {}
        self.local_chunks = []

        self.particles = []

        self.camera_position = Vector2(0, 0)
        self.real_camera_position = Vector2(0, 0)
        self.camera_position_offset = Vector2(0, 0)
        self.target_camera_position = Vector2(0, 0)

    def getMousePos(self):
        screen_pos = pygame.mouse.get_pos()
        world_pos = screen_pos + self.camera_position
        return world_pos

    @staticmethod
    def getChunkAtPos(pos):
        pos = Vector2(pos)
        chunk_pos_vec2 = pos - Vector2(
            pos.x % (CHUNK_SIZE.x * TILE_SIZE),
            pos.y % (CHUNK_SIZE.y * TILE_SIZE)
        )
        chunk_pos = (chunk_pos_vec2.x, chunk_pos_vec2.y)
        return chunk_pos

    def generateChunk(self, position):
        chunk_pos = self.getChunkAtPos(position)
        chunk = Chunk(chunk_pos)
        self.chunks[chunk_pos] = chunk
        return chunk

    def worldToScreenPosition(self, position):
        position = Vector2(position)
        screen_position = position - self.camera_position
        return screen_position

    def applyScreenshake(self, intensity=20):
        self.camera_position_offset += Vector2(
            random.randint(-intensity, intensity),
            random.randint(-intensity, intensity)
        )

    def update(self):
        keys = pygame.key.get_pressed()
        speed = 160*6
        lerp_speed = 10
        offset_lerp_speed = 10
        self.camera_position_offset = self.camera_position_offset.lerp(Vector2(), offset_lerp_speed * delta_time)
        self.target_camera_position.y -= delta_time * speed * (keys[K_w] - keys[K_s])
        self.target_camera_position.x -= delta_time * speed * (keys[K_a] - keys[K_d])
        self.real_camera_position = self.real_camera_position.lerp(self.target_camera_position,
                                                                   pygame.math.clamp(lerp_speed * delta_time, 0, 1))
        self.camera_position = self.real_camera_position + self.camera_position_offset

        for particle in self.particles:
            if particle.kill:
                self.particles.remove(particle)
                continue
            particle.update()

    def draw(self):
        chunk_positions = [  # positions to check for chunks at
            Vector2(0, 0),  # top left
            Vector2(width, 0),  # top right
            Vector2(width, height),  # bottom right
            Vector2(0, height),  # bottom left
            Vector2(width // 2, height // 2),  # centre
            Vector2(width // 2, 0),  # top middle
            Vector2(width // 2, height),  # bottom middle
            Vector2(0, height // 2),  # left middle
            Vector2(width, height // 2)  # right middle
        ]

        self.local_chunks = []

        for pos in chunk_positions:
            chunk_pos = self.getChunkAtPos(pos + self.camera_position)
            if chunk_pos in self.chunks:
                chunk = self.chunks[chunk_pos]
                if chunk in self.local_chunks:
                    continue
            else:
                chunk = self.generateChunk(chunk_pos)
            self.local_chunks.append(chunk)


        for chunk in self.local_chunks:
            for x, c in enumerate(chunk.tiles):
                for y, tile in enumerate(c):
                    pos = self.worldToScreenPosition(Vector2(x, y) * TILE_SIZE + chunk.pos)
                    if tile:
                        colour = "white"
                        pygame.draw.rect(display, colour, Rect(*pos, TILE_SIZE, TILE_SIZE))
            pygame.draw.rect(display, "red", Rect(self.worldToScreenPosition(chunk.pos), TILE_SIZE * CHUNK_SIZE), 1)

        for particle in self.particles:
            particle.draw(self)


world = World()

running = True
while running:

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                for i in range(20):
                    particle = Particle(
                        world.getMousePos()
                    )
                    particle.velocity = Vector2(
                        random.randint(-20, 20),
                        random.randint(-20, 20)
                    ) * 10
                    particle.colour = "white"
                    world.particles.append(particle)

    display.fill("black")

    world.update()
    world.draw()

    debug_box.set_text(f"FPS: {round(clock.get_fps(), 2)} <br>delta: {delta_time} <br>local chunks: "
                       f"{len(world.local_chunks)} <br>pos: {round(world.camera_position, 2)}")

    ui_manager.update(delta_time)
    ui_manager.draw_ui(display)

    pygame.display.flip()

    delta_time = pygame.math.clamp(clock.tick(FPS) / 1000, 0, 1)

pygame.quit()
