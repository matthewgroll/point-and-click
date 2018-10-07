import pygame
import time

pygame.init()

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


def message_display(text, x_pos, y_pos):
    font = pygame.font.SysFont('Georgia', 15)

    def talk(x_text, y_text):
        gameDisplay.blit(font.render(text, True, white), (x_text, y_text))

    talk(x_pos, y_pos)


cowboyImg = pygame.image.load('images/cowboy.png')
cactusImg_1 = pygame.image.load('images/cactus_1.png')
cactusImg_2 = pygame.image.load('images/cactus_2.png')


def game_loop():
    x = (display_width * 0.15)
    y = (display_height * 0.35)
    cact_x = (display_width * 0.75)
    cact_y = (display_height * 0.35)

    talking = False
    game_exit = False

    x_change = 0
    y_change = 0

    while not game_exit:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change += -5
                if event.key == pygame.K_RIGHT:
                    x_change += 5
                if event.key == pygame.K_UP:
                    y_change += -5
                if event.key == pygame.K_DOWN:
                    y_change += 5
                if event.key == pygame.K_z:
                    talking = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    x_change += 5
                if event.key == pygame.K_RIGHT:
                    x_change += -5
                if event.key == pygame.K_UP:
                    y_change += 5
                if event.key == pygame.K_DOWN:
                    y_change += -5

        x += x_change
        y += y_change
        gameDisplay.fill(black)
        cowboy(x, y)

        if x > display_width - cowboy_width:
            x = display_width - cowboy_width
        elif x < 0:
            x = 0
        if y > display_height - cowboy_height:
            y = display_height - cowboy_height
        elif y < 0:
            y = 0
        cactus(cact_x, cact_y)
        if talking:
            message_display("Hello!", cact_x - 20, cact_y - 20)
        pygame.display.update()
        clock.tick(60)


game_loop()
pygame.quit()
quit()
