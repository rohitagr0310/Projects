import pygame
from sys import exit
from random import randint


def display_score():
    current_time = pygame.time.get_ticks()
    score = int((current_time - game_time) / 1000)
    score_screen = font.render(f"SCORE - {score}", False, (64, 64, 64))
    score_rect = score_screen.get_rect(midbottom=(400, 50))
    screen.blit(score_screen, score_rect)

    return score


def enemy_movement(enemy_list):
    if enemy_list:
        for enemy_rect in enemy_list:
            enemy_rect.x -= 5

            if enemy_rect.bottom == 300:
                screen.blit(snail_surface, enemy_rect)
            else:
                screen.blit(fly_surface, enemy_rect)

        enemy_list = [enemy for enemy in enemy_list if enemy.x > -100]
        return enemy_list
    else:
        return []


def collision(player, enemys):
    if enemys:
        for enemy_rect in enemys:
            if player.colliderect(enemy_rect):
                return False
    return True


def player_animation():
    global player_surface, player_index

    if player_rect.bottom < 300:
        # display the jump surf when player is not on floor
        player_surface = player_jump
    else:
        # play walking animation if the player is on the floor
        player_index += 0.1
        if player_index >= len(player_walk):
            player_index = 0

        player_surface = player_walk[int(player_index)]


pygame.init()
screen = pygame.display.set_mode((800, 400))
game_active = False

# Basic layout of the game
pygame.display.set_caption("Runner")
clock = pygame.time.Clock()
time = int(pygame.time.get_ticks())
game_time = 0
font = pygame.font.Font("resources/font/Pixeltype.ttf", 40)
score = 0

# Import the resources
sky_screen = pygame.image.load("resources/graphics/Sky.png").convert()
ground_screen = pygame.image.load("resources/graphics/ground.png").convert()

snail_surface = pygame.image.load("resources/graphics/snail/snail1.png").convert_alpha()
fly_surface = pygame.image.load("resources/graphics/Fly/Fly1.png").convert_alpha()

player_walk_1 = pygame.image.load(
    "resources/graphics/Player/player_walk_1.png"
).convert_alpha()
player_walk_2 = pygame.image.load(
    "resources/graphics/Player/player_walk_2.png"
).convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_index = 0

player_jump = pygame.image.load("resources/graphics/Player/jump.png").convert_alpha()

game_start_player_surface = pygame.image.load(
    "resources/graphics/Player/player_stand.png"
).convert_alpha()

# Enemies list -
enemy_rect_list = []

# Player
player_surface = player_walk[player_index]
player_rect = player_surface.get_rect(midbottom=(80, 300))
player_gravity = 0

# Timer
enemy_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_timer, 1500)

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
                game_time = int(pygame.time.get_ticks())

        # Game obstacle timer
        if event.type == enemy_timer and game_active:
            if randint(0, 2):
                enemy_rect_list.append(
                    snail_surface.get_rect(bottomright=(randint(900, 1100), 300))
                )
            else:
                enemy_rect_list.append(
                    fly_surface.get_rect(bottomright=(randint(900, 1100), 210))
                )

    # Game pause and play states
    if game_active:

        # Screen rendering
        screen.blit(sky_screen, (0, 0))
        screen.blit(ground_screen, (0, 300))
        player_animation()
        screen.blit(player_surface, player_rect)

        score = display_score()

        # Update Movement (player)
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom > 300:
            player_rect.bottom = 300

        # Update Enemy Movement
        enemy_rect_list = enemy_movement(enemy_rect_list)

        game_active = collision(player_rect, enemy_rect_list)

    else:
        screen.fill((72, 80, 232))

        game_start_title = font.render(f"Speed Runner", False, (145, 150, 235))
        game_start_title_rect = game_start_title.get_rect(midbottom=(400, 50))

        game_start_player_surface_rect = game_start_player_surface.get_rect(
            midbottom=(400, 200)
        )

        score_screen = font.render(f"SCORE - {score}", False, (145, 150, 235))
        score_rect = score_screen.get_rect(midbottom=(400, 300))
        screen.blit(score_screen, score_rect)

        enemy_rect_list.clear()
        player_rect.midbottom = (80, 300)
        player_gravity = 0

        game_start_hint = font.render(f"Press Space to Begin", False, (145, 150, 235))
        game_start_hint_rect = game_start_hint.get_rect(midbottom=(400, 350))

        screen.blit(game_start_title, game_start_title_rect)
        screen.blit(game_start_hint, game_start_hint_rect)
        screen.blit(game_start_player_surface, game_start_player_surface_rect)

    pygame.display.update()
    clock.tick(60)
