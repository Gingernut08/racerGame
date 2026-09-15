from imports import pygame, Image, os, time, sin, cos, radians, log2, ceil, pi, hypot

WIDTH, HEIGHT = 1920, 1080


BASE = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz`¬!\"£$%^&*()-=_+[]#;',./\\{}~:@<>?|"


PADDING = [100, 200, 200, 100]

turnSpeed = 6
moveSpeed = 15
acceleration = 0.2
reverseAcceleration = 0.2
friction = 0.05
endTurn = 1.5





class Track:
    def __init__(self, screen):
        self.surface = screen
        self.dimensions = [18, 10]
        tileSizes = [(WIDTH - (PADDING[1] + PADDING[3])) // self.dimensions[0], (HEIGHT - (PADDING[0] + PADDING[1])) // self.dimensions[1]]
        print(tileSizes)
        if tileSizes[0] > tileSizes[1]:
            self.tileSize = tileSizes[1]
            self.pos = (PADDING[3] * (WIDTH - self.tileSize * self.dimensions[0]) / (PADDING[1] + PADDING[3]), PADDING[0])
        else:
            self.tileSize = tileSizes[0]
            self.pos = (PADDING[3], PADDING[0] * (HEIGHT - self.tileSize * self.dimensions[1]) / (PADDING[0] + PADDING[2]))
        self.shape = [[0 for _ in range(self.dimensions[0])] for _ in range(self.dimensions[1])]
        self.states = [[16 for _ in range(self.dimensions[0])] for _ in range(self.dimensions[1])]
        self.tiles = [pygame.transform.scale(
            pygame.image.load(os.path.join("Textures", "Track", str(i) + ".png")), (self.tileSize, self.tileSize)) for i in reversed(range(16))]
        self.car = Car(self.tileSize // 2, self)
    
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
            return '0'.zfill(ceil((self.dimensions[0] * self.dimensions[1]) / log2(len(BASE))))

        endoceString = ''

        while number:
            number, remainder = divmod(number, len(BASE))
            endoceString = BASE[remainder] + endoceString

        return endoceString.zfill(ceil((self.dimensions[0] * self.dimensions[1]) / log2(len(BASE))))
        
    def update_shape(self, pos):
        index = [
            int((pos[i] - self.pos[i]) // self.tileSize)
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
        # if x + 1 == self.dimensions[0] or self.shape[y][x + 1] == "01":
        #     around[1] = 1
        # if y == 0  or self.shape[y - 1][x] == "01":
        #     around[0] = 1
        # if y + 1 == self.dimensions[1] or self.shape[y + 1][x] == "01":
        #     around[2] = 1
        if x == 0 or self.shape[y][x - 1] == 0:
            around[3] = 1
        if x + 1 == self.dimensions[0] or self.shape[y][x + 1] == 0:
            around[1] = 1
        if y == 0  or self.shape[y - 1][x] == 0:
            around[0] = 1
        if y + 1 == self.dimensions[1] or self.shape[y + 1][x] == 0:
            around[2] = 1
        return around
    
    def update_states(self):
        self.states = [[16 for _ in range(self.dimensions[0])] for _ in range(self.dimensions[1])]
        for y in range(self.dimensions[1]):
            for x in range(self.dimensions[0]):
                if self.shape[y][x] == 1:
                    around = self.get_around(x, y)
                    sum = 0
                    for i in range(4):
                        sum += (2 ** i) * around[i]
                    self.states[y][x] = sum

    def draw(self, state):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(
            overlay,
            (100, 100, 100, 50),
            (self.pos[0] - 1, self.pos[1] - 1, self.tileSize * self.dimensions[0] + 2, self.tileSize * self.dimensions[1] + 2),
            1
        )
        for y in range(self.dimensions[1]):
            for x in range(self.dimensions[0]):
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
        if state == 0:
            self.car.calculate_movement()
            self.car.draw(self.surface)


class Car:
    def __init__(self, size, track):
        self.track = track
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

    def calculate_slowdown(self, velocity):
        index = [
                    int((self.pos[i] - self.track.pos[i]) // self.track.tileSize)
                    for i in range(2)
                ]
        value = 1 - self.track.shape[index[1]][index[0]]
        return velocity - value * ((velocity) / moveSpeed)

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
        self.movement[0] = max(-moveSpeed, min(moveSpeed, self.calculate_slowdown(self.movement[0])))

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

    def getTurnAmount(self, velocity):
        speed = hypot(*velocity)
        

        x = min(speed / moveSpeed, 1)

        rise = sin((x ** 1.5) * pi / 2)

        return turnSpeed * rise - (turnSpeed - endTurn) * x**4

    def calculate_movement(self):
        
        angle = radians(self.angle)
    
        # Get vector in forward direction
        forward = pygame.Vector2(
            -sin(angle),
            -cos(angle)
        )
        
        self.get_key_inputs()
        self.angle += (
            self.movementKeys[1]
            * (1 if self.movement[0] >= 0 else -1)
            * self.getTurnAmount(self.movement)
        )
        
        self.calculate_velocity()
        self.move_ammount(self.movement[0])
        # self.pos += forward * self.movementKeys[0] * moveSpeed