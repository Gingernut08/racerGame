from imports import pygame, Image, os, time, sin, cos, radians

turnSpeed = 4
moveSpeed = 10
acceleration = 0.2
reverseAcceleration = 0.2
friction = 0.05

class Car:
    def __init__(self, size):
        self.movementKeys = [0, 0] # [1 = forward -1 = back, 1 = left -1 = right]
        self.movement = [0, 0]
        self.pos = pygame.Vector2(500, 500)
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
        self.turnTime = time.time()
        self.moveTime = time.time()
        
        # debug
        self.dotShown = False
        self.pivots = [pygame.Vector2(self.image.get_width() / 2, 0.2 * self.image.get_height()), pygame.Vector2(self.image.get_height() / 2)]
        self.pivotNum = 0

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

    def rotate(self, rotated_image, rotated_texture, screen):
        # Pivot point on the original image: bottom-centre
        pivot = self.pivots[self.pivotNum]

        # Offset from the image centre to the pivot
        centre = pygame.Vector2(
            self.image.get_width() / 2,
            self.image.get_height() / 2
        )
        offset = pivot - centre
        

        # Rotate the offset
        offset = offset.rotate(-self.angle)

        # Position the rotated image so the pivot is at self.pos
        rect = rotated_image.get_rect(center=self.pos + offset)
        texture_rect = rotated_texture.get_rect(center=self.pos + offset)

        return rect, texture_rect

    def draw(self, screen):
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        rotated_texture = pygame.transform.rotate(self.texture, self.angle)

        rect, texture_rect = self.rotate(rotated_image, rotated_texture, screen)
        screen.blit(rotated_image, rect)
        screen.blit(rotated_texture, texture_rect)
        if self.dotShown:
            pygame.draw.circle(screen, (255, 0, 0), self.pos, 5)

    def move_ammount(self, ammount):
        angle = radians(self.angle)
        
        forward = pygame.Vector2(
            -sin(angle),
            -cos(angle)
        )
        
        self.pos += forward * ammount

    def calculate_velocity(self):
        timeMoving = time.time() - self.moveTime
        if self.movementKeys[0] ==  1:
            self.movement[0] += acceleration
        elif self.movementKeys[0] ==  -1:
            self.movement[0] -= reverseAcceleration
        else:
            if self.movement[0] > 0:
                self.movement[0] -= friction
            elif self.movement[0] < 0:
                self.movement[0] += friction
        self.movement[0] = max(-moveSpeed, min(moveSpeed, self.movement[0]))

    def get_key_inputs(self):
        keys = pygame.key.get_pressed()
        keysJust = pygame.key.get_just_pressed()

        self.movementKeys[0] = 0
        self.movementKeys[1] = 0

        if keys[pygame.K_w]:
            self.movementKeys[0] += 1
        if keys[pygame.K_s]:
            self.movementKeys[0] -= 1

        if keys[pygame.K_a]:
            self.movementKeys[1] += 1
        if keys[pygame.K_d]:
            self.movementKeys[1] -= 1
        
        if keysJust[pygame.K_a] or keysJust[pygame.K_d]:
            self.turnTime = time.time()
        if keysJust[pygame.K_w] or keysJust[pygame.K_s]:
            self.moveTime = time.time()
        
        if pygame.key.get_just_released()[pygame.K_SPACE]:
            self.dotShown = not self.dotShown
        if pygame.key.get_just_released()[pygame.K_RETURN]:
            self.pivotNum += 1
            self.pivotNum %= 2

    def calculate_movement(self):
        
        angle = radians(self.angle)
    
        # Get vector in forward direction
        forward = pygame.Vector2(
            -sin(angle),
            -cos(angle)
        )
        
        self.get_key_inputs()
        self.angle += self.movementKeys[1] * (1 if self.movement[0] >= 0 else -1) * turnSpeed
        
        self.calculate_velocity()
        self.move_ammount(self.movement[0])
        # self.pos += forward * self.movementKeys[0] * moveSpeed