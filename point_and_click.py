import pygame
import random

pygame.init()

# basic game constants
DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# dimensions for hit boxes
cowboy_width, cowboy_height = 60, 83
cactus_width, cactus_height = 86, 94
needle_width, needle_height = 96, 42


# set up display, each sprite capable of movement
def display(filename):
    def display_func(x, y):
        gameDisplay.blit(pygame.image.load(filename), (x, y))
    return display_func


# define appropriate png files for sprites
cowboy = display('images/cowboy.png')
cactus = display('images/cactus.png')
crosshair = display('images/crosshair.png')
crosshair_fired = display('images/crosshair_fired.png')
hp_bar = display('images/hp_bar.png')
enemy_bar = display('images/enemy_bar.png')
needle = display('images/needle.png')


# function for displaying text on screen
def message_display(text, x_pos, y_pos, font_size):
    font = pygame.font.SysFont('Georgia', font_size)
    gameDisplay.blit(font.render(text, True, WHITE), (x_pos, y_pos))


# set up window display, window text, and in-game clock
gameDisplay = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pygame.display.set_caption('Passion Fruit')
clock = pygame.time.Clock()


def game_loop():
    game_exit = False
    game_won = False
    game_over = False
    debug = False

    cowboy_init_x, cowboy_init_y = DISPLAY_WIDTH * 0.2, DISPLAY_HEIGHT * 0.2
    cowboy_x, cowboy_y = cowboy_init_x, cowboy_init_y
    cactus_init_x, cactus_init_y = DISPLAY_WIDTH * 0.8, DISPLAY_HEIGHT * 0.3
    cactus_x, cactus_y = cactus_init_x, cactus_init_y
    needle_x, needle_y = cactus_init_x, cactus_init_y

    cowboy_speed = 8
    needle_speed = 12

    cowboy_x_change, cowboy_y_change = 0, 0
    box_width, box_height = cowboy_width * 4, cowboy_height * 4
    box_x, box_y = cowboy_init_x - cowboy_width * 2, cowboy_init_y - cowboy_height*1.3

    bar_x, bar_y = 5, DISPLAY_HEIGHT - 100
    enemy_bar_x, enemy_bar_y = bar_x, bar_y - 70
    bar_width = 30
    player_hp, player_atk = 23, 1
    cactus_hp, cactus_atk = 10, 2

    FPS = 30
    cooldown = 30 * 0.5
    invuln_time = cooldown
    damaged = False

    while not game_exit:
        gameDisplay.fill(BLACK)

        player_hitbox = pygame.Rect(cowboy_x, cowboy_y, cowboy_width - 15, cowboy_height)
        cactus_hitbox = pygame.Rect(cactus_x, cactus_y, cactus_width, cactus_height)
        needle_hitbox = pygame.Rect(needle_x, needle_y, needle_width, needle_height)

        if debug:
            pygame.draw.rect(gameDisplay, WHITE, player_hitbox, 2)
            pygame.draw.rect(gameDisplay, WHITE, cactus_hitbox, 2)
            pygame.draw.rect(gameDisplay, WHITE, needle_hitbox, 2)

        # define conditions for having game won or lost
        if player_hp <= 0 and not game_won:
            game_over = True
            message_display("GAME OVER!", DISPLAY_WIDTH / 2, 50, 70)
        if cactus_hp <= 0 and not game_over:
            game_won = True
            message_display("YOU WIN!", DISPLAY_WIDTH / 2, 50, 70)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True

            # movement based on keys being pressed
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    cowboy_x_change += -cowboy_speed
                if event.key == pygame.K_RIGHT:
                    cowboy_x_change += cowboy_speed
                if event.key == pygame.K_UP:
                    cowboy_y_change += -cowboy_speed
                if event.key == pygame.K_DOWN:
                    cowboy_y_change += cowboy_speed

            # movement negated when keys are lifted
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    cowboy_x_change += cowboy_speed
                if event.key == pygame.K_RIGHT:
                    cowboy_x_change += -cowboy_speed
                if event.key == pygame.K_UP:
                    cowboy_y_change += cowboy_speed
                if event.key == pygame.K_DOWN:
                    cowboy_y_change += -cowboy_speed

            # event for firing at cactus: deals damage equal to player_atk
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                crosshair_fired(mouse_x - center_bal, mouse_y - center_bal)
                if cactus_hitbox.collidepoint(mouse_x, mouse_y):
                    cactus_hp -= player_atk
                if needle_hitbox.collidepoint(mouse_x, mouse_y):
                    # ideally the needle object would be temporarily disabled, for now it just moves out of bounds
                    needle_y = -100
                    clock.tick(17)
                    needle_x = cactus_init_x

        # set up cowboy and movement
        cowboy(cowboy_x, cowboy_y)
        cowboy_x += cowboy_x_change
        cowboy_y += cowboy_y_change
        
        # set up cactus
        cactus(cactus_x, cactus_y)

        # set up box and keep player confined within
        pygame.draw.rect(gameDisplay, WHITE, [box_x, box_y, box_width, box_height], 2)
        if cowboy_x > box_x + box_width - cowboy_width:
            cowboy_x = box_x + box_width - cowboy_width
        elif cowboy_x < box_x:
            cowboy_x = box_x
        if cowboy_y > box_y + box_height - cowboy_height:
            cowboy_y = box_y + box_height - cowboy_height
        elif cowboy_y < box_y:
            cowboy_y = box_y

        # purely visual graphics
        pygame.draw.line(gameDisplay, WHITE, (0, DISPLAY_HEIGHT * 0.60), (DISPLAY_WIDTH, DISPLAY_HEIGHT * 0.60))

        # display player HP and cactus HP bars
        for num in range(player_hp):
            hp_bar(bar_x + bar_width * num, bar_y)
        for num in range(cactus_hp):
            enemy_bar(enemy_bar_x + 7 * num, enemy_bar_y)

        # maintain a cross-hair sprite on the player's cursor that fires when mouse1 is pressed
        center_bal = 96/2
        crosshair(pygame.mouse.get_pos()[0] - center_bal, pygame.mouse.get_pos()[1] - center_bal)

        # generate horizontal needle fire attack
        needle(needle_x, needle_y)
        needle_x -= needle_speed
        if needle_x <= 0:
            needle_x = cactus_init_x
            needle_y = cactus_init_y + random.randint(-125, 75)
        if player_hitbox.colliderect(needle_hitbox) and not damaged:
            player_hp -= cactus_atk
            damaged = True

        # set up invulnerability period after taking damage
        if damaged:
            if invuln_time > 0:
                invuln_time -= 1
            if invuln_time <= 0:
                damaged = False
                invuln_time = cooldown

        # update entire display at a tick rate (FPS)
        pygame.display.update()
        clock.tick(FPS)


game_loop()
pygame.quit()
quit()
