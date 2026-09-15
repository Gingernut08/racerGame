from imports import pygame, os
from assets import Car
from math import sin, cos, radians, log2, ceil

pygame.init()
WIDTH = 1920
HEIGHT = 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Car Colour Changer")

BASE = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz`¬!\"£$%^&*()-=_+[]#;',./\\{}~:@<>?|"
class track:
    def __init__(self, screen):
        self.surface = screen
        self.tileSize = 100
        self.dimensiotns = [18, 10]
        self.pos = ((WIDTH - self.tileSize * self.dimensiotns[0]) // 2, (HEIGHT - self.tileSize * self.dimensiotns[1]) // 2)
        self.shape = [[0 for _ in range(self.dimensiotns[0])] for _ in range(self.dimensiotns[1])]
        self.states = [[16 for _ in range(self.dimensiotns[0])] for _ in range(self.dimensiotns[1])]
        self.tiles = [pygame.transform.scale(
            pygame.image.load(os.path.join("Textures", "Track", str(i) + ".png")), (self.tileSize, self.tileSize)) for i in reversed(range(16))]
    
    def import_shape(self, endoceString):
        number = 0

        for char in endoceString:
            number = number * len(BASE) + BASE.index(char)

        binary = bin(number)[2:]

        total_bits = len(self.shape) * len(self.shape[0])
        binary = binary.zfill(total_bits)

        index = 0

        for y in range(len(self.shape)):
            for x in range(len(self.shape[y])):
                self.shape[y][x] = int(binary[index])
                index += 1

        self.update_states()


    def export_shape(self):
        binary = ''.join(
            str(value)
            for row in self.shape
            for value in row
        )

        number = int(binary, 2)

        if number == 0:
            return '0'.zfill(ceil((self.dimensiotns[0] * self.dimensiotns[1]) / log2(len(BASE))))

        endoceString = ''

        while number:
            number, remainder = divmod(number, len(BASE))
            endoceString = BASE[remainder] + endoceString

        return endoceString.zfill(ceil((self.dimensiotns[0] * self.dimensiotns[1]) / log2(len(BASE))))
        
    def update_shape(self, pos):
        index = [
            (pos[i] - self.pos[i]) // self.tileSize
            for i in range(2)
        ]
        self.shape[index[1]][index[0]] += 1
        self.shape[index[1]][index[0]] %= 2
        self.update_states()
    
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
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(
            overlay,
            (100, 100, 100, 50),
            (self.pos[0] - 1, self.pos[1] - 1, self.tileSize * self.dimensiotns[0] + 2, self.tileSize * self.dimensiotns[1] + 2),
            1
        )
        for y in range(self.dimensiotns[1]):
            for x in range(self.dimensiotns[0]):
                pygame.draw.rect(
                    overlay,
                    (100, 100, 100, 50),
                    (self.pos[0] + x * self.tileSize, self.pos[1] + y * self.tileSize, self.tileSize, self.tileSize),
                    1
                )
                if self.states[y][x] != 16:
                    drawPos = (self.pos[0] + x * self.tileSize, self.pos[1] + y * self.tileSize)
                    self.surface.blit(self.tiles[self.states[y][x]], drawPos)
        self.surface.blit(overlay, (0, 0))







trackOne = track(screen)
trackOne.update_states()

clock = pygame.time.Clock()
running = True
state = 1
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
        
    
    # update display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()