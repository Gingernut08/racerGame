from imports import pygame
from assets import Car
from math import sin, cos, radians

pygame.init()
WIDTH = 1920
HEIGHT = 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Car Colour Changer")


trackShape = [
    [0, 0],
    [0, 1],
    [0, 2],
    [1, 2],
    [1, 3],
    [2, 3],
    [3, 3],
    [3, 2],
    [3, 1],
    [3, 0],
    [2, 0],
    [1, 0]
]

class track:
    def __init__(self, trackShape):
        self.tileSize = 100
        self.dimensiotns = [18, 9]
        self.pos = ((WIDTH - self.tileSize * self.dimensiotns[0]) // 2, (HEIGHT - self.tileSize * self.dimensiotns[1]) // 2)
        self.shape = [["00" for _ in range(self.dimensiotns[0])] for _ in range(self.dimensiotns[1])]
        for item in trackShape:
            self.shape[item[1]][item[0]] = "01"
        self.states = [row.copy() for row in self.shape]
    
    def get_around(self, x, y):
        around = [0] * 4
        if x == 0 or self.shape[y][x - 1] == "01":
            around[3] = 1
        if x + 1 == self.dimensiotns[0] or self.shape[y][x + 1] == "01":
            around[1] = 1
        if y == 0  or self.shape[y - 1][x] == "01":
            around[0] = 1
        if y + 1 == self.dimensiotns[1] or self.shape[y + 1][x] == "01":
            around[2] = 1
        return around
    
    def update_states(self):
        for y in range(self.dimensiotns[1]):
            for x in range(self.dimensiotns[0]):
                if self.shape[y][x] == "01":
                    around = self.get_around(x, y)
                    sum = 0
                    for i in range(4):
                        sum += (2 ** i) * around[i]
                    if sum < 10:
                        self.states[y][x] = "0" + str(sum)
                    else:
                        self.states[y][x] = str(sum)

trackOne = track(trackShape)
for row in trackOne.shape:
    print(" ".join(row))
print()

trackOne.update_states()
print()

for row in trackOne.states:
    print(" ".join(row))

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