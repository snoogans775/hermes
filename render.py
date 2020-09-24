import pygame

while true:
    pygame.time.delay(100)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN: # if the user hits the mouse button
            run = False
            runner.falling = False
            runner.sliding = False
            runner.jumpin = False

    # This will draw text displaying the score to the screen.      
    win.blit(bg, (0,0))
