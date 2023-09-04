import pygame as pg
from time import sleep
from math import tan, pi
from random import randrange, randint

TAN_30 = tan(20 * (pi / 180))
TAN_60 = tan(70 * (pi / 180))
DARK_GREEN = pg.Color(70, 160, 5)
DARK_BLUE = pg.Color(50, 65, 255)

def fInit(points):
    points["bank"].append(pg.Vector2(150, -450))
    points["bank"].append(pg.Vector2(150, 699))
    points["island"].append(pg.Vector2(450, -450))
    points["island"].append(pg.Vector2(450, 699))



def fPrintPoints(points):
    for list in points.values():
        p_str = ""
        for pnt in list:
            p_str += f"(X: {pnt.x} Y: {pnt.y}) "
        print(p_str)



def fScrollPoints(points, speed):
    for list in points.values():
        for pnt in list:
            pnt.y += speed



def fCreateBankPoints(bank_points):
    new_x, new_y = 0, 0
    if bank_points[0].y > -450:
        if bank_points[0].x == bank_points[1].x:
            bank_coeff = bank_points[0].x / 400
            if bank_coeff >= 0.7 or bank_coeff < 0.3:
                # If bank near edges, send to middle.
                new_x = randrange(120, 280, 10)
            
            else:
                # If around the middle, random widen or narrow bank, either way.
                rand_width = randrange(0, 60, 10)
                new_x = (rand_width + 340) if randint(0, 1) == 1 else rand_width

            new_y = -450 - int(abs(new_x - bank_points[0].x) * TAN_30)

        else:
            #Parallel segments.
            new_x = bank_points[0].x
            # Y length needs to be a function of the width of the river.
            # Narrow width, short length, and vice versa.
            new_y = -450 - randrange(int((450 - new_x) * 1.5), int((450 - new_x) * 2.5), 10)

        bank_points.insert(0, pg.Vector2(new_x, new_y))
        # This is okay.



def fCreateIslandPoints(points):
    """
    This gets a bit more complicated.
    """
    if points["island"][0].y >= -200:
        if points["bank"][0].x == points["bank"][1].x and points["bank"][0].x <= 120:

            island_start_y = points["bank"][1].y + randrange(-60, 0, 10)
            island_end_y = points["bank"][0].y + randrange(0, 60, 10)
            island_length = island_start_y - island_end_y
            # Island should be no more than 60% of available river width, but it might be
            # also limited by its length.
            width_limited_width = int(0.6 * (450 - points["bank"][0].x))
            # The island side should be at least 100px long.
            # On long islands, the following will produce a big number, that will later be discarded as
            # the island will in that case be width limited.
            length_limited_width = int(TAN_60 * ((island_length - 100) / 2))
            # The lesser of the two width limits is selected here.
            # Make sure these are integers.
            island_max_width = length_limited_width if (length_limited_width < width_limited_width) else width_limited_width
            # The minimum width will then be 50% of the selected max width.
            island_min_width = int(0.5 * island_max_width)
            # The actual island width is then selected randomly.
            # It will either be its max width or min width.
            island_width = island_max_width if (randint(0, 1) == 1) else island_min_width
            # island_width = randrange(island_min_width, island_max_width, 10)
            # Get the basic length of the island's parallel bank.
            island_parallel_length = island_length - int((TAN_30 * island_width) * 2)

            # If the island parallel length is greater than 450px, a bank step can be afforded around midway.
            # First, insert the end-points, however, in this order
            points["island"].insert(0, pg.Vector2(450, island_start_y)) # Will become index 1, next.
            points["island"].insert(0, pg.Vector2(450, island_end_y))

            # The next points should be inserted at index 1.
            points["island"].insert(1, pg.Vector2(450 - island_width, island_start_y - int(TAN_30 * island_width)))
            # Whether a bank step is feasible can now be checked.
            if island_parallel_length < 450:
                # Short island, no step. Just finish the island.
                points["island"].insert(1, pg.Vector2(450 - island_width, island_end_y + int(TAN_30 * island_width)))
            else:
                # Here is where the bank step is done.
                # The island width must be examined. If it was max, the next will be min, and vide versa.
                new_island_width = island_min_width if (island_width == island_max_width) else island_max_width
                first_parallel_length = int(island_parallel_length * (randint(3, 6) / 10))
                step_length = int(TAN_30 * (island_max_width - island_min_width))
                p_last_step = int(TAN_30 * island_width)
                points["island"].insert(1, pg.Vector2(450 - island_width, island_start_y - (first_parallel_length + p_last_step)))
                points["island"].insert(1, pg.Vector2(450 - new_island_width, island_start_y - (step_length + first_parallel_length + p_last_step)))
                points["island"].insert(1, pg.Vector2(450 - new_island_width, island_end_y + int(TAN_30 * new_island_width)))
            
        else:
            points["island"].insert(0, pg.Vector2(450, points["bank"][0].y + 50))


    
def fClipper(points, h):
    screen_points = {"bank":[], "island":[]}

    
    for key, pnt_list in points.items():
        i = 0
        # locate and plot the first on screen point:
        while pnt_list[i].y < 0:
            i += 1
        # print(i)
        # Create the first clipped point.
        if pnt_list[i].x == pnt_list[i - 1].x:
            # Parallel points
            screen_points[key].append(pg.Vector2(pnt_list[i].x + 50, 0))
        else:
            new_x = 0
            horiz_len = int(TAN_60 * pnt_list[i].y)
            if pnt_list[i].x > pnt_list[i - 1].x:
                new_x = (50 + pnt_list[i].x) - horiz_len
                # new_x = (((w - 1000) / 2) + pnt_list[i].x) - horiz_len
            else:
                new_x = 50 + pnt_list[i].x + horiz_len
                # new_x = ((w - 1000) / 2) + pnt_list[i].x + horiz_len
            screen_points[key].append(pg.Vector2(new_x, 0))
        
        # Then plot all but the last point...
        for j in range(i, len(pnt_list) - 1):
            screen_points[key].append(pg.Vector2(pnt_list[j].x + 50, pnt_list[j].y))
            # screen_points[key].append(pg.Vector2(pnt_list[j].x + ((w - 1000) / 2), pnt_list[j].y))
        # Finally, plot the last clipped point...
        if pnt_list[-1].x == pnt_list[-2].x:
            screen_points[key].append(pg.Vector2(pnt_list[-2].x + 50, (h - 1)))
            # screen_points[key].append(pg.Vector2(pnt_list[-2].x + ((w - 1000) / 2), (h - 1)))
        else:
            new_x = 0
            horiz_len = int(TAN_60 * ((h - 1) - pnt_list[-2].y))
            if pnt_list[-1].x > pnt_list[-2].x:
                new_x = 50 + pnt_list[-2].x + horiz_len
                # new_x = ((w - 1000) / 2) + pnt_list[-2].x + horiz_len
            else:
                new_x = 50 + (pnt_list[-2].x - horiz_len)
                # new_x = ((w - 1000) / 2) + (pnt_list[-2].x - horiz_len)
            screen_points[key].append(pg.Vector2(new_x, (h -1)))
        
        # Finish off with the screen coordinates
        if key == "bank":
            screen_points[key].append(pg.Vector2(0, (h - 1)))
            screen_points[key].append(pg.Vector2(0, 0))
        else:
            screen_points[key].append(pg.Vector2(500, (h - 1)))
            screen_points[key].append(pg.Vector2(500, 0))
            #screen_points[key].append(pg.Vector2(((w - 1000) / 2) + 500, (h - 1)))
            #screen_points[key].append(pg.Vector2(((w - 1000) / 2) + 500, 0))
    
    return screen_points






def fDestroyPoints(points, h):
    for list in points.values():
        try:
            if list[-2].y >= h:
                del list[-1]
        except IndexError:
            return False
    return True



def fDrawPoints(points, screen):
    for i in range(len(points["bank"]) - 1):
        pg.draw.line(screen, "green", points["bank"][i], points["bank"][i + 1], 1)
    
    for i in range(len(points["island"]) - 1):
        pg.draw.line(screen, "green", points["island"][i], points["island"][i + 1], 1)


def fPlotBackGround(screen_points, screen, h):
    screen.fill(DARK_BLUE)
    pg.draw.polygon(screen, DARK_GREEN, screen_points["bank"])
    pg.draw.polygon(screen, DARK_GREEN, screen_points["island"])

    rect = pg.Rect(0, 0, 500, (h - 1))
    flipped_half_screen = pg.transform.flip(screen.subsurface(rect).copy(), True, False)
    screen.blit(flipped_half_screen, (500, 0))


def fDrawSprite(pos, tr, screen):
    collided = False
    collide_list = [pg.Vector2(pos.x, pos.y - 8), pg.Vector2(pos.x - 12, pos.y), pg.Vector2(pos.x + 12, pos.y)]
    # Check bank collision
    for pnt in collide_list:
        if screen.get_at((int(pnt.x), int(pnt.y))) != DARK_BLUE:
            collided = True

    if collided == False:
        pg.draw.line(screen, "yellow", [pos.x, pos.y - 8], [pos.x, pos.y + 15], 6)
        if tr == 0.0:
            pg.draw.line(screen, "yellow", [pos.x - 15, pos.y + 8], [pos.x, pos.y], 6)
            pg.draw.line(screen, "yellow", [pos.x + 15, pos.y + 8], [pos.x, pos.y], 6)
            pg.draw.line(screen, "yellow", [pos.x - 9, pos.y + 20], [pos.x, pos.y + 16], 5)
            pg.draw.line(screen, "yellow", [pos.x + 9, pos.y + 20], [pos.x, pos.y + 16], 5)
        elif tr > 0.0:
            pg.draw.line(screen, "yellow", [pos.x - 13, pos.y + 7], [pos.x, pos.y - 1], 6)
            pg.draw.line(screen, "yellow", [pos.x + 12, pos.y + 9], [pos.x, pos.y + 1], 6)
            pg.draw.line(screen, "yellow", [pos.x - 8, pos.y + 19], [pos.x, pos.y + 16], 5)
            pg.draw.line(screen, "yellow", [pos.x + 8, pos.y + 21], [pos.x, pos.y + 16], 5)
        elif tr < 0.0:
            pg.draw.line(screen, "yellow", [pos.x - 12, pos.y + 9], [pos.x, pos.y + 1], 6)
            pg.draw.line(screen, "yellow", [pos.x + 13, pos.y + 7], [pos.x, pos.y - 1], 6)
            pg.draw.line(screen, "yellow", [pos.x - 8, pos.y + 21], [pos.x, pos.y + 16], 5)
            pg.draw.line(screen, "yellow", [pos.x + 8, pos.y + 19], [pos.x, pos.y + 16], 5)
        return True
    else:
        fDrawExplosion(pos, screen)
        return False
    

def fDrawExplosion(pos, screen):
    fire_colors = ("red", "yellow", "orange")
    for _ in range(20):
        fire = randint(0,2)
        x = randint(-15, 15)
        y = randint(-15, 15)
        debris = pg.Rect((int(pos.x + x), int(pos.y + y), 4, 4))
        pg.draw.rect(screen, fire_colors[fire], debris)
    sleep(0.1)
        # screen.set_at((int(pos.x) + randint(-20, 20), int(pos.y) + randint(-20, 20)), "yellow")    


def fGameLoop():
    points = {"bank": [], "island": []}
    speed = 2.0
    turn_rate = 0.0
    run_loop = True
    pg.init()
    fInit(points)
    screen = pg.display.set_mode((1000, 700)) #, pg.FULLSCREEN)
    w, h = pg.display.get_surface().get_size() 
    game_over = False
    clock = pg.time.Clock()
    player_pos = pg.Vector2(499, 650)

    while run_loop:
        # sleep(0.01)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run_loop = False
        
        if game_over == False:
            keys = pg.key.get_pressed()
            if keys[pg.K_LEFT]:
                if turn_rate > - 5.0:
                    turn_rate -= 0.05
            elif keys[pg.K_RIGHT]:
                if turn_rate < 5.0:
                    turn_rate += 0.05
            else:
                if turn_rate < -0.0:
                    turn_rate += 0.1
                elif turn_rate > 0.0:
                    turn_rate -= 0.1
                if turn_rate > -0.1 and turn_rate < 0.1:
                    turn_rate = 0.0  

            if keys[pg.K_UP]:
                if speed < 4:
                    speed += 0.05
            elif keys[pg.K_DOWN]:
                if speed > 1:
                    speed -= 0.5
            else:
                if speed > 2.0:
                    speed -= 0.1
                elif speed < 2:
                    speed += 0.1
                    

        fScrollPoints(points, round(speed))
        if not fDestroyPoints(points, h):
            run_loop = False
        fCreateBankPoints(points["bank"])
        fCreateIslandPoints(points)
        # fPrintPoints(points)
        screen_points = fClipper(points, h)
        # print(screen_points)
        # screen.fill("blue")
        # fDrawPoints(points, screen)
        fPlotBackGround(screen_points, screen, h)
        player_pos.x += turn_rate
        if not fDrawSprite(player_pos, round(turn_rate), screen):
            speed = 0
            turn_rate = 0.0
            game_over = True

        clock.tick(90)
        pg.display.flip()

    print("Quiting")
    pg.display.quit()
    pg.quit()
    exit()

if __name__ == "__main__":
    fGameLoop()