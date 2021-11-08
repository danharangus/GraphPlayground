import sys, pygame


pygame.init()
pygame.font.init()
font = pygame.font.SysFont('Arial', 60)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

screen = pygame.display.set_mode((1920, 1080))
pygame.display.set_caption("Graph Playground")
screen.fill(BLACK)
pygame.display.update()
loop = True

counter = 0
while loop:
    try:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = False
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                pygame.draw.circle(screen, WHITE, pos, 50, width=5)
                nodeText = font.render(str(counter), True, WHITE)
                counter = counter + 1
                screen.blit(nodeText, (pos[0] - 15, pos[1] - 35))
                pygame.display.update()

    except Exception as e:
        print(e)
        pygame.quit()
pygame.quit()
