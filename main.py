import pygame
import random 

pygame.init()



class Draw_info:
    #class attributes
    BLACK = 0, 0, 0
    BACKGROUND_COLOR = 100, 140, 150
    SWAP1 = 180, 250, 0
    SWAP2 = 250, 80, 0
    TITLE =100, 0, 100
    GREYS = []
    FONT = pygame.font.SysFont('comicsans', 20)
    LARGE_FONT = pygame.font.SysFont('comicsans', 35)
    SIDE_PAD = 100
    TOP_PAD = 150

    def __init__(self, width, height, n, lst_max):
        self.width = width
        self.height = height
        self.n = n
        self. lst_max= lst_max
        self.lst = self.build_list()
        self.bar_width = round((self.width - self.SIDE_PAD) / self.n)
        self.graph_height = self.height - self.TOP_PAD
        self.scale = self.graph_height / self.lst_max
        self.start_x = self.SIDE_PAD // 2

        # create the pygame window
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Visualizer")
        self.build_greys()

    def build_greys(self):
        # returns list of tuples representing n shades (r,g,b) from darkest to lightest
        greys = []
        lightest = 250
        darkest = 10
        color_range = lightest - darkest
        for i in range(self.n + 1):
            rgb_val = darkest + ( color_range / self.n) * i
            greys.append((rgb_val, rgb_val, rgb_val))
        self.GREYS = greys

    def build_list(self):
        lst = []
        for _ in range(self.n):
            val = random.randint(0, self. lst_max)
            lst.append(val)
        return lst


def draw(draw_info, algo_name):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)

    title = draw_info.LARGE_FONT.render(f"{algo_name}", 1, draw_info.TITLE)
    draw_info.window.blit(title, (draw_info.width / 2 - title.get_width() / 2, 5))

    controls = draw_info.FONT.render("R: Reset     SPACE: Start Sort", 1, draw_info.BLACK)
    draw_info.window.blit(controls, (draw_info.width / 2 - controls.get_width() / 2, 45))

    sorting = draw_info.FONT.render("I - Insertion Sort     B - Bubble Sort", 1, draw_info.BLACK)
    draw_info.window.blit(sorting, (draw_info.width / 2 - sorting.get_width() / 2, 65))

    draw_list(draw_info)
    pygame.display.update()

def draw_list(draw_info, color_positions={}, clear_bg=False):
    lst = draw_info.lst
    if clear_bg:
        clear_rect = (draw_info.SIDE_PAD // 2, draw_info.TOP_PAD, 
                        draw_info.width - draw_info.SIDE_PAD, draw_info.height - draw_info.TOP_PAD)
        pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)
    for i, val in enumerate(lst):
        x = draw_info.start_x + i * draw_info.bar_width
        y = draw_info.TOP_PAD + (draw_info.graph_height - (draw_info.scale * val))


        proportion = int((val / draw_info.lst_max * draw_info.n))
        color = draw_info.GREYS[proportion]

        if i in color_positions:
            color = color_positions[i]
        
        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.bar_width, draw_info.height))

    if clear_bg:
        pygame.display.update()


def bubble_sort(draw_info):
    lst = draw_info.lst
    for i in range(len(lst) - 1):
        for j in range(len(lst) - 1 - i):
            num1 = lst[j]
            num2 = lst[j + 1]
            if (num1 > num2):
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
                draw_list(draw_info, {j: draw_info.SWAP1, j + 1: draw_info.SWAP2}, True)
                yield True
    return lst

def insertion_sort(draw_info):
    lst = draw_info.lst

    for i in range(1, len(lst)):
        current = lst[i]
        while i > 0 and lst[i - 1] > current:
            lst[i] = lst[i - 1]
            i -= 1
            lst[i] = current
            draw_list(draw_info, {i - 1: draw_info.SWAP1, i: draw_info.SWAP2}, True)
            yield True

             





# render the screen
# define the main event loop
def main():

    run = True
    sorting = False

    sorting_algorithm = bubble_sort
    sorting_algo_name = "Bubble Sort"
    sorting_algorithm_generator = None

    clock = pygame.time.Clock()

    n = 150
    lst_max = 100

    draw_info = Draw_info(1000, 600, n, lst_max)

    while run:
        clock.tick(60) #tps
        if sorting:
            try:
                next(sorting_algorithm_generator)
            except StopIteration:
                sorting = False
        else:
            draw(draw_info, sorting_algo_name)
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
                draw_info.lst = draw_info.build_list()
                sorting = False
            elif event.key == pygame.K_SPACE and not sorting:
                sorting = True
                sorting_algorithm_generator = sorting_algorithm(draw_info)
            elif event.key == pygame.K_i and not sorting:
                sorting_algorithm  = insertion_sort
                sorting_algo_name  = "Insertion Sort"
            elif event.key == pygame.K_b and not sorting:
                sorting_algorithm  = bubble_sort
                sorting_algo_name  = "Bubble Sort"
            
    pygame.quit()

if __name__ == "__main__":
    main()
