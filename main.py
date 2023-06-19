# Author:Arpit Tiwari
# Date:6 november 2022
# Purpose:Making Space Invader Game

import pygame
import random
import math
from pygame import mixer

# Initialize the pygame
pygame.init()
mixer.init()

# create window for game
screen = pygame.display.set_mode((800, 600))

# Background for Game
BgImg = pygame.image.load('data/images/bg.jpg')

# Background music
mixer.music.load('data/audio/back.mp3')
mixer.music.play(-1)

# Set caption and icon for game
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('data/images/ufo.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('data/images/arcade-game.png')
playerx = 370
playery = 480
playerx_change = 0

# Enemy for game
enemyImg = []
enemyx = []
enemyy = []
enemyx_change = []
enemyy_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('data/images/enemy.png'))
    enemyx.append(random.randint(0, 735))
    enemyy.append(random.randint(50, 150))
    enemyx_change.append(0.4)
    enemyy_change.append(40)


# Bullet
BulletImg = pygame.image.load('data/images/bullet.png')
Bulletx = 0
Bullety = 480
Bulletx_change = 0
Bullety_change = 1.5
Bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
testx = 10
testy = 10

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

# To blit player image


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global Bullet_state
    Bullet_state = "Fire"
    screen.blit(BulletImg, (x + 16, y+10))


def isCollision(enemyx, enemyy, Bulletx, Bullety):
    distance = math.sqrt(math.pow(enemyx - Bulletx, 2) +
                         (math.pow(enemyy - Bullety, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game Loop
running = True
while running:
    # set color for screen - RGB(Red,Green,Blue)
    screen.fill((0, 0, 0))

    # Background Image
    screen.blit(BgImg, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if player presses left or right arrow key
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerx_change = -4

            if event.key == pygame.K_RIGHT:
                playerx_change = 4

            if event.key == pygame.K_SPACE:
                bullet_sound = mixer.Sound('data/audio/bullet.mp3')
                bullet_sound.play()

                if Bullet_state == "ready":
                    Bulletx = playerx
                    fire_bullet(Bulletx, Bullety)

        # if player releases left or right arrow key
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerx_change = 0

    # Spaceship Movement
    playerx += playerx_change
    if playerx <= 0:
        playerx = 0
    elif playerx >= 736:
        playerx = 736

    # Enemy Movement
    for i in range(num_of_enemies):
        # Game Over
        if enemyy[i] > 440:
            for j in range(num_of_enemies):
                enemyy[j] = 2000
            game_over_text()
            break
        enemyx[i] += enemyx_change[i]
        if enemyx[i] <= 0:
            enemyx_change[i] = 0.5
            enemyy[i] += enemyy_change[i]

        elif enemyx[i] >= 736:
            enemyx_change[i] = -0.5
            enemyy[i] += enemyy_change[i]

        # Collision
        collision = isCollision(enemyx[i], enemyy[i], Bulletx, Bullety)
        if collision:
            explosion_sound = mixer.Sound('data/audio/explosion.mp3')
            explosion_sound.play()
            Bullety = 480
            Bullet_state = "ready"
            score_value += 1

            enemyx[i] = random.randint(0, 735)
            enemyy[i] = random.randint(50, 150)

        enemy(enemyx[i], enemyy[i], i)

    # Bullet Movement
    if Bullety <= 0:
        Bullety = 480
        Bullet_state = "ready"

    if Bullet_state == "Fire":
        fire_bullet(Bulletx, Bullety)
        Bullety -= Bullety_change
    show_score(testx, testy)
    player(playerx, playery)
    pygame.display.update()