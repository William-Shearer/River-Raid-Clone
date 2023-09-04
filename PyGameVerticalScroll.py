"""
This is a basic vertical scroll algorithm. It generates a list of Vector2 style
points that scroll downwards at a constant rate.
"""
from time import sleep
from random import randint, randrange
from math import tan
import pygame

DARK_GREEN = pygame.Color(70, 160, 5)
"""
def fPrintCoords(positions):
    p_str = ""
    for p in positions:
            p_str += f"X: {p.x} Y: {p.y}"
            if p != positions[len(positions) - 1]:
                p_str += ", "
    print(p_str)
"""

def fGameInit(positions):
    
    positions.append(pygame.Vector2(200, 0))
    positions.append(pygame.Vector2(200, 350))
    positions.append(pygame.Vector2(400, 465))
    positions.append(pygame.Vector2(400, 700))
    return positions


def fDrawScreen(positions, screen):
    """
    for i in range(len(positions) - 1):
        point_a = (positions[i].x, positions[i].y)
        point_b = (positions[i + 1].x, positions[i + 1].y)
        pygame.draw.line(screen, "green", point_a, point_b, 3)
    """
    # Now, draw a polygon, instead.
    pygame.draw.polygon(screen, DARK_GREEN, positions, 0)
    inverse_positions = []
    for p in positions:
        inverse_point = pygame.Vector2(999 - p.x, p.y)
        inverse_positions.append(inverse_point)
    pygame.draw.polygon(screen, DARK_GREEN, inverse_positions, 0)



def fClipping(positions):
    screen_positions =[]
    new_x, horiz_len = 0, 0
    if positions[0].y < 0:
        if positions[1].x == positions[0].x:
            new_x = positions[0].x
        else:
            horiz_len = tan(1.0472) * positions[1].y 
            if positions[0].x > positions[1].x:
                new_x = positions[1].x + horiz_len
            else:
                new_x = positions[1].x - horiz_len
        screen_positions.append(pygame.Vector2(new_x, 0))
        # First point off screen done.
    
    # The rest of them that are on screen.
    for p in positions:
        if p.y >= 0 and p.y < 700:
            # This is just a straight copy of points that are on the screen.
            screen_positions.append(pygame.Vector2(p.x, p.y))
            # Done.
    
    # Now, the last point, if there is one off screen at the bottom. 
    # There is never more than one, point-destruction sees to that.
    # 699 is the last y coord on screen. Slice the last point. 
    # It is the same procedure as at the top of this function. 
    if positions[-1].y >= 700:
        if positions[-2].x == positions[-1].x:
            new_x = positions[-1].x
        else:
            horiz_len = tan(1.0472) * (699 - positions[-2].y)
            if positions[-1].x > positions[-2].x:
                new_x = positions[-2].x + horiz_len
            else:
                new_x = positions[-2].x - horiz_len
        screen_positions.append(pygame.Vector2(new_x, 699))
    # Finally, add the two corner points of the polygon that will be drawn.
    screen_positions.append(pygame.Vector2(0, 699))
    screen_positions.append(pygame.Vector2(0, 0))
    return screen_positions


def fPointsDestruction(positions):
    """
    If the second from last position is off the screen, eliminate the last point.
    No need to draw to it anymore.
    """
    if positions[-2].y > 700:
        del positions[-1]


def fPointsCreation(positions):
    """
    Limits: 
    X from 100 px to 400 px (range 300 px, which gives 150 px either side, + 100)
    Y max length 500 px, min length 300 px
    """
    if positions[0].y >= 0:
        if positions[0].x != positions[1].x:
            positions.insert(0, pygame.Vector2(positions[0].x, positions[0].y - randrange(300, 500, 10)))
        else:
            new_x = 0
            if (400 - positions[0].x) >= 150:
                new_x = randrange(positions[0].x + 80, 400, 10)
            else:
                new_x = randrange(100, positions[0].x - 80, 10)

            new_y = positions[0].y - int(tan(0.5236) * abs((new_x - positions[0].x)))
            positions.insert(0, pygame.Vector2(new_x, new_y))




def fScroll(positions, increment):
    for i in range(len(positions)):
        positions[i].y += increment
    return positions


def fGameLoop():
    running = True
    point_list = []
    speed = 0
    pygame.init()
    screen = pygame.display.set_mode((1000, 700))
    pygame.display.set_caption("River Raid")
    clock = pygame.time.Clock()

    fGameInit(point_list)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                key = pygame.key.name(event.key)
                if key == "up":
                    speed += 1
                if key == "down" and speed > 0:
                    speed -= 1

        fScroll(point_list, speed)
        # sleep(0.016)
        fPointsDestruction(point_list)
        fPointsCreation(point_list)
        # fPrintCoords(point_list)
        screen_points = fClipping(point_list)
        screen.fill("blue")
        fDrawScreen(screen_points, screen)
        clock.tick(90)
        pygame.display.flip()
        
    
    # Broken out of loop.
    pygame.display.quit()
    pygame.quit()
    exit()


        
        



if __name__ == "__main__":
    fGameLoop()
