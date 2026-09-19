import pygame
pygame.init()
screen=pygame.display.set_mode((0,0),pygame.FULLSCREEN)
(WIDTH,HEIGHT)=screen.get_size()
pygame.display.set_caption("intro")

clock=pygame.time.Clock()
bg=pygame.image.load("Textures/Untitled design (26).png")
bg = pygame.transform.rotate(bg, 90)
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
car = pygame.image.load("Textures/car/RGBBlackCar.png").convert_alpha()
car=pygame.transform.scale(car,(50,50))
car = pygame.transform.rotate(car,270)
carx=400
cary=430 #bottom=430 top=200
running=True
go=[]
while running:
    for event in pygame.event.get():
        if event.type ==pygame.QUIT:
            running=False 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    go.append((carx+10,cary+25))
    #vroom Time 
    carx+=3
    screen.blit(bg, (0,0))         
    
    if len(go)>1:
        pygame.draw.lines(screen,(255,0,1),False,go,10)
    screen.blit(car, (carx, cary))
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
#bgdoneee


