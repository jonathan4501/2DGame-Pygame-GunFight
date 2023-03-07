import pygame
import os
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1000, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gun Fight")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 238)

BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

HEALTH_FONT = pygame.font.SysFont('comiscans', 40)
WINNER_FONT = pygame.font.SysFont('comiscans', 100)

FPS = 60
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 5
GUN_WIDTH, GUN_HEIGHT = 55, 40

BLUE_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

BLUE_GUN_IMAGE = pygame.image.load(
    os.path.join('Tools', 'BlueGun.png'))
BLUE_GUN = pygame.transform.rotate(pygame.transform.scale(
    BLUE_GUN_IMAGE, (GUN_WIDTH, GUN_HEIGHT)), 0)

RED_GUN_IMAGE = pygame.image.load(
    os.path.join('Tools', 'RedGun.png'))
RED_GUN = pygame.transform.rotate(pygame.transform.scale(
    RED_GUN_IMAGE, (GUN_WIDTH, GUN_HEIGHT)), 0)

WALLPAPER = pygame.transform.scale(pygame.image.load(
    os.path.join('Tools', 'wallpaper.png')), (WIDTH, HEIGHT))


def draw_window(red, blue, red_bullets, blue_bullets, red_health, blue_health):
    WIN.blit(WALLPAPER, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    red_health_text = HEALTH_FONT.render(
        "Health: " + str(red_health), 1, WHITE)
    blue_health_text = HEALTH_FONT.render(
        "Health: " + str(blue_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(blue_health_text, (10, 10))

    WIN.blit(BLUE_GUN, (blue.x, blue.y))
    WIN.blit(RED_GUN, (red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in blue_bullets:
        pygame.draw.rect(WIN, BLUE, bullet)

    pygame.display.update()


def blue_handle_movement(keys_pressed, blue):
    if keys_pressed[pygame.K_a] and blue.x - VEL > 0:  # LEFT
        blue.x -= VEL
    if keys_pressed[pygame.K_d] and blue.x + VEL + blue.width < BORDER.x:  # RIGHT
        blue.x += VEL
    if keys_pressed[pygame.K_w] and blue.y - VEL > 0:  # UP
        blue.y -= VEL
    if keys_pressed[pygame.K_s] and blue.y + VEL + blue.height < HEIGHT - 15:  # DOWN
        blue.y += VEL


def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width:  # LEFT
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH:  # RIGHT
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0:  # UP
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 15:  # DOWN
        red.y += VEL


def handle_bullets(blue_bullets, red_bullets, blue, red):
    for bullet in blue_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            blue_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            blue_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if blue.colliderect(bullet):
            pygame.event.post(pygame.event.Event(BLUE_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() /
                         2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)


def main():
    red = pygame.Rect(700, 300, GUN_WIDTH, GUN_HEIGHT)
    blue = pygame.Rect(100, 300, GUN_WIDTH, GUN_HEIGHT)

    red_bullets = []
    blue_bullets = []

    red_health = 15
    blue_health = 15

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            print(type(event))
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(blue_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        blue.x + blue.width, blue.y + blue.height//2 - 2, 10, 5)
                    blue_bullets.append(bullet)
                    # BULLET_FIRE_SOUND.play()
                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        red.x, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    # BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 1
                # BULLET_HIT_SOUND.play()
            if event.type == BLUE_HIT:
                blue_health -= 1
                # BULLET_HIT_SOUND.play()

        winner_text = ""
        if red_health <= 0:
            winner_text = "Blue Wins !!!"

        if blue_health <= 0:
            winner_text = "Red Wins !!!"

        if winner_text != "":
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        blue_handle_movement(keys_pressed, blue)
        red_handle_movement(keys_pressed, red)

        handle_bullets(blue_bullets, red_bullets, blue, red)

        draw_window(red, blue, red_bullets, blue_bullets,
                    red_health, blue_health)


if __name__ == "__main__":
    main()
