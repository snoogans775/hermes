import pygame

(width, height) = (300, 200)
screen = pygame.display.set_mode((width, height))
pygame.display.flip()

bg = pygame.Surface((20, 20))

while True:
    pygame.time.delay(100)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN: # if the user hits the mouse 
            print('Mouse Clicked')
        
        print(event)

    # This will draw text displaying the score to the screen.      
    screen.blit(bg, (0,0))
