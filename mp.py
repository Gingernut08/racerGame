import pygame
pygame.init()
WIDTH = 1920
HEIGHT = 1080
screen=pygame.display.set_mode((WIDTH,HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("intro")
clock=pygame.time.Clock()
bg=pygame.image.load("Textures/Untitled design (20).png")
bg = pygame.transform.rotate(bg, 90)
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
car = pygame.image.load("Textures/RGBBlackCar.png").convert_alpha()
car=pygame.transform.scale(car,(50,50))
carx=300
cary=500
running=True
while running:
    for event in pygame.event.get():
        if event.type ==pygame.QUIT:
            running=False 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    screen.blit(bg, (0,0))         
    screen.blit(car, (carx, cary))
    pygame.display.flip()
    clock.tick(60)
pygame.quit()