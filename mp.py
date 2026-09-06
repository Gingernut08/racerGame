import pygame
pygame.init
width=1920
height=1080
canvas=pygame.display.set_mode((width,height))
pygame.display.set_caption("intro")
fps=pygame.time.Clock()
bg=pygame.image.load("Textures\mainpage bg.svg")
car = pygame.image.load("Textures\RGBBlackCar.png").convert_alpha()
car=pygame.transform.scale(car,(50,50))
carx=300
cary=500
running=True
           
