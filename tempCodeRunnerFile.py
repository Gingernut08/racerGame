
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