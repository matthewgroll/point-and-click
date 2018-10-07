import pygame

pygame.init()

display_width = 800
display_height = 600

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


cowboyImg = pygame.image.load('images/cowboy.png')
cactusImg_1 = pygame.image.load('images/cactus_1.png')
cactusImg_2 = pygame.image.load('images/cactus_2.png')


def game_loop():
    x = (display_width * 0.15)
    y = (display_height * 0.35)
    cact_x = (display_width * 0.75)
    cact_y = (display_height * 0.35)

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
        cactus(cact_x, cact_y)
        pygame.display.update()
        clock.tick(60)


game_loop()
pygame.quit()
quit()
