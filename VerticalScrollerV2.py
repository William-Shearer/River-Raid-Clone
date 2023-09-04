from random import randint, randrange
import pygame

TAN_30 = 0.57735
TAN_60 = 1.73205

def fInitPoints(points):
    points.append(pygame.Vector2(300, 0))
    points.append(pygame.Vector2(300, 350))
    points.append(pygame.Vector2(300, 700))


def fScroll(points, speed):
    for p in points["bank"]:
        p.y += speed


def fPrintPoints(points):
    points_str = ""
    for p in points:
        points_str += f"X:{p.x} Y:{p.y}"
        if p != points[-1]:
            points_str += ", "

    print(points_str)

def fCreatePoints(points):
    if points["bank"][0].y >= 0:
        new_x = 0
        if points["bank"][0].x == points["bank"][1].x:
            if (points["bank"][0].x / 400) >= 0.5:
                # If the bank is more than 50% of the strip width, bank must narrow (river widen).
                new_x = points["bank"][0].x - int(0.4 * points["bank"][0].x) - randrange(0, int(0.6 * points["bank"][0].x))
            else:
                new_x = points["bank"][0].x + int((400 - points["bank"][0].x) * 0.4) + randrange(0, int((400 - points["bank"][0].x) * 0.6))
            new_y = -abs(int((new_x - points["bank"][0].x) * TAN_30))

        else:
            # This happens when a parallel bank is created.
            # Here, it must be checked if the bank width narrowed to LT 30% of 400.
            # If it did, also create an island.
            new_x = points["bank"][0].x
            # Make length of parallel bank a function of river width.
            new_y = -randrange(250, 450, 10)
                           

        points["bank"].insert(0, pygame.Vector2(new_x, new_y))




def fDestroyPoints(points):
    if points[-2].y >= 700:
        del points[-1]


def fDrawPoints(points, screen):
    for i in range(len(points["bank"]) - 1):
        pygame.draw.line(screen, "yellow", points["bank"][i], points["bank"][i + 1], 1)




def fGameLoop():

    clock = pygame.time.Clock()
    points = {"bank": [], "island": []}
    run_loop = True
    fInitPoints(points["bank"])
    pygame.init()
    screen = pygame.display.set_mode((1000, 700))


    while run_loop:
        fScroll(points, 1)
        fDestroyPoints(points["bank"])
        fCreatePoints(points)
        # fPrintPoints(bank_points)
        screen.fill("blue")
        fDrawPoints(points, screen)
        clock.tick(90)

        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_loop = False

    pygame.display.quit()
    pygame.quit()
    exit()


if __name__ == "__main__":
    fGameLoop()
