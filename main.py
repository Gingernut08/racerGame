from imports import pygame, os
from assets import Car, Track, WIDTH, HEIGHT
from math import sin, cos, radians, log2, ceil

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.mouse.set_visible(False)
pygame.display.set_caption("Car Colour Changer")

cursor = pygame.transform.scale(pygame.image.load(os.path.join("Textures", "tempCursor" + ".png")), (50, 50))


trackOne = Track(screen)
trackOne.update_states()

clock = pygame.time.Clock()
running = True
state = 1
bgColor = (150, 200, 150)

mouse = True

carTest = Car(100)

while running:
    # Get all events
    for event in pygame.event.get():
        # Quit if operating system close button pressed
        if event.type == pygame.QUIT:
            running = False
        # Get keypress events
        if event.type == pygame.KEYDOWN:
            # Quit if escape button pressed
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_p:
                state += 1
                state %= 2
            if event.key == pygame.K_e:
                recent = trackOne.export_shape()
            if event.key == pygame.K_i:
                trackOne.import_shape(recent)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if state == 1:
                trackOne.update_shape(pygame.mouse.get_pos())
    
    # Draw to display
    screen.fill(bgColor)
    
    if state == 0:
        carTest.calculate_movement()
        trackOne.draw()
        carTest.draw(screen)
    
    if state == 1:
        trackOne.draw()
        # Draw Mouse
        screen.blit(cursor, pygame.mouse.get_pos())
    
    
    # update display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()