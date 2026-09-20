from imports import pygame, os, copy, Image
from assets import Car, Track, WIDTH, HEIGHT
from math import sin, cos, radians, log2, ceil, atan2, degrees
from statistics import mean

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.mouse.set_visible(False)
pygame.display.set_caption("Car Colour Changer")

cursor = pygame.transform.scale(pygame.image.load(os.path.join("Textures", "tempCursor" + ".png")), (50, 50))


trackOne = Track(screen)
trackOne.update_states()

clock = pygame.time.Clock()
running = True
bgColor = (150, 200, 150)

state = 0

with open(os.path.join("Saves", "tracks" + ".txt"), "r") as file:
    trackValues = [line.strip() for line in file]
trackValues.insert(0, "0000000000000000000000000000")
trackIndex = 0

class Cursor:
    def __init__(self, size):
        self.prevPos = [pygame.mouse.get_pos() for _ in range(5)]
        self.pos = pygame.mouse.get_pos()
        
        self.size = size
        self.colorOne = (255, 255, 0)
        self.colorTwo = (0, 255, 255)
        self.colorThree = (255, 0, 255)
        self.imageFile = os.path.join("Textures", "car", "RGBBlackCar.png")
        self.texture = pygame.transform.scale(
            pygame.image.load(os.path.join("Textures", "car", "CarTexture.png")).convert_alpha(),
            (self.size, self.size))
        self.change_colors()
        self.angle = 0
        
        
    def change_colors(self):
        # Load Image File
        img = Image.open(self.imageFile).convert("RGBA")
        pixData = img.load()
        # Iterate through all pixels in the image
        for y in range(img.size[1]):
            for x in range(img.size[0]):
                # If pixel is Red replace with colorOne
                if pixData[x, y] == (255, 0, 0, 255):
                    pixData[x, y] = (*self.colorOne, 255)
                # If pixel is Green replace with colorTwo
                if pixData[x, y] == (0, 255, 0, 255):
                    pixData[x, y] = (*self.colorTwo, 255)
                # If pixel if Blue replace with colorThree
                if pixData[x, y] == (0, 0, 255, 255):
                    pixData[x, y] = (*self.colorThree, 255)
        # Convert image back into pygame surface
        self.image = pygame.transform.scale(pygame.image.frombytes(
            img.tobytes(),
            img.size,
            img.mode
        ), 
        (self.size, self.size))

    def draw(self, screen):
        self.prevPos.append(self.pos)
        self.prevPos.pop(0)
        self.pos = pygame.mouse.get_pos()

        dx = [self.pos[0] - self.prevPos[i][0] for i in range(5)]
        dy = [self.prevPos[i][1] - self.pos[1] for i in range(5)]

        if dx != 0 or dy != 0:
            self.angles = [degrees(atan2(dy[i], dx[i])) - 90 for i in range(5)]
        self.angle = mean(self.angles)

        image = pygame.transform.rotate(self.image, self.angle)
        texture = pygame.transform.rotate(self.texture, self.angle)

        screen.blit(image, image.get_rect(center=self.pos))
        screen.blit(texture, texture.get_rect(center=self.pos))

textCursor = Cursor(20)

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
                text = trackOne.export_shape()
                with open(os.path.join("Saves", "tracks" + ".txt"), "a") as file:
                    file.write(text + "\n")
                trackValues.append(text)
                copy(text)
            if event.key == pygame.K_i:
                trackIndex += 1
                trackIndex %= len(trackValues)
                trackOne.import_shape(trackValues[trackIndex])
        if event.type == pygame.MOUSEBUTTONDOWN:
            if state == 1:
                trackOne.update_shape(pygame.mouse.get_pos())
    
    # Draw to display
    screen.fill(bgColor)
    
    trackOne.draw(state)
    if state == 1:
        textCursor.draw(screen)
        print(textCursor.angle)
        # screen.blit(cursor, pygame.mouse.get_pos())
    
    
    # update display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()