import pygame
import random
import math
from pygame import mixer

# Initialazer pygame
pygame.init()

# Create screen
screen = pygame.display.set_mode((800, 600))

# Setting
pygame.display.set_caption("Space Battle")
icon = pygame.image.load("img/ovni.png")
pygame.display.set_icon(icon)
background = pygame.image.load("img/Fondo.jpg")

# Player
img_player = pygame.image.load("img/cohete.png")
player_x = 368
player_y = 520
player_x_change = 0

# Enemies
img_enemies = []
enemies_x = []
enemies_y = []
enemies_x_change = []
enemies_y_change = []
enemies_quantities = 8

for e in range(enemies_quantities):
    img_enemies.append(pygame.image.load("img/enemigo.png"))
    enemies_x.append(random.randint(0, 736))
    enemies_y.append(random.randint(50, 200))
    enemies_x_change.append(0.1)
    enemies_y_change.append(50)

# Shoot
img_shoot = pygame.image.load("img/bala.png")
shoot_x = 0
shoot_y = 520
shoot_x_change = 0
shoot_y_change = 0.5
shoot_visible = False

# Score
score = 0
font = pygame.font.Font('freesansbold.ttf', 32)
font_finish = pygame.font.Font('freesansbold.ttf', 40)
text_x = 10
text_y = 10

# Sounds game
mixer.music.load('sound/MusicaFondo.mp3')
mixer.music.set_volume(0.3)
mixer.music.play(-1)


def end_game():
    finish_game_text = font_finish.render("**** END GAME ****", True, (255, 255, 255))
    screen.blit(finish_game_text, (220, 200))


def show_score(x, y):
    text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(text, (x, y))


def player(x, y):
    screen.blit(img_player, (x, y))


def enemies(x, y, ene):
    screen.blit(img_enemies[ene], (x, y))


def shoot(x, y):
    global shoot_visible
    shoot_visible = True
    screen.blit(img_shoot, (x + 16, y + 10))


def is_collision(x_1, y_1, x_2, y_2):
    distance = math.sqrt(math.pow(x_1 - x_2, 2) + math.pow(y_1 - y_2, 2))
    if distance < 27:
        return True
    else:
        return False


# Loop of game
is_run = True
while is_run:
    # Change background
    screen.blit(background, (0, 0))

    # Loop for events
    for event in pygame.event.get():
        # Condition close window
        if event.type == pygame.QUIT:
            is_run = False

        # Press keys left and right
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change -= 0.3
            if event.key == pygame.K_RIGHT:
                player_x_change += 0.3
            if event.key == pygame.K_SPACE:
                sound_shoot = mixer.Sound('sound/disparo.mp3')
                sound_shoot.play()
                if not shoot_visible:
                    shoot_x = player_x
                    shoot(shoot_x, shoot_y)

        # Release key pressed
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0

    player_x += player_x_change
    if player_x <= 0:
        player_x = 0
    elif player_x >= 736:
        player_x = 736

    # Configuration enemies
    for e in range(enemies_quantities):
        # finish game
        if enemies_y[e] > 480:
            for k in range(enemies_quantities):
                enemies_y[k] = 1000
            end_game()
            break

        enemies_x[e] += enemies_x_change[e]
        if enemies_x[e] <= 0:
            enemies_x_change[e] = 0.1
            enemies_y[e] += enemies_y_change[e]
        elif enemies_x[e] >= 736:
            enemies_x_change[e] = -0.1
            enemies_y[e] += enemies_y_change[e]

        collision = is_collision(enemies_x[e], enemies_y[e], shoot_x, shoot_y)
        if collision:
            sound_collision = mixer.Sound('sound/Golpe.mp3')
            sound_collision.play()
            shoot_y = 500
            shoot_visible = False
            score += 1
            enemies_x[e] = random.randint(0, 736)
            enemies_y[e] = random.randint(50, 200)

        enemies(enemies_x[e], enemies_y[e], e)

    if shoot_y <= -64:
        shoot_y = 500
        shoot_visible = False

    if shoot_visible:
        shoot(shoot_x, shoot_y)
        shoot_y -= shoot_y_change

    player(player_x, player_y)
    show_score(text_x, text_y)
    pygame.display.update()
