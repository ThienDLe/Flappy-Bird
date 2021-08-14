import pygame
import sys
import random
pygame.mixer.init(44100, -16, 2, 64)
pygame.init()
clock = pygame.time.Clock()

# -------------
# CONSTANT VARS
# -------------
WIN_WIDTH, WIN_HEIGHT = 500, 789
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

FPS = 60
VEL = 5
BASE_HEIHGT = 100
PIPE_HEIGHT = [150, 250, 350, 450, 550, 650]
PIPE_GAP = 200

WHITE = (255, 255, 255)

# -----------
# IMPORT IMGS
# -----------
BACKGROUND_SURFACE = pygame.transform.scale2x(pygame.image.load(
    '/Users/lethien/Desktop/Projects/Flappy Bird by AI with NEAT/Flappy Bird/assets/background-day.png').convert())

BASE_SURFACE = pygame.transform.scale2x(pygame.image.load(
    '/Users/lethien/Desktop/Projects/Flappy Bird by AI with NEAT/Flappy Bird/assets/base.png').convert())

PIPE_SURFACE = pygame.transform.scale2x(pygame.image.load(
    '/Users/lethien/Desktop/Projects/Flappy Bird by AI with NEAT/Flappy Bird/assets/pipe-green.png').convert())

BIRD_DOWNFLAP = pygame.transform.scale2x(pygame.image.load(
    '/Users/lethien/Desktop/Projects/Flappy Bird by AI with NEAT/Flappy Bird/assets/bluebird-downflap.png').convert_alpha())
BIRD_MIDFLAP = pygame.transform.scale2x(pygame.image.load(
    '/Users/lethien/Desktop/Projects/Flappy Bird by AI with NEAT/Flappy Bird/assets/bluebird-midflap.png').convert_alpha())
BIRD_UPFLAP = pygame.transform.scale2x(pygame.image.load(
    '/Users/lethien/Desktop/Projects/Flappy Bird by AI with NEAT/Flappy Bird/assets/bluebird-upflap.png').convert())
BIRD_FRAMES = [BIRD_DOWNFLAP, BIRD_MIDFLAP, BIRD_UPFLAP]

GAME_OVER_SURFACE = pygame.image.load(
    '/Users/lethien/Desktop/Projects/Flappy Bird by AI with NEAT/Flappy Bird/assets/message.png').convert_alpha()

FLAP_SOUND = pygame.mixer.Sound(
    '/Users/lethien/Desktop/Projects/Flappy Bird by AI with NEAT/Flappy Bird/sounds/sfx_wing.wav')
DEATH_SOUND = pygame.mixer.Sound(
    '/Users/lethien/Desktop/Projects/Flappy Bird by AI with NEAT/Flappy Bird/sounds/sfx_die.wav')
SCORE_SOUND = pygame.mixer.Sound(
    '/Users/lethien/Desktop/Projects/Flappy Bird by AI with NEAT/Flappy Bird/sounds/sfx_point.wav')

GAME_FONT = pygame.font.SysFont('cosmicsan', 50)
# ---------
# FUNCTIONS
# ---------
# Base


def draw_base():
    WIN.blit(BASE_SURFACE, (base_pos_x, WIN_HEIGHT - BASE_HEIHGT))
    WIN.blit(BASE_SURFACE, (base_pos_x +
             BASE_SURFACE.get_width(), WIN_HEIGHT - BASE_HEIHGT))


# Pipes
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
        if pipe.bottom >= WIN_HEIGHT:
            WIN.blit(PIPE_SURFACE, pipe)
        else:
            # False x-axis direction, True y-axis direction
            flip_pipe = pygame.transform.flip(PIPE_SURFACE, False, True)
            WIN.blit(flip_pipe, pipe)


# Bird
def bird_animation():
    new_bird = BIRD_FRAMES[bird_index]
    new_bird_rect = new_bird.get_rect(center=(100, bird_rect.centery))
    return new_bird, new_bird_rect


def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement * 3, 1)
    return new_bird


# Collision
def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            DEATH_SOUND.play()
            return False

    if bird_rect.top <= -BASE_HEIHGT or bird_rect.bottom >= WIN_HEIGHT:
        return False
    return True

# Score


def score_display(game_state):
    if game_state == 'main_game':
        score_surface = GAME_FONT.render(str(int(score)), True, WHITE)
        score_rect = score_surface.get_rect(
            center=((WIN_WIDTH - score_surface.get_width()) // 2, 100))
        WIN.blit(score_surface, score_rect)

    if game_state == 'game_over':
        score_surface = GAME_FONT.render(
            'Score: ' + str(int(score)), True, WHITE)
        score_rect = score_surface.get_rect(
            center=(WIN_WIDTH // 2, 100))
        WIN.blit(score_surface, score_rect)

        high_score_surface = GAME_FONT.render('High Score: ' +
                                              str(int(high_score)), True, WHITE)
        high_score_rect = high_score_surface.get_rect(
            center=(WIN_WIDTH // 2, 600))
        WIN.blit(high_score_surface, high_score_rect)


def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score
# ----------
# WHILE LOOP
# ----------


# ___Variables:
# Base
base_pos_x = 0

# Pipes
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1400)  # 1.4 second spawn a pipe

# Bird
bird_index = 0
bird_surface = BIRD_FRAMES[bird_index]
bird_rect = bird_surface.get_rect(center=(100, WIN_HEIGHT // 2 - 100))
gravity = 0.5
bird_movement = 0
BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)  # time for flapping the wings

# Game
game_active = True
score = 0
high_score = 0
score_sound_countdown = 100
game_over_rect = GAME_OVER_SURFACE.get_rect(
    center=(WIN_WIDTH//2, WIN_HEIGHT//2 - 50))

# Loop:
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 9
                FLAP_SOUND.play()

            if event.key == pygame.K_SPACE and not game_active:
                game_active = True
                pipe_list.clear()
                bird_movement = 0
                bird_rect.center = (100, WIN_HEIGHT // 2 - 100)
                score = 0
                score_sound_countdown = 100

        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipes())

        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird_surface, bird_rect = bird_animation()

    # Background
    WIN.blit(BACKGROUND_SURFACE, (0, 0))

    if game_active:
        # Bird
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement
        WIN.blit(rotated_bird, bird_rect)
        game_active = check_collision(pipe_list)

        # Pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        score += 0.01
        score_display('main_game')
        score_sound_countdown -= 1
        if score_sound_countdown == 0:
            SCORE_SOUND.play()
            score_sound_countdown = 100
    else:
        WIN.blit(GAME_OVER_SURFACE, game_over_rect)
        high_score = update_score(score, high_score)
        score_display('game_over')

    # Base
    base_pos_x -= 1
    draw_base()
    if base_pos_x <= -BASE_SURFACE.get_width():
        base_pos_x = 0

    pygame.display.update()
    clock.tick(FPS)
