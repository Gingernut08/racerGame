from imports import pygame, Image, os, sin, cos, radians

turnSpeed = 5
moveSpeed = 5

class Car:
    def __init__(self, size):
        self.movement = [0, 0]
        self.pos = [500, 500]
        self.angle = 1
        self.size = size
        self.colorOne = (255, 255, 0)
        self.colorTwo = (0, 255, 255)
        self.colorThree = (255, 0, 255)
        self.imageFile = os.path.join("Textures", "RGBBlackCar.png")
        self.texture = pygame.transform.scale(
            pygame.image.load(os.path.join("Textures", "CarTexture.png")).convert_alpha(),
            (self.size, self.size))
        self.change_colors()

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
        # rotated = pygame.transform.rotate(self.image, self.angle)
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        rotated_texture = pygame.transform.rotate(self.texture, self.angle)

        rect = rotated_image.get_rect(center=self.pos)
        screen.blit(rotated_image, rect)

        texture_rect = rotated_texture.get_rect(center=self.pos)
        screen.blit(rotated_texture, texture_rect)

    def move_ammount(self, ammount):
        angle = radians(self.angle)
        
        forward = pygame.Vector2(
            -sin(angle),
            -cos(angle)
        )
        
        self.pos += forward * ammount


    def calculate_movement(self):
        
        angle = radians(self.angle)
    
        forward = pygame.Vector2(
            -sin(angle),
            -cos(angle)
        )
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.movment[1] = 1
            self.angle += turnSpeed
        elif keys[pygame.K_d]:
            self.movment[1] = -1
            self.angle -= turnSpeed
        else:
            self.movment[1] = 0
        if keys[pygame.K_w]:
            self.movment[0] = 1
            self.move_ammount(moveSpeed)
        elif keys[pygame.K_s]:
            self.movment[0] = -1
            self.move_ammount(-moveSpeed)
        else:
            self.movment[0] = 0