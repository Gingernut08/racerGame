from imports import pygame, os, copy, Image
from assets import Cursor, Car, Track, WIDTH, HEIGHT
from math import sin, cos, radians, log2, ceil, atan2, degrees
from statistics import mean

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load(os.path.join("audio", "carSoundtrack" + ".mp3"))
pygame.mixer.music.set_volume(0)
# pygame.mixer.music.play(-1)

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

cursor = Cursor(20)

music = True
musicVolume = 0
sfx = True
sfxVolume = 0

def adjust_music():
    global music, musicVolume
    if music:
        musicVolume += 0.01
    else:
        musicVolume -= 0.01
    musicVolume = min(max(musicVolume, 0), 1)
    pygame.mixer.music.set_volume(musicVolume)

def toggle_music():
    global music
    music = not music

def adjust_sfx():
    global sfx, sfxVolume
    



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
            if event.key == pygame.K_m:
                toggle_music()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if state == 1:
                trackOne.update_shape(pygame.mouse.get_pos())
    
    # Draw to display
    screen.fill(bgColor)
    
    trackOne.draw(state)
    if state == 1:
        cursor.draw(screen)
    
    # update display
    pygame.display.flip()
    adjust_music()
    clock.tick(60)

pygame.quit()