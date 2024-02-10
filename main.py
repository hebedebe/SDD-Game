import pygame
from pygame.locals import *

import pygame_gui as gui

import random

import particles
from assetloader import Assets
from particles import Particle, ExpandingCircleParticle
import util
from constants import *

pygame.init()

display = pygame.display.set_mode((WIDTH, HEIGHT), SCALED | FULLSCREEN)

clock = pygame.time.Clock()

events = []

delta_time = 0
timescale = 1

assets = Assets()

ui_manager = gui.UIManager((WIDTH, HEIGHT))
debug_box = gui.elements.UITextBox(
    "",
    Rect(0, 0, 120, 30),
    ui_manager
)


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
        self.entities = []

        self.particles = set()

        self.camera_position = Vector2(0, 0)
        self.real_camera_position = Vector2(0, 0)
        self.camera_position_offset = Vector2(0, 0)
        self.target_camera_position = Vector2(0, 0)

    def addParticle(self, particle):
        self.particles.add(particle)

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

    def getTileAtPos(self, pos):
        chunk_pos = self.getChunkAtPos(pos)
        chunk = self.chunks[chunk_pos]
        remainder_vec2 = (pos - chunk_pos) // TILE_SIZE
        remainder = (remainder_vec2.x, remainder_vec2.y)
        tile = chunk.tiles[remainder]
        return tile

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
        lerp_speed = 10
        offset_lerp_speed = 50
        self.camera_position_offset = self.camera_position_offset.smoothstep(Vector2(), offset_lerp_speed * delta_time)
        self.real_camera_position = self.real_camera_position.lerp(self.target_camera_position,
                                                                   pygame.math.clamp(lerp_speed * delta_time, 0, 1))
        self.camera_position = self.real_camera_position + self.camera_position_offset

        particles_to_kill = set()
        for particle in self.particles:
            if particle.kill:
                particles_to_kill.add(particle)
                continue
            particle.update(delta_time)

        for particle in particles_to_kill:
            self.particles.remove(particle)

    def draw(self):
        chunk_positions = [  # positions to check for chunks at
            Vector2(0, 0),  # top left
            Vector2(WIDTH, 0),  # top right
            Vector2(WIDTH, HEIGHT),  # bottom right
            Vector2(0, HEIGHT),  # bottom left
            Vector2(WIDTH // 2, HEIGHT // 2),  # centre
            Vector2(WIDTH // 2, 0),  # top middle
            Vector2(WIDTH // 2, HEIGHT),  # bottom middle
            Vector2(0, HEIGHT // 2),  # left middle
            Vector2(WIDTH, HEIGHT // 2)  # right middle
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

        pygame.draw.circle(display, "red",
                           self.worldToScreenPosition(self.target_camera_position + Vector2(WIDTH, HEIGHT) // 2), 3)
        pygame.draw.circle(display, "yellow",
                           self.worldToScreenPosition(self.camera_position + Vector2(WIDTH, HEIGHT) // 2), 3)
        pygame.draw.circle(display, "green",
                           self.worldToScreenPosition(self.real_camera_position + Vector2(WIDTH, HEIGHT) // 2), 3)

        display.blit(assets.get("border_left"), (0, 0))
        display.blit(assets.get("border_right"), (420, 0))

    def drawParticles(self):
        for particle in self.particles:
            particle.draw(display, self)


class Player:
    def __init__(self, pos):
        self.pos = Vector2(pos)
        self.velocity = Vector2()
        self.controlled_velocity = Vector2()

        self.gravity = Vector2(0, 1600)

        self.drag = 2
        self.drag_on_ground = 20

        self.jump_strength = -800
        self.speed = 200
        self.boost_distance = 100

        self.on_ground = False

        self.width = 16
        self.height = 32

        self.health = 100

        self.mouse_direction = Vector2

    def centre(self):
        return self.pos + Vector2(self.width, self.height) / 2

    def getVelocity(self):
        return self.velocity + self.controlled_velocity

    def getCurrentDrag(self):
        return self.drag_on_ground if self.on_ground else self.drag

    def resetVelocity(self, x=False, y=False):
        if x:
            self.velocity.x = 0
            self.controlled_velocity.x = 0
        if y:
            self.velocity.y = 0
            self.controlled_velocity.y = 0

    def update(self, delta_time, world):
        keys = pygame.key.get_pressed()

        self.controlled_velocity.x = (keys[K_d] - keys[K_a]) * self.speed

        if keys[K_d] and self.velocity.x < 0:
            self.velocity.x *= -1
        if keys[K_a] and self.velocity.x > 0:
            self.velocity.x *= -1

        self.velocity += self.gravity * delta_time

        self.velocity -= self.velocity * self.getCurrentDrag() * delta_time

        self.on_ground = False
        velocity = self.getVelocity()
        self.pos.x += velocity.x * delta_time
        self.check_collision(Vector2(velocity.x, 0), world)
        self.pos.y += velocity.y * delta_time
        self.check_collision(Vector2(0, velocity.y), world)

        world.target_camera_position = self.pos - Vector2(WIDTH // 2 - self.width // 2, HEIGHT // 2 - self.height // 2)

        self.mouse_direction = (world.getMousePos() - self.centre()).normalize()

        for event in events:
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.velocity.y = 0
                    self.velocity += 1000 * self.mouse_direction

                    direction = self.getVelocity().normalize()

                    world.addParticle(
                        particles.Spark(
                            self.centre(),
                            100,
                            direction,
                            "white"
                        )
                    )

                    world.applyScreenshake(15)
                    particles.worldEmitCircle(
                        world,
                        self.centre(),
                        10,
                        "white",
                        180,
                        200,
                    )
                    world.addParticle(
                        ExpandingCircleParticle(
                            self.centre() + Vector2(0, self.width // 2),
                            40,
                            "yellow"
                        )
                    )

        if keys[K_w] and self.on_ground:
            self.velocity.y = self.jump_strength

    def check_collision(self, velocity, world):
        player_rect = pygame.Rect(self.pos.x, self.pos.y, self.width, self.height)
        for chunk in world.local_chunks:
            if type(chunk) is tuple:
                continue
            for x in range(int(CHUNK_SIZE.x)):
                for y in range(int(CHUNK_SIZE.y)):
                    if chunk.tiles[x][y]:
                        tile_rect = pygame.Rect(chunk.pos.x + x * TILE_SIZE, chunk.pos.y + y * TILE_SIZE, TILE_SIZE,
                                                TILE_SIZE)
                        if player_rect.colliderect(tile_rect):
                            if velocity.y > 0:
                                self.pos.y = tile_rect.top - self.height
                                self.resetVelocity(y=True)
                                self.on_ground = True
                            elif velocity.y < 0:
                                self.pos.y = tile_rect.bottom
                                self.resetVelocity(y=True)
                            elif velocity.x > 0:
                                self.pos.x = tile_rect.left - self.width
                                self.resetVelocity(x=True)
                            elif velocity.x < 0:
                                self.pos.x = tile_rect.right
                                self.resetVelocity(x=True)

    def draw(self, world):
        pygame.draw.rect(display, "blue", pygame.Rect(world.worldToScreenPosition(self.pos), (self.width, self.height)))
        pygame.draw.line(display, "yellow", world.worldToScreenPosition(self.centre() + self.mouse_direction * 20),
                         world.worldToScreenPosition(self.centre() + self.mouse_direction * 65), 3)


def main():
    global delta_time, events
    world = World()
    player = Player((WIDTH // 2, HEIGHT // 2))
    player_health_fade = 100
    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == QUIT:
                running = False
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    player.health -= 20

        display.fill("black")

        player.update(delta_time, world)
        player.draw(world)

        world.update()
        world.draw()

        debug_box.set_text(f"FPS: {round(clock.get_fps(), 2)}")

        health_bar_pos = Vector2(0, HEIGHT-32)
        if player.health > 0:
            player_health_fade = pygame.math.lerp(player_health_fade, player.health, delta_time * 5)
            pygame.draw.line(display, HEALTH_BAR_SUB_COLOUR,
                             health_bar_pos + [14, 15],
                             health_bar_pos + [14 + player_health_fade, 15],
                             13
                             )
            pygame.draw.line(display, HEALTH_BAR_COLOUR,
                             health_bar_pos + [14, 15],
                             health_bar_pos + [14 + player.health, 15],
                             13
                             )
        display.blit(assets.get("bar_outline"), health_bar_pos)

        ui_manager.update(delta_time)
        ui_manager.draw_ui(display)

        world.drawParticles()

        pygame.display.flip()

        delta_time = pygame.math.clamp(clock.tick(FPS) / 1000, 0, 1) * timescale

    pygame.quit()


main()
