"""
This is a basic vertical scroll algorithm. It generates a list of Vector2 style
points that scroll downwards at a constant rate.
"""
from time import sleep
from random import randint, randrange
from math import tan
from VerticalScrollClass import Vector2


def fGameInit(positions):
    positions.append(Vector2(200, 0))
    positions.append(Vector2(200, 350))
    positions.append(Vector2(400, 465))
    positions.append(Vector2(400, 700))
    return positions


def fPrintCoords(positions):
    p_str = ""
    for p in positions:
            p_str += f"X: {p.coord_x} Y: {p.coord_y}"
            if p != positions[len(positions) - 1]:
                p_str += ", "
    print(p_str)


def fPointsDestruction(positions):
    """
    If the second from last position is off the screen, eliminate the last point.
    No need to draw to it anymore.
    """
    if positions[-2].coord_y > 700:
        del positions[-1]


def fPointsCreation(positions):
    """
    Limits: 
    X from 100 px to 400 px (range 300 px, which gives 150 px either side, + 100)
    Y max length 700 px, min length 300 px
    """
    if positions[0].coord_y >= 0:
        if positions[0].coord_x != positions[1].coord_x:
            positions.insert(0, Vector2(positions[0].coord_x, positions[0].coord_y - randrange(300, 700, 10)))
        else:
            new_x = 0
            if x_range := (400 - positions[0].coord_x) >= 150:
                # If x range >= 150, the new_x must increase from old_x.
                new_x = randrange(positions[0].coord_x + 40, 400, 10)
            else:
                new_x = randrange(100, positions[0].coord_x - 40, 10)

            new_y = positions[0].coord_y - int(tan(0.5236) * abs((new_x - positions[0].coord_x)))
            positions.insert(0, Vector2(new_x, new_y))


def fScroll(positions, increment):
    for i in range(len(positions)):
        positions[i].set_y(increment)
    return positions


def fGameLoop():
    expand_flag = False
    point_list = []
    fGameInit(point_list)

    while True:
        fScroll(point_list, 1)
        sleep(0.016)
        fPointsDestruction(point_list)
        fPointsCreation(point_list)
        fPrintCoords(point_list)
        

        
        



if __name__ == "__main__":
    fGameLoop()
