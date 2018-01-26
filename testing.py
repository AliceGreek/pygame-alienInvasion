import pygame

pygame.init()
screen = pygame.display.set_mode((640, 480))

done = False
while not done:
    pygame.event.pump()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        done = True
    if keys[pygame.K_SPACE]:
        print("got here")
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            print("mouse at ", event.pos)
            