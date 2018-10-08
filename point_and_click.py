import pygame
import time
import random

pygame.init()
# 800 by 600 default
display_width = 800
display_height = 600
cowboy_width = 60
cowboy_height = 83
cactus_width = 86
cactus_height = 94
needle_width = 96
needle_height = 42
enemy_bar_width = 4

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Point and Click')
clock = pygame.time.Clock()

cowboyImg = pygame.image.load('images/cowboy.png')
cactusImg_1 = pygame.image.load('images/cactus.png')
pointerImg = pygame.image.load('images/crosshair.png')
fireImg = pygame.image.load('images/crosshair_fired.png')
hpImg = pygame.image.load('images/hp_bar.png')
enemyBarImg = pygame.image.load('images/enemy_bar.png')
needleImg = pygame.image.load('images/needle.png')


def display(img):
    def display_func(x, y):
        gameDisplay.blit(img, (x, y))
    return display_func


cowboy = display(cowboyImg)
cactus = display(cactusImg_1)
cursor = display(pointerImg)
cursor_fired = display(fireImg)
hp_bar = display(hpImg)
enemy_bar = display(enemyBarImg)
needle = display(needleImg)


def message_display(text, x_pos, y_pos, font_size):
    font = pygame.font.SysFont('Georgia', font_size)

    def talk(x_text, y_text):
        gameDisplay.blit(font.render(text, True, white), (x_text, y_text))

    talk(x_pos, y_pos)


def game_loop():
    starting_x = display_width * 0.15
    starting_y = display_height * 0.37
    x = starting_x
    y = starting_y
    cactus_x = (display_width * 0.75)
    cactus_y = (display_height * 0.35)
    starting_needle_x = cactus_x
    starting_needle_y = cactus_y
    needle_x = starting_needle_x
    needle_y = starting_needle_y
    bar_x = 5
    bar_y = display_height - 100

    talking = False
    game_over = False
    game_won = False
    game_exit = False
    hp = 25
    cactus_hp = 180

    x_change = 0
    y_change = 0
    needle_x_change = 12

    while not game_exit:
        gameDisplay.fill(black)
        # hitboxes can be made visible for testing purposes
        player_hitbox = pygame.Rect(x, y, cowboy_width - 15, cowboy_height)
        pygame.draw.rect(gameDisplay, black, player_hitbox, 2)
        needle_hitbox = pygame.Rect(needle_x, needle_y, needle_width, needle_height)
        pygame.draw.rect(gameDisplay, black, needle_hitbox, 2)
        cactus_hitbox = pygame.Rect(cactus_x, cactus_y, cactus_width, cactus_height)
        pygame.draw.rect(gameDisplay, black, cactus_hitbox, 2)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True

            speed = 7
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change += -speed
                if event.key == pygame.K_RIGHT:
                    x_change += speed
                if event.key == pygame.K_UP:
                    y_change += -speed
                if event.key == pygame.K_DOWN:
                    y_change += speed
                if event.key == pygame.K_z:
                    talking = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    x_change += speed
                if event.key == pygame.K_RIGHT:
                    x_change += -speed
                if event.key == pygame.K_UP:
                    y_change += speed
                if event.key == pygame.K_DOWN:
                    y_change += -speed

        x += x_change
        y += y_change
        needle_x -= needle_x_change

        if hp <= 0 and not game_won:
            hp = 0
            game_over = True

        if game_over:
            message_display("GAME OVER!", display_width/2, 50, 70)
        if cactus_hp <= 0 and not game_over:
            game_won = True
            message_display("YOU WIN!", display_width/2 , 50, 70)

        # draw basic shapes for background
        pygame.draw.line(gameDisplay, white, (0, display_height * 0.65), (display_width, display_height * 0.65))
        # player box confines
        box_x = starting_x - 50
        box_y = starting_y - 150
        box_width = 250
        box_height = 300
        pygame.draw.rect(gameDisplay, white, [box_x, box_y, box_width, box_height], 2)
        cowboy(x, y)
        # keep player within confines of box
        if x > box_x + box_width - cowboy_width:
            x = box_x + box_width - cowboy_width
        elif x < box_x:
            x = box_x
        if y > box_y + box_height - cowboy_height:
            y = box_y + box_height - cowboy_height
        elif y < box_y:
            y = box_y
        # draw cactus
        cactus(cactus_x, cactus_y)
        # draw hp bar based on value of hp
        # ensures that when hp value is changed, appropriate number of bars are drawn
        for num in range(hp):
            hp_bar(bar_x + 30*num, bar_y)
        for num in range(cactus_hp):
            enemy_bar(bar_x + num*enemy_bar_width, bar_y - 60)
        if talking:
            message_display("Hello!", cactus_x - 20, cactus_y - 20, 15)
        center_bal = 96/2
        # manage cursor display
        if pygame.mouse.get_pressed()[0]:
            cursor_fired(pygame.mouse.get_pos()[0] - center_bal, pygame.mouse.get_pos()[1] - center_bal)
        else:
            cursor(pygame.mouse.get_pos()[0] - center_bal, pygame.mouse.get_pos()[1] - center_bal)
        # manage collision with needles
        needle(needle_x, needle_y)
        if needle_x <= 0:
            needle_x = starting_needle_x
            needle_y = starting_needle_y + random.randint(-125, 75)
        if player_hitbox.colliderect(needle_hitbox):
            hp -= 1
        if pygame.mouse.get_pressed()[0] and needle_hitbox.collidepoint(pygame.mouse.get_pos()):
            needle_x = -100
        if pygame.mouse.get_pressed()[0] and cactus_hitbox.collidepoint(pygame.mouse.get_pos()):
            cactus_hp -= 1
        pygame.display.update()
        # fps
        clock.tick(60)


game_loop()
pygame.quit()
quit()
