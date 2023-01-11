import pygame
from sys import exit


def display_score():
    current_time = pygame.time.get_ticks()
    score = int((current_time - game_time) / 1000)
    score_screen = font.render(f"SCORE - {score}", False, (64, 64, 64))
    score_rect = score_screen.get_rect(midbottom=(400, 50))
    screen.blit(score_screen, score_rect)


def game_start_score(end_time):
    score = int((end_time - game_time) / 1000)
    score_screen = font.render(f"SCORE - {score}", False, (145, 150, 235))
    score_rect = score_screen.get_rect(midbottom=(400, 300))
    screen.blit(score_screen, score_rect)


pygame.init()
screen = pygame.display.set_mode((800, 400))
game_active = True

# Basic layout of the game
pygame.display.set_caption("Runner")
clock = pygame.time.Clock()
time = int(pygame.time.get_ticks())
game_time = 0
font = pygame.font.Font("resources/font/Pixeltype.ttf", 40)

# Import the resources
sky_screen = pygame.image.load("resources/graphics/Sky.png").convert()
ground_screen = pygame.image.load("resources/graphics/ground.png").convert()
snail_surface = pygame.image.load("resources/graphics/snail/snail1.png").convert_alpha()

player_surface = pygame.image.load(
    "resources/graphics/Player/player_walk_1.png"
).convert_alpha()

game_start_player_surface = pygame.image.load(
    "resources/graphics/Player/player_stand.png"
).convert_alpha()

# Enemies
snail_x_position = 800
snail_rect = snail_surface.get_rect(midbottom=(snail_x_position, 300))

# Player
player_rect = player_surface.get_rect(midbottom=(60, 300))
player_gravity = 0


# Game continous loop
while True:
    # Event Loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos) and player_rect.bottom == 300:
                    player_gravity = -20

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom == 300:
                    player_gravity = -20
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                snail_rect.left = 800
                game_time = int(pygame.time.get_ticks())

    # Game pause and play states
    if game_active:

        # Screen rendering
        screen.blit(sky_screen, (0, 0))
        screen.blit(ground_screen, (0, 300))
        screen.blit(snail_surface, snail_rect)
        screen.blit(player_surface, player_rect)

        display_score()

        # Update Movement (Enemies)
        snail_rect.left -= 4
        if snail_rect.right <= 0:
            snail_rect.left = 800

        # Update Movement (player)
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom > 300:
            player_rect.bottom = 300

        # Key Map
        keys = pygame.key.get_pressed()

        # Collisions
        collision = player_rect.colliderect(snail_rect)
        if snail_rect.colliderect(player_rect):
            game_active = False
            end_time = pygame.time.get_ticks()

    else:
        screen.fill((72, 80, 232))

        game_start_title = font.render(f"Speed Runner", False, (145, 150, 235))
        game_start_title_rect = game_start_title.get_rect(midbottom=(400, 50))

        game_start_player_surface_rect = game_start_player_surface.get_rect(
            midbottom=(400, 200)
        )

        game_start_score(end_time)

        game_start_hint = font.render(f"Press Space to Begin", False, (145, 150, 235))
        game_start_hint_rect = game_start_hint.get_rect(midbottom=(400, 350))

        screen.blit(game_start_title, game_start_title_rect)
        screen.blit(game_start_hint, game_start_hint_rect)
        screen.blit(game_start_player_surface, game_start_player_surface_rect)

    pygame.display.update()
    clock.tick(60)
