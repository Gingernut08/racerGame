import pygame
pygame.init()
width=1920
height=1080
canvas=pygame.display.set_mode((width,height))
pygame.display.set_caption("intro")
fps=pygame.time.Clock()
bg=pygame.image.load("Textures/Untitled design (20).png")
bg = pygame.transform.rotate(bg, 90)
car = pygame.image.load("Textures/RGBBlackCar.png").convert_alpha()
car=pygame.transform.scale(car,(50,50))
carx=300
cary=500
running=True
while running:
    for event in pygame.event.get():
        if event.type ==pygame.QUIT:
            running=False
    canvas.blit(bg,(0,0))           
    canvas.blit(car, (carx, cary))
    pygame.display.flip()
    fps.tick(60)
pygame.quit()