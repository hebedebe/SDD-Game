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
events = []
delta_time = 0
timescale = 1
ui_manager = gui.UIManager((width, height))
debug_box = gui.elements.UITextBox(
    "",
    Rect(0, 0, 225, 65),
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
        for i in range(3):
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
        keys = pygame.key.get_pressed()
        speed = 160*6
        lerp_speed = 10
        offset_lerp_speed = 10
        self.camera_position_offset = self.camera_position_offset.smoothstep(Vector2(), offset_lerp_speed * delta_time)
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

        pygame.draw.circle(display, "red", self.worldToScreenPosition(self.target_camera_position + Vector2(width, height)//2), 3)
        pygame.draw.circle(display, "green", self.worldToScreenPosition(self.real_camera_position + Vector2(width, height)//2), 3)


class Player:
    def __init__(self, pos):
        self.pos = Vector2(pos)
        self.velocity = Vector2()
        self.controlled_velocity = Vector2()
        self.acceleration = Vector2(0, 1200)
        self.jump_strength = -800
        self.speed = 200
        self.drag = 2
        self.ground_drag = 20
        self.on_ground = False
        self.width = 16
        self.height = 32

        self.mouse_direction = Vector2

    def centre(self):
        return self.pos + Vector2(self.width, self.height)/2

    def update(self, delta_time, world):
        keys = pygame.key.get_pressed()

        self.controlled_velocity.x = (keys[K_d] - keys[K_a]) * self.speed
        self.velocity += self.acceleration * delta_time

        self.on_ground = False
        self.pos.x += (self.velocity.x + self.controlled_velocity.x) * delta_time
        self.check_collision(Vector2(self.velocity.x + self.controlled_velocity.x, 0), world)
        self.pos.y += (self.velocity.y + self.controlled_velocity.y) * delta_time
        self.check_collision(Vector2(0, self.velocity.y + self.controlled_velocity.y), world)

        self.velocity -= self.velocity * (self.ground_drag if self.on_ground else self.drag) * delta_time

        world.target_camera_position = self.pos - Vector2(width//2 - self.width//2, height//2 - self.height//2)

        self.mouse_direction = (world.getMousePos() - self.centre()).normalize()

        for event in events:
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.velocity += 1000 * self.mouse_direction
                    world.applyScreenshake(10)
                    world.particles.append(
                        ExpandingCircleParticle(
                            self.centre(),
                            40,
                            "yellow"
                        )
                    )

        if keys[K_w] and self.on_ground:
            self.velocity.y = self.jump_strength
            world.applyScreenshake(4)

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
                                self.velocity.y = 0
                                self.controlled_velocity.y = 0
                                self.on_ground = True
                            elif velocity.y < 0:
                                self.pos.y = tile_rect.bottom
                                self.velocity.y = 0
                                self.controlled_velocity.y = 0
                            elif velocity.x > 0:
                                self.pos.x = tile_rect.left - self.width
                                self.velocity.x = 0
                            elif velocity.x < 0:
                                self.pos.x = tile_rect.right
                                self.velocity.x = 0


    def draw(self, world):
        pygame.draw.rect(display, "blue", pygame.Rect(world.worldToScreenPosition(self.pos), (self.width, self.height)))
        pygame.draw.line(display, "yellow", world.worldToScreenPosition(self.centre() + self.mouse_direction * 20), world.worldToScreenPosition(self.centre() + self.mouse_direction * 65), 3)


def main():
    global delta_time, events
    world = World()
    player = Player((width // 2, height // 2))
    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == QUIT:
                running = False
            ui_manager.process_events(event)

        display.fill("black")

        player.update(delta_time, world)
        player.draw(world)

        world.update()
        world.draw()

        debug_box.set_text(f"FPS: {round(clock.get_fps(), 2)} <br> Altitude: {-round(player.pos.y/10, 2)}m")

        ui_manager.update(delta_time)
        ui_manager.draw_ui(display)

        pygame.display.flip()

        delta_time = pygame.math.clamp(clock.tick(FPS) / 1000, 0, 1) * timescale

    pygame.quit()

main()