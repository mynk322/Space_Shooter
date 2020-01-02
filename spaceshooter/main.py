
#Paste your folder path here
path = ""



import pygame
import random
from pygame import mixer

# initialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800,600))

#background
background = pygame.image.load(path + 'spaceshooter/Images/background.jpg')

#Title and Icon
pygame.display.set_caption(" Space Invader")
icon = pygame.image.load(path + 'spaceshooter/Images/myufo.png')
pygame.display.set_icon(icon)

#Background Sound
mixer.music.load(path+'spaceshooter/sounds/background.wav')
mixer.music.play(-1)
#Player
playerImg = pygame.image.load(path+'spaceshooter/Images/spaceship.png')
playerX = 370
playerY = 480
playerX_change = 0

def player(x,y):
    playerX=x
    playerY=y
    screen.blit(playerImg, (playerX, playerY))

#Enemy
enemyImg =[]
enemyX =[]
enemyY =[] 
enemyX_change =[] 
enemyY_change =[] 
num_of_enemies = 6
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load(path + 'spaceshooter/Images/ghost.png'))
    enemyX.append(random.randint(15,720))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(2)
    enemyY_change.append(0)
    
#Blast
blastImg = pygame.image.load(path+'spaceshooter/Images/blast.png')

#Bullet
bulletImg = pygame.image.load(path + 'spaceshooter/Images/bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state= "ready"

def enemy(x,y,i):
    enemyX=x
    enemyY=y
    screen.blit(enemyImg[i], (enemyX, enemyY))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg,(x+22,y+10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    bulletX-=enemyX
    bulletY-=enemyY
    if bulletX >= -29 and bulletX <= 1 and bulletY <= 27 and bulletY >=-19 :
        return True
    return False
#Score    
score = 0
font = pygame.font.Font('freesansbold.ttf',32)
textX = 10
textY = 10
def show_score(x,y):
    global score
    global font
    score_display = font.render("Score : " + str(score), True, (255, 255, 0))
    screen.blit(score_display,(x,y))

over_font = pygame.font.Font('freesansbold.ttf',190)
#GameOver Text
def game_over_text()    :
    global over_font
    game_display = over_font.render("GAME", True, (255, 255, 255))
    screen.blit(game_display,(100,100))
    over_display = over_font.render("OVER!", True, (255, 255, 255))
    screen.blit(over_display,(100,300))
    
    
# Game Loop
running = True
while running:
    
    #RGB background colour
    screen.fill((0,0,0))
    #background image
    screen.blit(background, (0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
        #if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                playerX_change = 0.0
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.0
                
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":    
                    bulletX = playerX
                    bullet_sound = mixer.Sound(path + 'spaceshooter/sounds/laser.wav')
                    bullet_sound.play()
                    fire_bullet(bulletX,bulletY)
            
    # Checking of boundaries of player         
    playerX+=playerX_change
    for i in range(num_of_enemies):    
        enemyX[i]+=enemyX_change[i]
    for i in range(num_of_enemies):
        
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break
    
    if playerX <= 16 :
        playerX_change = max(playerX_change,0)
    if playerX >= 736 :
        playerX_change = min(playerX_change,0)
        
    # Checking of boundaries of enemy    
    for i in range(num_of_enemies):
        if enemyX[i] <= 16 or enemyX[i] >= 736:
            enemyX_change[i] *= -1
            enemyY[i]+=40
    #Bullet Movement
    if bullet_state is "fire":
        
        fire_bullet(bulletX,bulletY)
        bulletY-=bulletY_change
    for i in range(num_of_enemies):    
        collision = isCollision(enemyX[i],enemyY[i],bulletX,bulletY)
        if collision:
            bulletY=480
            blast_sound = mixer.Sound(path + 'spaceshooter/sounds/explosion.wav')
            blast_sound.play()
            screen.blit(blastImg, (enemyX[i], enemyY[i]))
            bullet_state = "ready"
            score+=1
            enemyX[i] = random.randint(15,720)
            enemyY[i] = random.randint(50,150)
        enemy(enemyX[i], enemyY[i], i)
    
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    show_score(textX,textY)
    player(playerX,playerY)
    pygame.display.update()