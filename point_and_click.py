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

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Point and Click')
clock = pygame.time.Clock()

cowboyImg = pygame.image.load('images/cowboy.png')
cactusImg_1 = pygame.image.load('images/cactus_1.png')
cactusImg_2 = pygame.image.load('images/cactus_2.png')
pointerImg = pygame.image.load('images/crosshair.png')
fireImg = pygame.image.load('images/crosshair_fired.png')
hpImg = pygame.image.load('images/hp_bar.png')
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
needle = display(needleImg)


def message_display(text, x_pos, y_pos):
    font = pygame.font.SysFont('Georgia', 15)

    def talk(x_text, y_text):
        gameDisplay.blit(font.render(text, True, white), (x_text, y_text))

    talk(x_pos, y_pos)


def game_loop():
    starting_x = display_width * 0.15
    starting_y = display_height * 0.37
    x = starting_x
    y = starting_y
    cact_x = (display_width * 0.75)
    cact_y = (display_height * 0.35)
    needle_x = cact_x
    needle_y = cact_y + random.randint(-20, 20)
    bar_x = 5
    bar_y = display_height - 100

    talking = False
    game_over = False
    game_exit = False
    hp = 10

    x_change = 0
    y_change = 0
    needle_x_change = 0

    while not game_exit:
        gameDisplay.fill(black)

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
                if event.key == pygame.K_f:
                    needle_x_change = 5

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

        if hp <= 0:
            game_over = True

        # draw basic shapes for background
        pygame.draw.line(gameDisplay, white, (0, display_height * 0.65), (display_width, display_height * 0.65))
        # player box confines
        box_x = starting_x - 50
        box_y = starting_y - 200
        box_width = 250
        box_height = 350
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
        cactus(cact_x, cact_y)
        # draw hp bar based on value of hp
        # ensures that when hp value is changed, appropriate number of bars are drawn
        for num in range(hp):
            hp_bar(bar_x + 30*num, bar_y)
        if talking:
            message_display("Hello!", cact_x - 20, cact_y - 20)
        center_bal = 96/2
        # manage cursor display
        if pygame.mouse.get_pressed()[0]:
            cursor_fired(pygame.mouse.get_pos()[0] - center_bal, pygame.mouse.get_pos()[1] - center_bal)
        else:
            cursor(pygame.mouse.get_pos()[0] - center_bal, pygame.mouse.get_pos()[1] - center_bal)
        # manage collision with needles

        player_hitbox = pygame.Rect(x, y, cowboy_width - 15, cowboy_height)
        pygame.draw.rect(gameDisplay, white, player_hitbox, 2)
        needle_hitbox = pygame.Rect(needle_x, needle_y, needle_width, needle_height)
        pygame.draw.rect(gameDisplay, white, needle_hitbox, 2)
        needle(needle_x, needle_y)
        if player_hitbox.colliderect(needle_hitbox):
            hp -= 1
        pygame.display.update()
        # fps
        clock.tick(30)


game_loop()
pygame.quit()
quit()
