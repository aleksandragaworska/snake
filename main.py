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
    apple_x = round(randrange(0, width - step) / step) * step
    apple_y = round(randrange(0, length - step) / step) * step
    return apple_x, apple_y


snake_body = []
snake_len = 1


def draw_snake_body(snake_body):
    for x, y in snake_body:
        pygame.draw.circle(surface=window, color=color, radius=10, center=(x, y))


snake_moved = False

while run:
    pygame.time.delay(50)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        if x > step:
            x -= step
            snake_moved = True
    if keys[pygame.K_RIGHT]:
        if x < width - step:
            x += step
            snake_moved = True
    if keys[pygame.K_UP]:
        if y > step:
            y -= step
            snake_moved = True
    if keys[pygame.K_DOWN]:
        if y < length - step:
            y += step
            snake_moved = True
    if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
        color = springgreen
    if keys[pygame.K_RSHIFT]:
        color = deepskyblue
    window.fill((0, 0, 0))

    if len(snake_body) == 0 or (x, y) != snake_body[0]:
        snake_body.append((x, y))

    draw_snake_body(snake_body[-snake_len:])

    if need_new_apple:
        need_new_apple = False
        apple_x, apple_y = get_new_apple()
    pygame.draw.circle(surface=window, color=color, radius=10, center=(x, y))
    if apple_x == x and apple_y == y:
        need_new_apple = True
        snake_len += 1
        print('Yummy!')
    pygame.draw.circle(surface=window, color=red, radius=10, center=(apple_x, apple_y))
    clock.tick(30)
    pygame.display.update()
