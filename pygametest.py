import pygame


def check_collision(player_x, player_y, treasure_x, treasure_y):
    global screen, textWin, player_size_x, player_size_y, player_y_start, player_x_start
    collisionState = False
    if player_y >= treasure_y and player_y <= treasure_y + player_size_y:
        if player_x >= treasure_x and player_x <= treasure_x + player_size_x:
            player_y = player_y_start
            player_x = player_x_start
            collisionState = True
        elif player_x + player_size_x >= treasure_x and player_x + player_size_x <= treasure_x:
            player_y = player_y_start
            player_x = player_x_start
            collisionState = True
    elif player_y + player_size_y >= treasure_y and player_y + player_size_y <= treasure_y + player_size_y:
        if player_x >= treasure_x and player_x <= treasure_x + player_size_x:
            player_y = player_y_start
            player_x = player_x_start
            collisionState = True
        elif player_x + player_size_x >= treasure_x and player_x + player_size_x <= treasure_x:
            player_y = player_y_start
            player_x = player_x_start
            collisionState = True
    return collisionState, player_y, player_x


pygame.init()
screen_x = 700
screen_y = 700
player_size_x = int(screen_x / 23)
player_size_y = int(screen_y / 25)
font_size = int(screen_x / 20)
screen = pygame.display.set_mode((screen_x, screen_y))

finished = False
player_x = int((screen_x - player_size_x) / 2)
player_y = screen_y - player_size_y
player_y_start = player_y
player_x_start = player_x
player_score = 0
player_lives = 3

playerImage = pygame.image.load("player.png")
playerImage = pygame.transform.scale(playerImage, (player_size_x, player_size_y))
playerImage = playerImage.convert_alpha()

background = pygame.image.load("background.png")
background = pygame.transform.scale(background, (screen_x, screen_y))

treasureImage = pygame.image.load("treasure.png")
treasureImage = pygame.transform.scale(treasureImage, (player_size_x, player_size_y))
treasureImage = treasureImage.convert_alpha()
treasure_x = int((screen_x - player_size_x) / 2)
treasure_y = 50

enemyName = {0: "Eddie", 1: "Mabel", 2: "Sennen", 3: "Summer", 4: "Tammie", 5: "Darren", 6: "Crissnog", 7: "Keith"}

enemyImage = {}
for i in range(0, 8):
    filename = enemyName[i] + ".jpg"
    enemyImagetemp = pygame.image.load(filename)
    enemyImagetemp = pygame.transform.scale(enemyImagetemp, (player_size_x, player_size_y))
    enemyImagetemp = enemyImagetemp.convert_alpha()
    enemyImage[i] = enemyImagetemp
enemy_x = int((screen_x - player_size_x) / 2)
enemy_y = int((screen_y - (player_size_y * 3)))
movingRight = True
speedup_factor = 0.5

enemySound = pygame.mixer.Sound("eaten.wav")
treasureSound = pygame.mixer.Sound('treasure_sound.wav')

font = pygame.font.SysFont("comicsans", font_size)
level = 1
enemy_speed = 1
textWin = font.render("You've reached level {}!".format(level), True, (0, 0, 0))

text_x = int(screen_x / 2) - textWin.get_width() / 2
text_y = int(screen_y / 2) - textWin.get_height() / 2

collisionTreasure = False
collisionEnemy = True

enemies = [(enemy_x, enemy_y, movingRight)]

text_color = (0, 0, 0)

frame = pygame.time.Clock()
while finished == False:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
    enemyIndex = 0
    for enemy_x, enemy_y, movingRight in enemies:
        if enemy_x >= screen_x - (player_size_x):
            movingRight = False
        elif enemy_x <= 0:
            movingRight = True

        if movingRight == True:
            enemy_x += 5 * ((enemyIndex + enemy_speed) * speedup_factor)
        else:
            enemy_x -= 5 * ((enemyIndex + enemy_speed) * speedup_factor)
        enemies[enemyIndex] = (enemy_x, enemy_y, movingRight)
        enemyIndex += 1

    pressedKeys = pygame.key.get_pressed()
    if pressedKeys[pygame.K_q] == 1:
        player_y -= 5
        if player_y < 0:
            player_y = 0
    if pressedKeys[pygame.K_a] == 1:
        player_y += 5
        if player_y > screen_y - player_size_y:
            player_y = screen_y - player_size_y

    if pressedKeys[pygame.K_o] == 1:
        player_x -= 5
        if player_x < player_size_x:
            player_x = player_size_x
    if pressedKeys[pygame.K_p] == 1:
        player_x += 5
        if player_x > screen_x - player_size_x:
            player_x = screen_x - player_size_x

    # draw in background, player, enemies
    screen.blit(background, (0, 0))
    screen.blit(treasureImage, (treasure_x, treasure_y))
    screen.blit(playerImage, (player_x, player_y))

    enemy_count = 0
    for enemy_x, enemy_y, movingRight in enemies:
        screen.blit(enemyImage[enemy_count], (enemy_x, enemy_y))
        collisionEnemy, player_y, player_x = check_collision(player_x, player_y, enemy_x, enemy_y)
        if collisionEnemy == True:
            enemySound.play()
            enemy_speed -= 1
            if enemy_speed < 1:
                enemy_speed = 1
            player_score -= (50 * (enemy_count + 1))
            if player_score < 0:
                player_score = 0
            player_lives -= 1
            textLose = font.render("Oh dear {} got you!".format(enemyName[enemy_count]), True, text_color)
            screen.blit(textLose, (text_x, text_y))
            pygame.display.flip()
            frame.tick(1)
            if player_lives == 0:
                textEnd = font.render("Game Over.  Your score = {}".format(player_score), True, text_color)
                screen.blit(textEnd, ((screen_x / 2 - textEnd.get_width() / 2), screen_y / 2 + (font_size * 2)))
                pygame.display.flip()
                frame.tick(1)
                frame.tick(1)
                frame.tick(1)
                finished = True
        enemy_count += 1

    collisionTreasure, player_y, player_x = check_collision(player_x, player_y, treasure_x, treasure_y)
    if collisionTreasure == True:
        treasureSound.play()
        player_score += (100 * level)
        level += 1
        enemy_speed += 1
        if level <= 8:
            enemies.append((enemy_x - 50 * level, enemy_y - (player_size_y * 2) - 5 * level, False))
        textWin = font.render("You've reached level {}!".format(level), True, text_color)
        screen.blit(textWin, (text_x, text_y))
        pygame.display.flip()
        frame.tick(1)

    textScore = font.render("Score : {}".format(player_score), True, text_color)
    screen.blit(textScore, (50, 50))
    textLives = font.render("Lives: {}".format(player_lives), True, text_color)
    screen.blit(textLives, (screen_x - 200, font_size * 2))
    textLevel = font.render("Level: {}".format(level), True, text_color)
    screen.blit(textLevel, (screen_x - 200, font_size))

    pygame.display.flip()
    frame.tick(30)
