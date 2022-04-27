import math
import pygame
import random 
from time import sleep

pygame.init()



class Draw_info:
    #class attributes
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    BG_COLOR = 100, 140, 150
    GREEN = 0, 255, 0
    RED = 255, 0, 0
    GREY = 128, 128, 128
    BACKGROUND_COLOR = BG_COLOR
    GRADIENTS = []
    FONT = pygame.font.SysFont('comicsans', 20)
    LARGE_FONT = pygame.font.SysFont('comicsans', 40)
    SIDE_PAD = 100
    TOP_PAD = 150


    def __init__(self, width, height, lst, n, max_posib):
        self.width = width
        self.height = height
        self.n = n
        self.max_posib = max_posib

        # create the pygame window
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Visualizer")
        self.set_list(lst)
        self.build_color_gradient()
    

    def set_list(self, lst):
        self.lst = lst
        self.min_value = min(lst)
        self.max_value = max(lst)
        self.bar_width = round((self.width - self.SIDE_PAD) / len(lst))
        self.graph_height = self.height - self.TOP_PAD
        self.scale = self.graph_height / self.max_posib

        self.bar_height = math.floor((self.graph_height) / (self.max_value - self.min_value))
        self.start_x = self.SIDE_PAD // 2

    def build_color_gradient(self):
        # returns list of tuples representing n shades (r,g,b) from darkest to lightest
        gradients = []
        lightest = 220
        darkest = 20
        color_range = lightest - darkest
        for i in range(self.n + 1):
            rgb_val = darkest + ( color_range / self.n) * i
            gradients.append((rgb_val, rgb_val, rgb_val))
        self.GRADIENTS = gradients

def build_list(n, max_val):
    lst = []
    for _ in range(n):
        val = random.randint(0, max_val)
        lst.append(val)
    return lst


def draw(draw_info, n):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)

    controls = draw_info.FONT.render("R: Reset     SPACE: Start Sort", 1, draw_info.BLACK)
    draw_info.window.blit(controls, (draw_info.width / 2 - controls.get_width() / 2, 5))

    sorting = draw_info.FONT.render("I - Insertion Sort     B - Bubble Sort", 1, draw_info.BLACK)
    draw_info.window.blit(sorting, (draw_info.width / 2 - sorting.get_width() / 2, 35))

    draw_list(draw_info, n)
    pygame.display.update()

def draw_list(draw_info, n, color_positions={}, clear_bg=False):
    lst = draw_info.lst
    if clear_bg:
        clear_rect = (draw_info.SIDE_PAD // 2, draw_info.TOP_PAD, 
                        draw_info.width - draw_info.SIDE_PAD, draw_info.height - draw_info.TOP_PAD)
        pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)
    for i, val in enumerate(lst):
        x = draw_info.start_x + i * draw_info.bar_width
        #y = draw_info.height - (val - draw_info.min_value) * draw_info.bar_height
        y = draw_info.TOP_PAD + (draw_info.graph_height - (draw_info.scale * val))


        proportion = int((val / draw_info.max_value) * draw_info.n)
        color = draw_info.GRADIENTS[proportion]

        if i in color_positions:
            color = color_positions[i]
        
        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.bar_width, draw_info.height))

    if clear_bg:
        pygame.display.update()


def bubble_sort(draw_info, n):
    lst = draw_info.lst

    for i in range(len(lst) - 1):
        for j in range(len(lst) - 1 - i):
            num1 = lst[j]
            num2 = lst[j + 1]

            if (num1 > num2):
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
                draw_list(draw_info, n, {j: draw_info.GREEN, j + 1: draw_info.RED}, True)
                yield True
    return lst

# render the screen
# define the main event loop
def main():

    run = True
    sorting = False


    sorting_algorithm = bubble_sort
    sorting_algo_name = "Bubble Sort"
    sorting_algorithm_generator = None

    clock = pygame.time.Clock()

    n = 100
    max_val = 100

    lst = build_list(n, max_val)
    draw_info = Draw_info(1000, 600, lst, n, max_val)

    while run:
        #sleep(.1)
        clock.tick(60) #tps
        if sorting:
            try:
                next(sorting_algorithm_generator)
            except StopIteration:
                sorting = False
        else:
            draw(draw_info, n)
        pygame.display.update()
        for event in pygame.event.get(): 
        # Returns a list of all the events that have occured since the last loop
        # It gives it to us in the event variable. We can the check the event variable
        # for specific events
            if event.type == pygame.QUIT:
                run = False
            if event.type != pygame.KEYDOWN:
                continue
            if event.key == pygame.K_r:
                lst = build_list(n, max_val)
                draw_info.set_list(lst)
                sorting = False
            elif event.key == pygame.K_SPACE and not sorting:
                sorting = True
                sorting_algorithm_generator = sorting_algorithm(draw_info, n)
    pygame.quit()

if __name__ == "__main__":
    main()
