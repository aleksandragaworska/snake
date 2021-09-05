import pygame
from random import randrange

pygame.init()

width = 800
length = 800

x = length / 2
y = width / 2

step = 10

window = pygame.display.set_mode(size=(width, length))

run = True

deepskyblue = (0, 191, 255)
springgreen = (0, 255, 127)
red = (255, 0, 0)
color = deepskyblue

need_new_apple = True

clock = pygame.time.Clock()


def get_new_apple():
    apple_x = round(randrange(step, width - step) / step) * step
    apple_y = round(randrange(step, length - step) / step) * step
    return apple_x, apple_y


snake_body = []
snake_len = 1

current_direction = None
direction = None
x_changed = 0
y_changed = 0


def draw_snake_body(snake_body):
    for x, y in snake_body:
        pygame.draw.circle(surface=window, color=color, radius=10, center=(x, y))


def can_change_direction(current_direction, direction):
    if not current_direction or not direction or (current_direction == direction):
        return True, True
    if current_direction == 'left' and direction == 'right':
        return False, True
    if current_direction == 'right' and direction == 'left':
        return False, True
    if current_direction == 'up' and direction == 'down':
        return True, False
    if current_direction == 'down' and direction == 'up':
        return True, False
    return True, True


def get_changes_snake_head_position(x_old, y_old, current_direction, x_changed, y_changed, direction):
    if not current_direction:
        current_direction = direction
    can_change_x, can_change_y = can_change_direction(current_direction, direction)
    if can_change_x and not can_change_y:
        return x_old + x_changed, y_old, direction
    if not can_change_x and can_change_y:
        return x_old, y_old + y_changed, direction
    if not can_change_x and not can_change_y:
        return x_old, y_old, current_direction
    if direction == 'left' and x_old <= step:
        return x_old, y_old + y_changed, direction
    if direction == 'right' and x_old >= width - step:
        return x_old, y_old + y_changed, direction
    if direction == 'up' and y_old <= step:
        return x_old + x_changed, y_old, direction
    if direction == 'down' and y_old >= width - step:
        return x_old + x_changed, y_old, direction

    return x_old + x_changed, y_old + y_changed, direction


while run:
    pygame.time.delay(50)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        x_changed = -step
        y_changed = 0
        direction = 'left'
    elif keys[pygame.K_RIGHT]:
        x_changed = step
        y_changed = 0
        direction = 'right'
    elif keys[pygame.K_UP]:
        x_changed = 0
        y_changed = -step
        direction = 'up'
    elif keys[pygame.K_DOWN]:
        x_changed = 0
        y_changed = step
        direction = 'down'
    window.fill((0, 0, 0))

    x, y, current_direction = get_changes_snake_head_position(x, y, current_direction, x_changed, y_changed, direction)

    if len(snake_body) == 0 or (x, y) != snake_body[-1]:
        snake_body.append((x, y))

    for n in range(1, snake_len + 1):
        draw_snake_body(snake_body[-n:])

    if need_new_apple:
        need_new_apple = False
        apple_x, apple_y = get_new_apple()
    pygame.draw.circle(surface=window, color=color, radius=10, center=(x, y))
    if apple_x == x and apple_y == y:
        need_new_apple = True
        snake_len += 1
        print('Yummy!')
    pygame.draw.circle(surface=window, color=red, radius=10, center=(apple_x, apple_y))
    pygame.display.update()
    clock.tick(30)
