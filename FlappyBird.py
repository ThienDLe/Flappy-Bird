import pygame
import sys
import random
pygame.init()
clock = pygame.time.Clock()

# -------------
# CONSTANT VARS
# -------------
WIN_WIDTH, WIN_HEIGHT = 500, 789
FPS = 60
VEL = 5
PIPE_HEIGHT = [150, 250, 350, 450, 550, 650]
PIPE_GAP = 200
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))


# -----------
# IMPORT IMGS
# -----------
BACKGROUND_SURFACE = pygame.transform.scale2x(pygame.image.load(
    '/Users/lethien/Desktop/Projects/Flappy Bird by AI with NEAT/Flappy Bird/assets/background-day.png').convert())
BIRD_SURFACE = pygame.transform.scale2x(pygame.image.load(
    '/Users/lethien/Desktop/Projects/Flappy Bird by AI with NEAT/Flappy Bird/assets/bluebird-midflap.png').convert())
BASE_SURFACE = pygame.transform.scale2x(pygame.image.load(
    '/Users/lethien/Desktop/Projects/Flappy Bird by AI with NEAT/Flappy Bird/assets/base.png').convert())
PIPE_SURFACE = pygame.transform.scale2x(pygame.image.load(
    '/Users/lethien/Desktop/Projects/Flappy Bird by AI with NEAT/Flappy Bird/assets/pipe-green.png').convert())

# ---------
# FUNCTIONS
# ---------


def draw_base():
    WIN.blit(BASE_SURFACE, (base_pos_x, WIN_HEIGHT - 100))
    WIN.blit(BASE_SURFACE, (base_pos_x +
             BASE_SURFACE.get_width(), WIN_HEIGHT - 100))


def create_pipes():
    random_pipe_pos = random.choice(PIPE_HEIGHT)
    bottom_pipe = PIPE_SURFACE.get_rect(
        midbottom=(WIN_WIDTH + 100, random_pipe_pos - PIPE_GAP))
    top_pipe = PIPE_SURFACE.get_rect(
        midtop=(WIN_WIDTH + 100, random_pipe_pos))
    return bottom_pipe, top_pipe


def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= VEL
    return pipes


def draw_pipes(pipes):
    for pipe in pipes:
        WIN.blit(PIPE_SURFACE, pipe)


# ----------
# WHILE LOOP
# ----------
# Game variables:
base_pos_x = 0
gravity = 0.5
bird_movement = 0

bird_surface = BIRD_SURFACE
bird_rect = bird_surface.get_rect(center=(100, WIN_HEIGHT // 2 - 100))

pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1400)  # 1.4 second spawn time

# Loop:
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_movement = 0
                bird_movement -= 10

        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipes())

    # Background
    WIN.blit(BACKGROUND_SURFACE, (0, 0))

    # Bird
    bird_movement += gravity
    bird_rect.centery += bird_movement
    WIN.blit(bird_surface, bird_rect)

    # Pipes
    pipe_list = move_pipes(pipe_list)
    draw_pipes(pipe_list)

    # Base
    base_pos_x -= 1
    draw_base()
    if base_pos_x <= -BASE_SURFACE.get_width():
        base_pos_x = 0

    pygame.display.update()
    clock.tick(FPS)
