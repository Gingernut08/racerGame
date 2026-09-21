from imports import pygame, Image, os, time, sin, cos, radians, log2, ceil, degrees, atan2, pi, mean

WIDTH, HEIGHT = 1920, 1080


BASE = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz`¬!\"£$%^&*()-=_+[]#;',./\\{}~:@<>?|"


PADDING = [100, 200, 200, 100]

turnSpeed = 3
moveSpeed = 12
acceleration = 0.2
reverseAcceleration = 0.2
friction = 0.05
endTurn = 1.5
hudPadding = [10, 20]
bestTurnSpeed = 8
squeelSpeed = 9
screechTurnTimme = 0.7
turnAcceleration = 0.1
turnCentering = 20
minTurnSpeed = 0.05

def create_sfx(fileNames):
    sfxItems = {}
    for file in fileNames:
        sfxItems[file] = pygame.mixer.Sound(os.path.join("audio", "sfx", "screech" + ".mp3"))
        # sfxItems[file] = pygame.mixer.Sound(os.path.join("audio", "sfx", file + ".mp3"))
    return sfxItems

class Cursor:
    def __init__(self, size):
        self.prevPos = [pygame.mouse.get_pos() for _ in range(5)]
        self.pos = pygame.mouse.get_pos()
        
        self.size = size
        self.colorOne = (255, 255, 0)
        self.colorTwo = (255, 100, 0)
        self.colorThree = (255, 255, 255)
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
        mousePos = pygame.mouse.get_pos()

        self.prevPos.append(mousePos)
        self.prevPos.pop(0)

        angles = []

        for i in range(5):
            dx = mousePos[0] - self.prevPos[i][0]
            dy = self.prevPos[i][1] - mousePos[1]

            if dx != 0 or dy != 0:
                angles.append(degrees(atan2(dy, dx)) - 90)

        if angles:
            self.angle = mean(angles)

        self.pos = mousePos

        image = pygame.transform.rotate(self.image, self.angle)
        texture = pygame.transform.rotate(self.texture, self.angle)

        screen.blit(image, image.get_rect(center=self.pos))
        screen.blit(texture, texture.get_rect(center=self.pos))
class HUD:
    def __init__(self, car):
        pos = [WIDTH - PADDING[1] + 20, HEIGHT - PADDING[2] + 20]
        self.size = WIDTH - pos[0] - 20
        self.vert = [pos[0], pos[1] - 2 * self.size - 20, self.size, 2 * self.size]
        self.hori = [pos[0] - self.size, pos[1], 2 * self.size, self.size]
        self.speed = [pos[0], self.vert[1] - self.size - 20, self.size, self.size]
        self.speedDial = [self.speed[0] + self.size // 2, self.speed[1] + self.size // 2, self.size // 2 - 10]
        self.values = [0, 0]
        self.car = car
        self.speedo = 0
        self.speedoUpdateTime = 0.25
        self.updateSpeedo = time.time() - self.speedoUpdateTime
        self.arcStartTime = time.time()
        self.arcDuration = self.speedoUpdateTime * 2
    
    def drawNumber(self, screen, pos, size, value):
        if time.time() - self.updateSpeedo > self.speedoUpdateTime:
            self.speedo = 99 * value
            self.updateSpeedo = time.time()

        segmentWidth = 2 * size / 30
        segmentHeight = (size - segmentWidth) // 2

        # Negative values are red
        colour = (200, 0, 0) if self.speedo < -0.5 else (255, 255, 255)

        segment = pygame.Surface(
            (segmentWidth, segmentHeight),
            pygame.SRCALPHA
        )

        pygame.draw.polygon(
            segment,
            colour,
            (
                ((segmentWidth - 1) // 2, 0),
                (segmentWidth - 1, (segmentWidth - 1) // 2),
                (segmentWidth - 1, segmentHeight - 1 - (segmentWidth - 1) // 2),
                ((segmentWidth - 1) // 2, segmentHeight - 1),
                (0, segmentHeight - 1 - (segmentWidth - 1) // 2),
                (0, (segmentWidth - 1) // 2)
            )
        )

        horizontal = pygame.transform.rotate(segment, -90)

        segments = {
            0: "abcdef",
            1: "bc",
            2: "abdeg",
            3: "abcdg",
            4: "bcfg",
            5: "acdfg",
            6: "acdefg",
            7: "abc",
            8: "abcdefg",
            9: "abcdfg"
        }

        def drawDigit(x, digit):
            halfWidth = (segmentHeight - segmentWidth) / 2

            positions = {
                "a": (x, pos[1] - 2 * halfWidth),
                "b": (x + halfWidth + segmentWidth / 2, pos[1] - halfWidth),
                "c": (x + halfWidth + segmentWidth / 2, pos[1] + halfWidth),
                "d": (x, pos[1] + 2 * halfWidth),
                "e": (x - halfWidth - segmentWidth / 2, pos[1] + halfWidth),
                "f": (x - halfWidth - segmentWidth / 2, pos[1] - halfWidth),
                "g": (x, pos[1])
            }

            for name in segments[digit]:
                part = horizontal if name in "adg" else segment
                rect = part.get_rect(center=positions[name])
                screen.blit(part, rect)

        num = max(0, min(99, int(abs(self.speedo))))

        tens = num // 10
        ones = num % 10

        digitSpacing = size * 0.75

        drawDigit(pos[0] - digitSpacing / 2, tens)
        drawDigit(pos[0] + digitSpacing / 2, ones)
    
    def draw(self, screen):
        pygame.draw.rect(screen, (100, 100, 100), self.vert)
        pygame.draw.rect(screen, (100, 100, 100), self.hori)
        pygame.draw.rect(screen, (100, 100, 100), self.speed)

        pygame.draw.circle(screen, (150, 150, 150), self.speedDial[:2], self.speedDial[2])
        
        progress = (time.time() - self.arcStartTime) / self.arcDuration

        if progress >= 1:
            self.arcStartTime = time.time()
            progress = 0
        progress *= 2

        pygame.draw.arc(
            screen,
            (150, 175, 150),
            (
                self.speedDial[0] - self.speedDial[2],
                self.speedDial[1] - self.speedDial[2],
                self.speedDial[2] * 2,
                self.speedDial[2] * 2
            ),
            0.5 * pi - 2 * pi * min(progress, 1),
            0.5 * pi,
            2
        )
        if progress >= 1:
            pygame.draw.arc(
                screen,
                (150, 150, 150),
                (
                    self.speedDial[0] - self.speedDial[2],
                    self.speedDial[1] - self.speedDial[2],
                    self.speedDial[2] * 2,
                    self.speedDial[2] * 2
                ),
                0.5 * pi - 2 * pi * (max(progress, 1) - 1),
                0.5 * pi,
                2
            )

        self.drawNumber(screen, self.speedDial[:2], self.speedDial[2], self.values[1])
        
        if self.values[1] != 0:
            self.values[0] *= self.values[1] / abs(self.values[1])
        pygame.draw.rect(screen, (100, 200, 100), (
                                                    min(self.hori[0] + self.size - self.values[0] * (self.size - hudPadding[1]), self.hori[0] + self.size), 
                                                    self.hori[1] + hudPadding[0],
                                                    abs(self.values[0]) * (self.size - hudPadding[1]),
                                                    self.hori[3] - (2 * hudPadding[0])
                                                    ))
        pygame.draw.rect(screen, (100, 200, 100), (
                                                    self.vert[0] + hudPadding[0],
                                                    min(self.vert[1] + self.size - self.values[1] * (self.size - hudPadding[1]), self.vert[1] + self.size),
                                                    self.vert[2] - (2 * hudPadding[0]),
                                                    abs(self.values[1]) * (self.size - hudPadding[1])
                                                    ))
        if self.car.movementKeys[0] != 0:
            pygame.draw.rect(screen, (200, 200, 200), (
                                                        self.vert[0] + hudPadding[1] // 2,
                                                        self.vert[1] + self.size - (self.size - hudPadding[1] // 2) * self.car.movementKeys[0] - hudPadding[1] // 4,
                                                        self.vert[2] - 2 * hudPadding[0],
                                                        hudPadding[1] // 2
                                                        ))
        if self.car.movementKeys[1] != 0:
            pygame.draw.rect(screen, (200, 200, 200), (
                                                        self.hori[0] + self.size - (self.size - hudPadding[1] // 2) * self.car.movementKeys[1] - hudPadding[1] // 4,
                                                        self.hori[1] + hudPadding[1] // 2,
                                                        hudPadding[1] // 2,
                                                        self.hori[3] - 2 * hudPadding[0]
                                                        ))


class Track:
    def __init__(self, screen):
        self.surface = screen
        self.dimensions = [18, 10]
        tileSizes = [(WIDTH - (PADDING[1] + PADDING[3])) // self.dimensions[0], (HEIGHT - (PADDING[0] + PADDING[1])) // self.dimensions[1]]
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
    def import_shape(self, encodeString):
        number = 0

        for char in encodeString:
            number = number * len(BASE) + BASE.index(char)

        total_digits = self.dimensions[0] * self.dimensions[1]
        base4 = ""

        while number:
            number, remainder = divmod(number, 4)
            base4 = str(remainder) + base4

        base4 = base4.zfill(total_digits)

        index = 0

        for y in range(self.dimensions[1]):
            for x in range(self.dimensions[0]):
                self.shape[y][x] = int(base4[index])
                index += 1

        self.update_states()


    def export_shape(self):
        base4 = ''.join(
            str(value)
            for row in self.shape
            for value in row
        )

        number = int(base4, 4)

        length = ceil(
            len(base4) / log2(len(BASE))
        )

        encodeString = ""

        if number == 0:
            return "0" * length

        while number:
            number, remainder = divmod(number, len(BASE))
            encodeString = BASE[remainder] + encodeString

        return encodeString.zfill(length)
        
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
        self.hud = HUD(self)
        self.track = track
        self.movementKeys = [0, 0] # [1 = forward -1 = back, 1 = left -1 = right]
        self.movement = [0, 0]
        self.pos = pygame.Vector2(500, 500)
        self.angle = 0
        self.size = size
        self.colorOne = (255, 255, 0)
        self.colorTwo = (0, 255, 255)
        self.colorThree = (255, 0, 255)
        self.imageFile = os.path.join("Textures", "car", "RGBBlackCar.png")
        self.texture = pygame.transform.scale(
            pygame.image.load(os.path.join("Textures", "car", "CarTexture.png")).convert_alpha(),
            (self.size, self.size))
        self.change_colors()
        self.turnTime = time.time()
        self.moveTime = time.time()
        
        # debug
        self.dotShown = False
        self.pivots = [pygame.Vector2(self.image.get_width() / 2, 0.2 * self.image.get_height()), pygame.Vector2(self.image.get_height() / 2)]
        self.pivotNum = 0
        
        self.sfx = ["screech", "engine", "honk"]
        self.loopSfx = ["engine"]
        self.sounds = create_sfx(self.sfx)
        self.playing = {sfx: 0 for sfx in self.sfx}
        
        self.screechTime = 0
        self.lastTurnUpdate = time.time()
        self.turnSpeed = 0

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
        self.play_sfx()
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        rotated_texture = pygame.transform.rotate(self.texture, self.angle)

        rect, texture_rect = self.rotate(rotated_image, rotated_texture, screen)
        screen.blit(rotated_image, rect)
        screen.blit(rotated_texture, texture_rect)
        if self.dotShown:
            pygame.draw.circle(screen, (255, 0, 0), self.pos, 5)
        self.hud.draw(screen)

    def move_ammount(self, ammount):
        angle = radians(self.angle)
        
        forward = pygame.Vector2(
            -sin(angle),
            -cos(angle)
        )
        
        self.pos += forward * ammount

    def calculate_slowdown(self, velocity):
        value = 1.5
        # if not all([self.pos[i] < self.track.pos[i] and self.pos[i] > self.pos[i] + self.track.dimensions[i] * self.track.tileSize for i in range(2)]):
        index = [
                    int((self.pos[i] - self.track.pos[i]) // self.track.tileSize)
                    for i in range(2)
                ]
        if all([self.track.pos[i] < self.pos[i] and self.pos[i] < self.track.pos[i] + self.track.tileSize * self.track.dimensions[i] for i in range(2)]):
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

        if keys[pygame.K_RIGHT]:
            self.movementKeys[0] += 1
        if keys[pygame.K_LEFT]:
            self.movementKeys[0] -= 1
        if self.movementKeys[0] == 0:
            self.playing["engine"] = 0
        else:
            self.playing["engine"] = 1

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

    def play_sfx(self):
        for key in self.sfx:
            if self.playing[key] == 0:
                pass
                # self.sounds[key].stop()
            elif self.playing[key] == 1:
                if key in self.loopSfx:
                    # self.sounds[key].play(-1)
                    self.playing[key] = 2
                else:
                    print(key)
                    self.sounds[key].play()
                    self.playing[key] = 0

    # def getTurnAmount(self, speed):
    #     speed = abs(speed)
    #     if speed <= bestTurnSpeed:
    #         x = speed / bestTurnSpeed
    #         return turnSpeed * sin((x ** 1.5 * pi / 2))
    #     x = (speed - bestTurnSpeed) / (moveSpeed - bestTurnSpeed)
    #     finalTurnSpeed = turnSpeed - (turnSpeed - endTurn) * x ** 4
    #     turningTime = time.time() - self.turnTime
    #     finalTurnSpeed *= min(turningTime / turnAcceleration, 1)
    #     if finalTurnSpeed != 0 and speed >= squeelSpeed and time.time() - self.turnTime > screechTurnTimme:
    #         if time.time() - self.screechTime >= 0.1:
    #             self.sounds["screech"].play()
    #             self.screechTime = time.time()
    #     return finalTurnSpeed

    def get_max_turn(self, speed):
        speed = abs(speed)
        if speed <= bestTurnSpeed:
            x = speed / bestTurnSpeed
            return turnSpeed * sin((x ** 1.5 * pi / 2))
        x = (speed - bestTurnSpeed) / (moveSpeed - bestTurnSpeed)
        maxTurnSpeed = turnSpeed - (turnSpeed - endTurn) * x ** 4
        return maxTurnSpeed


    def calculate_turning(self):
        currentTime = time.time()
        dt = currentTime - self.lastTurnUpdate
        self.lastTurnUpdate = currentTime

        speed = self.movement[0]

        # No turning at very low speeds
        if abs(speed) < minTurnSpeed:
            self.turnSpeed = 0
            return

        maxTurnSpeed = self.get_max_turn(speed)

        # Prevent extremely small turn values
        if abs(maxTurnSpeed) < minTurnSpeed:
            self.turnSpeed = 0
            return

        # Steering direction is reversed when travelling backwards
        movementDirection = 1 if speed > 0 else -1

        if self.movementKeys[1] != 0:
            targetTurnSpeed = (
                self.movementKeys[1]
                * movementDirection
                * maxTurnSpeed
            )

            # Reach maximum steering in turnAcceleration seconds
            change = maxTurnSpeed * dt / turnAcceleration

            if self.turnSpeed < targetTurnSpeed:
                self.turnSpeed = min(
                    self.turnSpeed + change,
                    targetTurnSpeed
                )
            elif self.turnSpeed > targetTurnSpeed:
                self.turnSpeed = max(
                    self.turnSpeed - change,
                    targetTurnSpeed
                )

        else:
            # Return steering towards centre
            change = turnCentering * dt

            if self.turnSpeed > 0:
                self.turnSpeed = max(0, self.turnSpeed - change)
            elif self.turnSpeed < 0:
                self.turnSpeed = min(0, self.turnSpeed + change)

        # Snap tiny values to zero
        if abs(self.turnSpeed) < minTurnSpeed:
            self.turnSpeed = 0
        
        
    def calculate_movement(self):
        
        angle = radians(self.angle)
    
        # Get vector in forward direction
        forward = pygame.Vector2(
            -sin(angle),
            -cos(angle)
        )
        
        self.get_key_inputs()
        # angleChange = self.movementKeys[1] * (1 if self.movement[0] >= 0 else -1) * self.getTurnAmount(self.movement[0])
        self.calculate_turning()
        self.angle += self.turnSpeed
        
        self.calculate_velocity()
        self.move_ammount(self.movement[0])
        
        self.hud.values = [self.turnSpeed / turnSpeed, self.movement[0] / moveSpeed]
        # self.pos += forward * self.movementKeys[0] * moveSpeed