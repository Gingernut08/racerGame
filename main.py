from imports import pygame
from assets import Car
from math import sin, cos, radians

pygame.init()
WIDTH = 1920
HEIGHT = 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Car Colour Changer")


class track:
    def __init__(self):
        self.tileSize = 100
        self.dimensiotns = [18, 9]
        self.pos = ((WIDTH - self.tileSize * self.dimensiotns[0]) // 2, (HEIGHT - self.tileSize * self.dimensiotns[1]) // 2)
        self.shape = [["0" for _ in range(self.dimensiotns[0])] for _ in range(self.dimensiotns[1])]

trackOne = track()
print(trackOne.pos)

clock = pygame.time.Clock()
running = True
bgColor = (150, 150, 150)

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
    
    carTest.calculate_movement()
    
    # Draw to display
    screen.fill(bgColor)
    carTest.draw(screen)
    # update display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()