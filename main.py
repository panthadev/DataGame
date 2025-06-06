import pygame
import player
import boss



# pygame setup
pygame.init()
screen = pygame.display.set_mode((1250, 500))
clock = pygame.time.Clock()
running = True


boss_sprite = boss.Boss(screen, "assets/boss/boss_idle.png", 500, 100)
player_sprite = player.Player(screen,"assets/player/idle.png", boss_sprite)


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")




    # RENDER YOUR GAME HERE

    boss_sprite.update()

    player_sprite.update()

    




    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()