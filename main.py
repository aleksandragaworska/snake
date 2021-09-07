import pygame
from random import randrange

pygame.init()

width = 800
length = 800

x = width / 2
y = length / 2

step = 10


window = pygame.display.set_mode(size=(width, length))

run = True

deepskyblue = (0, 191, 255)
springgreen = (0, 255, 127)
red = (255, 0, 0)
blue = (50, 153, 213)
color = deepskyblue

need_new_apple = True

clock = pygame.time.Clock()


def get_new_apple():
    apple_x = round(randrange(step, width - step) / step) * step
    apple_y = round(randrange(step, length - step) / step) * step
    return apple_x, apple_y


start_snake_lenght = 25
snake_body = [(x, y)]
for i in range(start_snake_lenght - 1, 0, -1):
    snake_body.append([x, y + step * i])

snake_len = start_snake_lenght

current_direction = None
direction = None
x_changed = 0
y_changed = 0


def draw_snake_body(snake_body):
    for x, y in snake_body:
        pygame.draw.circle(surface=window, color=color, radius=10, center=(x, y))


def get_real_direction_and_changed(current_direction, direction, x_changed, y_changed):
    if current_direction == 'left' and direction == 'right':
        return -step, 0, current_direction
    if current_direction == 'right' and direction == 'left':
        return step, 0, current_direction
    if current_direction == 'up' and direction == 'down':
        return 0, -step, current_direction
    if current_direction == 'down' and direction == 'up':
        return 0, step, current_direction
    return x_changed, y_changed, direction


def get_changes_snake_head_position(x_old, y_old, x_changed, y_changed):
    if x_old + x_changed < step or x_old + x_changed > width - step:
        return x_old, y_old + y_changed
    if y_old + y_changed < step or y_old + y_changed > length - step:
        return x_old + x_changed, y_old
    return x_old + x_changed, y_old + y_changed


score_font = pygame.font.SysFont("comicsansms", int(width / 20))
end_game = False

while run:
    pygame.time.delay(50)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    while end_game:
        window.fill(blue)
        value = score_font.render(f"Your Score: {snake_len - start_snake_lenght}", True, springgreen)
        window.blit(value, [0, 0])
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end_game = False
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

    if current_direction is None:
        current_direction = direction

    x_changed, y_changed, direction = get_real_direction_and_changed(current_direction, direction, x_changed, y_changed)

    x, y = get_changes_snake_head_position(x, y, x_changed, y_changed)

    current_direction = direction

    if (x, y) != snake_body[-1]:
        snake_body.append((x, y))

    snake_head = snake_body[-1]

    if snake_len > 1 and snake_head in snake_body[-snake_len:-1]:
        end_game = True

    for n in range(1, snake_len + 1):
        draw_snake_body(snake_body[-n:])

    if need_new_apple:
        need_new_apple = False
        apple_x, apple_y = get_new_apple()
    if apple_x == x and apple_y == y:
        need_new_apple = True
        snake_len += 1
        print('Yummy!')
    pygame.draw.circle(surface=window, color=red, radius=10, center=(apple_x, apple_y))
    score_text = score_font.render(f"Your Score: {snake_len - start_snake_lenght}", True, springgreen)
    window.blit(score_text, [0, 0])
    pygame.display.update()
    clock.tick(30)
