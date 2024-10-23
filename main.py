import pygame
from pygame import mixer
import random
import math
#Intialize the pygame
pygame.init ()

#Creates the screen
screen = pygame.display.set_mode((800, 600))

#Background
background = pygame.image.load('background.png')

#Background Sound
mixer.music.load('background.wav')
mixer.music.play(-1)

#Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

#Player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0

#Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append (pygame.image.load('enemy.png'))
    enemyX.append (random.randint(0,800))
    enemyY.append (random.randint(50,150))
    enemyX_change.append  (4)
    enemyY_change.append (40)

#Bullets
bulletsImg = pygame.image.load('bullets.png')
bulletsX = 0
bulletsY = 480
bulletsX_change = 0
bulletsY_change = 10
bullets_state = 'ready'

#Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

#Game over text
over_font = pygame.font.Font('freesansbold.ttf', 64)

def show_score(x,y):
    score = font.render("Score :" + str(score_value), True, (255,255,255))
    screen.blit(score,(x,y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255,255,255))
    screen.blit(over_text, (200,250))


def player(x,y):
    screen.blit(playerImg,(x,y))

def enemy(x,y, i):
    screen.blit(enemyImg[i],(x,y))

def fire_bullets(x,y):
    global bullets_state
    bullets_state = "fire"
    screen.blit(bulletsImg, (x + 16, y + 10))

def isCollision(enemyX,enemyY,bulletsX,bulletsY):
    distance = math.sqrt((math.pow(enemyX-bulletsX,2)) + (math.pow(enemyY-bulletsY, 2)))
    if distance < 27:
        return True
    else:
        return False

#Game Loop
running = True
while running:

    # RGB - Red, Green, Blue
    screen.fill((0, 128, 128))
    #Background
    screen.blit(background, (0,0))


    for event in pygame.event.get() :
        if event.type == pygame.QUIT:
            running = False

        #If keystroke is pressed right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key ==pygame.K_SPACE:
               if bullets_state == 'ready':
                bullets_Sound = mixer.Sound('laser.wav')
                bullets_Sound.play()
                bulletsX = playerX
                fire_bullets(playerX, bulletsY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

#Checking for boundaries of spaceship
    playerX += playerX_change

    if playerX <=0:
        playerX = 0
    elif playerX >=736:
        playerX = 736

#Enemy Movement
    for i in range(num_of_enemies):

        #Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]

        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

    # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletsX, bulletsY)
        if collision:
            explosion_Sound = mixer.Sound('explosion.wav')
            explosion_Sound.play()
            bulletsY = 480
            bullets_state = 'ready'
            score_value += 1
            enemyX[i] = random.randint(0, 800)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

#Bullet Movement
    if bulletsY <=0 :
        bulletsY = 480
        bullets_state = 'ready'

    if bullets_state == 'fire':
        fire_bullets(playerX, bulletsY)
        bulletsY -= bulletsY_change



    player(playerX,playerY)
    show_score(textX,textY)
    pygame.display.update()