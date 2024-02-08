import pygame


def linecast(start_pos, direction, distance, collidable_objects, distance_threshold=1) -> tuple[pygame.Vector2, list]:
    direction.normalize_ip()
    pos = pygame.Vector2(start_pos)
    distance_marched = 0

    collided_objects = []

    is_marching = True
    while is_marching:
        circle_collider = pygame.geometry.Circle(pos, distance)
        final_collision = False
        for c in collidable_objects:
            while circle_collider.colliderect(c.rect):
                circle_collider.radius /= 2
                if circle_collider.radius <= distance_threshold:
                    final_collision = True
                    collided_objects.append(c)
                    break
        pos += direction * circle_collider.radius
        distance_marched += circle_collider.radius
        if distance_marched >= distance - distance_threshold or final_collision:
            is_marching = False
            if (pos - start_pos).magnitude() > distance:
                pos -= start_pos
                pos.normalize_ip()
                pos *= distance
                pos += start_pos
    return pos, collided_objects
