import math
import random

import pygame
from pygame import mixer

# Intialize the pygame
pygame.init()

# create the screen cua so game123
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load(r'game1\image\background.png')

# Sound
mixer.music.load(r"game1\sound\background.wav")
mixer.music.play(-1)

# Caption and Icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load(r'game1\image\ufo.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load(r'game1\image\space-invaders.png')
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 5

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load(r'game1\image\enemy.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(5)
    enemyY_change.append(17)

# Bullet

bulletImg = pygame.image.load(r'game1\image\bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 15
bullet_state = "ready"

# Score

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render("Score: " + str(score_value) + "/30", True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_win_text():
    over_text = over_font.render("YOU WIN", True, (255, 255, 255))
    screen.blit(over_text, (230, 250))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (230, 250))

def pause():
    paused = True
    clock = pygame.time.Clock()

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = False

        # Hiển thị màn hình tạm dừng
        screen.blit(background, (0, 0))

        # Vẽ một hình chữ nhật semi-transparent làm nền
        pause_overlay = pygame.Surface((800, 600), pygame.SRCALPHA)
        pygame.draw.rect(pause_overlay, (0, 0, 0, 200), (0, 0, 800, 600))
        screen.blit(pause_overlay, (0, 0))

        # Tạo hiệu ứng animation cho khung
        pause_frame = pygame.image.load(r'game1\image\pause.jpg')  # Đây là ảnh khung
        pause_frame = pygame.transform.scale(pause_frame, (400, 300))  # Resize khung
        screen.blit(pause_frame, (200, 150))

        # Tạo nút tiếp tục
        continue_button = pygame.image.load(r'game1\image\continue.jpg')  # Đây là ảnh nút tiếp tục
        continue_button = pygame.transform.scale(continue_button, (200, 50))  # Resize nút tiếp tục
        screen.blit(continue_button, (300, 400))

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        # Kiểm tra nếu người chơi click vào nút tiếp tục
        if 300 + continue_button.get_width() > mouse[0] > 300 and 400 + continue_button.get_height() > mouse[1] > 400:
            # Hiển thị nút tiếp tục với hiệu ứng khi di chuột qua
            screen.blit(pygame.transform.scale(continue_button, (continue_button.get_width() + 5, continue_button.get_height() + 5)), (295, 395))
            if click[0] == 1:
                paused = False

        pygame.display.update()
        clock.tick(60)



def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 40:
        return True
    else:
        return False


def reset_game():
    global playerX, playerY, playerX_change, enemyX, enemyY, enemyX_change, enemyY_change, bulletX, bulletY, bullet_state, score_value

    playerX = 370
    playerY = 480
    playerX_change = 0

    for i in range(num_of_enemies):
        enemyX[i] = random.randint(0, 736)
        enemyY[i] = random.randint(50, 150)
        enemyX_change[i] = 2
        enemyY_change[i] = 20

    bulletX = 0
    bulletY = 480
    bulletX_change = 0
    bulletY_change = 15
    bullet_state = "ready"

    score_value = 0


# Thiết lập phím tắt "R" cho việc reset game
reset_key = pygame.K_r
for event in pygame.event.get():
    if event.type == pygame.QUIT:
        running = False

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            playerX_change = -5
        elif event.key == pygame.K_RIGHT:
            playerX_change = 5
  
        
# Game Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletSound = mixer.Sound(r"game1\sound\laser.wav")
                    bulletSound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
            if event.key == pygame.K_ESCAPE:
                pause() 
            # Kiểm tra khi nào phím tắt "R" được nhấn
            elif event.key == reset_key:
                reset_game()
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    for i in range(num_of_enemies):
        if score_value >= 30:
            winSound = mixer.Sound(r"game1\sound\win.wav")
            winSound.play()
            game_win_text()
            break
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            overSound = mixer.Sound(r"game1\sound\game_over.wav")
            overSound.play()
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosionSound = mixer.Sound(r"game1\sound\explosion.wav")
            explosionSound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)
    
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
    
    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()