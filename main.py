import pygame
from random import randrange
from dataclasses import dataclass
from typing import Tuple


@dataclass
class Color:
    deepskyblue: Tuple[int] = (0, 191, 255)
    springgreen: Tuple[int] = (0, 255, 127)
    red: Tuple[int] = (255, 0, 0)
    white: Tuple[int] = (128, 128, 128)
    blue: Tuple[int] = (50, 153, 213)


@dataclass
class Config:
    run: bool = True
    width: int = 800
    length: int = 800
    x: int = width / 2
    y: int = length / 2
    step: int = 20
    need_new_apple: bool = True
    end_game: bool = False
    restart_game: bool = False
    current_direction: str = 'up'
    x_changed: int = 0
    y_changed: int = -step
    direction: str = 'up'
    start_snake_lenght: int = 25
    snake_len: int = start_snake_lenght
    default_color: Color = Color.deepskyblue


def get_new_apple(config):
    apple_x = round(randrange(config.step, config.width - config.step) / config.step) * config.step
    apple_y = round(randrange(config.step, config.length - config.step) / config.step) * config.step
    return apple_x, apple_y


def get_start_snake(config):
    snake_body = []
    for i in range(config.start_snake_lenght - 1, 0, -1):
        snake_body.append((config.x, config.y + config.step * i))
    snake_body.append((config.x, config.y))
    return snake_body


def draw_grade(window, config, color):
    block = config.step
    for x in range(0, config.width, block):
        for y in range(0, config.length, block):
            rect = pygame.Rect(x, y, block, block)
            pygame.draw.rect(window, color.white, rect, 1)


def draw_snake_body(window, snake_body, config):
    for x, y in snake_body:
        point_list = [
            (x + config.step / 4, y),
            (x + 3 * config.step / 4, y),
            (x + config.step, y + config.step / 4),
            (x + config.step, y + 3 * config.step / 4),
            (x + 3 * config.step / 4, y + config.step),
            (x + config.step / 4, y + config.step),
            (x, y + 3 * config.step / 4),
            (x, y + config.step / 4)

        ]
        pygame.draw.polygon(window, config.default_color, point_list)


def get_direction_and_changed(config):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        config.x_changed = -config.step
        config.y_changed = 0
        config.direction = 'left'
    elif keys[pygame.K_RIGHT]:
        config.x_changed = config.step
        config.y_changed = 0
        config.direction = 'right'
    elif keys[pygame.K_UP]:
        config.x_changed = 0
        config.y_changed = -config.step
        config.direction = 'up'
    elif keys[pygame.K_DOWN]:
        config.x_changed = 0
        config.y_changed = config.step
        config.direction = 'down'
    return config.x_changed, config.y_changed, config.direction


def get_real_direction_and_changed(config):
    if config.current_direction == 'left' and config.direction == 'right':
        return -config.step, 0, config.current_direction
    if config.current_direction == 'right' and config.direction == 'left':
        return config.step, 0, config.current_direction
    if config.current_direction == 'up' and config.direction == 'down':
        return 0, -config.step, config.current_direction
    if config.current_direction == 'down' and config.direction == 'up':
        return 0, config.step, config.current_direction
    return config.x_changed, config.y_changed, config.direction


def get_changes_snake_head_position(config):
    if config.x + config.x_changed < config.step:
        return config.width - config.step, config.y + config.y_changed
    if config.x + config.x_changed > config.width - config.step:
        return config.step, config.y + config.y_changed
    if config.y + config.y_changed < config.step:
        return config.x + config.x_changed, config.length - config.step
    if config.y + config.y_changed > config.length - config.step:
        return config.x + config.x_changed, config.step
    return config.x + config.x_changed, config.y + config.y_changed


def main():
    clock = pygame.time.Clock()
    color = Color()
    config = Config()

    window = pygame.display.set_mode(size=(config.width, config.length))

    game_over_font = pygame.font.SysFont("comicsansms", int(config.width / 10))
    score_font = pygame.font.SysFont("comicsansms", int(config.width / 20))

    snake_body = get_start_snake(config)

    while config.run:
        pygame.time.delay(80)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                config.run = False

        window.fill((0, 0, 0))
        draw_grade(window, config, color)

        while config.end_game:
            window.fill(color.blue)
            game_over = game_over_font.render(f"GAME OVER", True, color.red)
            final_score = score_font.render(f"Your Score: {config.snake_len - config.start_snake_lenght}", True, color.springgreen)
            try_again = score_font.render("Try again! Press SPACE", True, color.springgreen)
            window.blit(game_over, [config.width * 0.3, config.length * 0.35])
            window.blit(final_score, [config.width * 0.4, config.length * 0.45])
            window.blit(try_again, [config.width * 0.3, config.length * 0.50])
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    config.end_game = False
                    config.run = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        config = Config()
                        snake_body = get_start_snake(config)

        config.x_changed, config.y_changed, config.direction = get_direction_and_changed(config)

        config.x_changed, config.y_changed, config.direction = get_real_direction_and_changed(config)

        config.x, config.y = get_changes_snake_head_position(config)

        config.current_direction = config.direction

        if (config.x, config.y) != snake_body[-1]:
            snake_body.append((config.x, config.y))

        snake_head = snake_body[-1]

        if config.snake_len > 1 and snake_head in snake_body[-config.snake_len:-1]:
            config.end_game = True

        for n in range(1, config.snake_len + 1):
            draw_snake_body(window, snake_body[-n:], config)

        if config.need_new_apple:
            config.need_new_apple = False
            apple_x, apple_y = get_new_apple(config)
        if apple_x == config.x and apple_y == config.y:
            config.need_new_apple = True
            config.snake_len += 1
        pygame.draw.circle(surface=window, color=color.red, radius=config.step / 2, center=(apple_x + config.step / 2, apple_y + config.step / 2))
        score_text = score_font.render(f"Your Score: {config.snake_len - config.start_snake_lenght}", True, color.springgreen)
        window.blit(score_text, [0, 0])
        pygame.display.update()
        clock.tick(30)


if __name__ == '__main__':
    pygame.init()
    main()
