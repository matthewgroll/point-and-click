import pygame
import time

pygame.init()
# 800 by 600 default
display_width = 800
display_height = 600
cowboy_width = 60
cowboy_height = 83
cactus_width = 86
cactus_height = 94

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Point and Click')
clock = pygame.time.Clock()


def cowboy(x_val_cow, y_val_cow):
    gameDisplay.blit(cowboyImg, (x_val_cow, y_val_cow))


# state: 0 = normal, 1 = damaged
cactus_state = 0


def cactus(x_val_cact, y_val_cact):
    if cactus_state == 0:
        gameDisplay.blit(cactusImg_1, (x_val_cact, y_val_cact))
    if cactus_state == 1:
        gameDisplay.blit(cactusImg_2, (x_val_cact, y_val_cact))


def cursor(x_val_mouse, y_val_mouse):
    gameDisplay.blit(pointerImg, (x_val_mouse - 96/2, y_val_mouse - 96/2))


def cursor_fired(x_val_mouse, y_val_mouse):
    gameDisplay.blit(fireImg, (x_val_mouse - 96/2, y_val_mouse - 96/2))


def hp_bar(x_val_bar, y_val_bar):
    gameDisplay.blit(hpImg, (x_val_bar, y_val_bar))


def message_display(text, x_pos, y_pos):
    font = pygame.font.SysFont('Georgia', 15)

    def talk(x_text, y_text):
        gameDisplay.blit(font.render(text, True, white), (x_text, y_text))

    talk(x_pos, y_pos)


cowboyImg = pygame.image.load('images/cowboy.png')
cactusImg_1 = pygame.image.load('images/cactus_1.png')
cactusImg_2 = pygame.image.load('images/cactus_2.png')
pointerImg = pygame.image.load('images/crosshair.png')
fireImg = pygame.image.load('images/crosshair_fired.png')
hpImg = pygame.image.load('images/hp_bar.png')
needleImg = pygame.image.load('images/needle.png')

def game_loop():
    starting_x = display_width * 0.15
    starting_y = display_height * 0.37
    x = starting_x
    y = starting_y
    cact_x = (display_width * 0.75)
    cact_y = (display_height * 0.35)
    bar_x = 5
    bar_y = display_height - 100

    talking = False
    game_over = False
    game_exit = False
    hp = 10

    x_change = 0
    y_change = 0

    while not game_exit:

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
        if hp <= 0:
            game_over = True
        gameDisplay.fill(black)
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
        if pygame.mouse.get_pressed()[0]:
            cursor_fired(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
        else:
            cursor(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
        pygame.display.update()
        clock.tick(60)


game_loop()
pygame.quit()
quit()
