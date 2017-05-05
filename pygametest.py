import pygame


def check_collision(player_x, player_y, treasure_x, treasure_y):
    global screen, textWin, player_size_x, player_size_y
    collisionState = False
    if player_y >= treasure_y and player_y <= treasure_y + player_size_y:
        if player_x >= treasure_x and player_x <= treasure_x + player_size_x:

            player_y = player_y_start
            collisionState = True
        elif player_x + player_size_x >= treasure_x and player_x + player_size_x <= treasure_x:

            player_y = player_y_start
            collisionState = True
    elif player_y + player_size_y >= treasure_y and player_y + player_size_y <= treasure_y + player_size_y:
        if player_x >= treasure_x and player_x <= treasure_x + player_size_x:

            player_y = player_y_start
            collisionState = True
        elif player_x + player_size_x >= treasure_x and player_x + player_size_x <= treasure_x:

            player_y = player_y_start
            collisionState = True
    return collisionState, player_y


pygame.init()
screen_x = 900
screen_y = 900
player_size_x = 50
player_size_y = 50
screen = pygame.display.set_mode((screen_x, screen_y))

finished = False
player_x = int((screen_x - player_size_x) / 2)
player_y = screen_y - player_size_y
player_y_start = player_y

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

enemyImage = pygame.image.load("enemy.png")
enemyImage = pygame.transform.scale(enemyImage, (player_size_x, player_size_y))
enemyImage = enemyImage.convert_alpha()
enemy_x = int((screen_x - player_size_x) / 2)
enemy_y = int((screen_y - (player_size_y * 3)))
movingRight = True

font = pygame.font.SysFont("comicsans", 85)
level = 1
textWin = font.render("You've reached level {}!".format(level), True, (0, 0, 0))

text_x = int(screen_x / 2) - textWin.get_width() / 2
text_y = int(screen_y / 2) - textWin.get_height() / 2

collisionTreasure = False
collisionEnemy = True

enemies = [(enemy_x, enemy_y, movingRight)]

frame = pygame.time.Clock()
while finished == False:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
    enemyIndex = 0
    for enemy_x, enemy_y, movingRight in enemies:
        if enemy_x >= screen_x - 50 - player_size_x:
            movingRight = False
        elif enemy_x <= 50:
            movingRight = True

        if movingRight == True:
            enemy_x += 5 * level
        else:
            enemy_x -= 5 * level
        enemies[enemyIndex] = (enemy_x, enemy_y, movingRight)
        enemyIndex += 1
    pressedKeys = pygame.key.get_pressed()
    if pressedKeys[pygame.K_SPACE] == 1:
        player_y -= 5

    color = (0, 0, 255)
    black = (0, 0, 0)

    # draw in background, player, enemies
    screen.blit(background, (0, 0))
    screen.blit(treasureImage, (treasure_x, treasure_y))
    screen.blit(playerImage, (player_x, player_y))
    for enemy_x, enemy_y, movingRight in enemies:
        screen.blit(enemyImage, (enemy_x, enemy_y))
        collisionEnemy, player_y = check_collision(player_x, player_y, enemy_x, enemy_y)
        if collisionEnemy == True:
            level = 1
            textWin = font.render("Oh dear, you died!", True, (0, 0, 0))
        screen.blit(textWin, (text_x, text_y))
        pygame.display.flip()
        frame.tick(1)

collisionTreasure, player_y = check_collision(player_x, player_y, treasure_x, treasure_y)
if collisionTreasure == True:
    level += 1
    enemies.append((enemy_x - 50 * level, enemy_y - 50 * level, False))
    textWin = font.render("You've reached level {}!".format(level), True, (0, 0, 0))
    screen.blit(textWin, (text_x, text_y))
    pygame.display.flip()
    frame.tick(1)
pygame.display.flip()
frame.tick(30)
