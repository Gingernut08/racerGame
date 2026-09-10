from imports import pygame, os
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
    [1, 0],
    [1, 1],
    [2, 1],
    [2, 2]
]

class track:
    def __init__(self, screen, trackShape):
        self.surface = screen
        self.tileSize = 100
        self.dimensiotns = [18, 10]
        self.pos = ((WIDTH - self.tileSize * self.dimensiotns[0]) // 2, (HEIGHT - self.tileSize * self.dimensiotns[1]) // 2)
        self.shape = [[1 for _ in range(self.dimensiotns[0])] for _ in range(self.dimensiotns[1])]
        # for item in trackShape:
        #     self.shape[item[1]][item[0]] = 1
        self.states = [[16 for _ in range(self.dimensiotns[0])] for _ in range(self.dimensiotns[1])]
        self.tiles = [pygame.transform.scale(
            pygame.image.load(os.path.join("Textures", "Track", str(i) + ".png")), (self.tileSize, self.tileSize)) for i in range(16)]
    
    def get_around(self, x, y):
        around = [0] * 4
        
        # this is wrong im dumb
        # if x == 0 or self.shape[y][x - 1] == "01":
        #     around[3] = 1
        # if x + 1 == self.dimensiotns[0] or self.shape[y][x + 1] == "01":
        #     around[1] = 1
        # if y == 0  or self.shape[y - 1][x] == "01":
        #     around[0] = 1
        # if y + 1 == self.dimensiotns[1] or self.shape[y + 1][x] == "01":
        #     around[2] = 1
        if x == 0 or self.shape[y][x - 1] == 0:
            around[3] = 1
        if x + 1 == self.dimensiotns[0] or self.shape[y][x + 1] == 0:
            around[1] = 1
        if y == 0  or self.shape[y - 1][x] == 0:
            around[0] = 1
        if y + 1 == self.dimensiotns[1] or self.shape[y + 1][x] == 0:
            around[2] = 1
        return around
    
    def update_states(self):
        self.states = [[16 for _ in range(self.dimensiotns[0])] for _ in range(self.dimensiotns[1])]
        for y in range(self.dimensiotns[1]):
            for x in range(self.dimensiotns[0]):
                if self.shape[y][x] == 1:
                    around = self.get_around(x, y)
                    sum = 0
                    for i in range(4):
                        sum += (2 ** i) * around[i]
                    self.states[y][x] = sum

    def draw(self):
        for y in range(self.dimensiotns[1]):
            for x in range(self.dimensiotns[0]):
                if self.states[y][x] != 16:
                    drawPos = (self.pos[0] + x * self.tileSize, self.pos[1] + y * self.tileSize)
                    self.surface.blit(self.tiles[self.states[y][x]], drawPos)







trackOne = track(screen, trackShape)
trackOne.update_states()

clock = pygame.time.Clock()
running = True
bgColor = (150, 200, 150)

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
    trackOne.draw()
    carTest.draw(screen)
    # update display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()