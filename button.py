import pygame

pygame.init()
screen = pygame.display.set_mode((600, 400), pygame.RESIZABLE)
screen2 = pygame.Surface((600, 400))
SIZE = pygame.display.Info()
WIDTH = SIZE.current_w
HEIGHT = SIZE.current_h
print(WIDTH, HEIGHT)
red = (255, 0, 0)
green = (0, 255, 0)


def button(screen, position, text, size=50, color="yellow", bg="darkblue"):
    """ draws a rectangle and some lines and then blits the text on it """
    font = pygame.font.SysFont("Arial", size)
    text_render = font.render(text, 1, color)
    x, y, w , h = text_render.get_rect()
    x, y = position
    # line(surface, color, (startingpoint), (endingpoint), thickness)
    pygame.draw.line(screen2, (150, 150, 150), (x, y), (x + w + 1, y), 5)
    pygame.draw.line(screen2, (150, 150, 150), (x, y - 2), (x, y + h), 5)
    pygame.draw.line(screen2, (50, 50, 50), (x, y + h), (x + w , y + h), 5)
    pygame.draw.line(screen2, (50, 50, 50), (x + w , y+h), [x + w , y], 5)
    # the rectangle that makes the background
    pygame.draw.rect(screen2, bg, (x, y, w + 2, h))
    return screen2.blit(text_render, (x, y))

def start():
    print("Ok, let's go")

def menu():
    """ This is the menu that waits you to click the s key to start """

    # Args: button(surface, (width, height), text)
    # added size, color and bg in version 2
    b1 = button(screen, (400, 300), "Quit", size=40, color="yellow", bg="black")
    b2 = button(screen, (500, 300), "Start", size=40)
    while True:
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                key_to_start = event.key == pygame.K_s or event.key == pygame.K_RIGHT or event.key == pygame.K_UP
                if key_to_start:
                    start()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if b1.collidepoint(pygame.mouse.get_pos()):
                    pygame.quit()
                elif b2.collidepoint(pygame.mouse.get_pos()):
                    start()
        screen.blit(pygame.transform.scale(screen2, (WIDTH, HEIGHT)), (0, 0))
        pygame.display.update()
    pygame.quit()

menu()
