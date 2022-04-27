import pygame
import random 
from time import sleep

pygame.init()

class Draw_info:
    #class attributes
    BLACK = 0, 0, 0
    BACKGROUND_COLOR = 100, 140, 150
    MENU_BG_COLOR = 80, 120, 120
    SWAP1 = 180, 250, 0
    SWAP2 = 250, 80, 0
    TITLE =100, 0, 100
    GREYS = []

    FONT = pygame.font.SysFont('calibri', 20)
    LARGE_FONT = pygame.font.SysFont('cansolas', 50)

    SIDE_PAD = 100
    LEFT_MENU = 200
    TOP_PAD = 150
    BOTTOM_PAD = 50

    def __init__(self, width, height, n, lst_max):
        self.width = width
        self.height = height
        self.n = n
        self. lst_max= lst_max
        self.lst = self.build_list()
        self.bar_width = round((self.width - self.SIDE_PAD - self.LEFT_MENU) / self.n)
        self.graph_height = self.height - self.TOP_PAD
        self.scale = self.graph_height / self.lst_max
        self.start_x = self.SIDE_PAD // 2 + self.LEFT_MENU

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
    menu_rect = (0,0,draw_info.LEFT_MENU, draw_info.height)
    pygame.draw.rect(draw_info.window, draw_info.MENU_BG_COLOR, menu_rect)

    title = draw_info.LARGE_FONT.render(f"{algo_name}", 1, draw_info.TITLE)
    draw_info.window.blit(title, (draw_info.width / 2 + draw_info.LEFT_MENU / 2 - title.get_width() / 2, 10))

    controls = draw_info.FONT.render("R: Reset     SPACE: Start Sort", 1, draw_info.BLACK)
    draw_info.window.blit(controls, (draw_info.width / 2 + draw_info.LEFT_MENU / 2 - controls.get_width() / 2, 45))

    sorting_str = [
        "I - Insertion Sort", 
        "B - Bubble Sort", 
        "Q - Quick Sort", 
        "M - Merge Sort",
        "S - Selection Sort",
        ]
    sorting = draw_info.FONT.render(sorting_str[0], 1, draw_info.BLACK)
    draw_info.window.blit(sorting, (30, 30))
    sorting = draw_info.FONT.render(sorting_str[1], 1, draw_info.BLACK)
    draw_info.window.blit(sorting, (30, 55))
    sorting = draw_info.FONT.render(sorting_str[2], 1, draw_info.BLACK)
    draw_info.window.blit(sorting, (30, 80))
    sorting = draw_info.FONT.render(sorting_str[3], 1, draw_info.BLACK)
    draw_info.window.blit(sorting, (30, 105))
    sorting = draw_info.FONT.render(sorting_str[4], 1, draw_info.BLACK)
    draw_info.window.blit(sorting, (30, 130))

    draw_list(draw_info)
    pygame.display.update()

def draw_list(draw_info, color_positions={}, clear_bg=False):
    lst = draw_info.lst
    if clear_bg:
        clear_rect = (draw_info.SIDE_PAD // 2 + draw_info.LEFT_MENU, draw_info.TOP_PAD, 
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



def quick_sort_wrapper(draw_info):
    quickSort(draw_info.lst, 0, draw_info.n - 1, draw_info)
    yield True

def partition(arr, low, high, draw_info):
    i = (low - 1)         # index of smaller element
    pivot = arr[high]     # pivot
 
    for j in range(low, high):
 
        # If current element is smaller
        # than or equal to pivot
        if arr[j] <= pivot:
         
            # increment index of
            # smaller element
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
            draw_list(draw_info, {i: draw_info.SWAP1, j: draw_info.SWAP2}, True)
 
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    draw_list(draw_info, {i + 1: draw_info.SWAP1, high: draw_info.SWAP2}, True)
    return (i + 1)
 
# The main function that implements QuickSort
# arr[] --> Array to be sorted,
# low --> Starting index,
# high --> Ending index
 
# Function to do Quick sort
def quickSort(arr, low, high, draw_info):
    if low < high:
 
        # pi is partitioning index, arr[p] is now
        # at right place
        pi = partition(arr, low, high, draw_info)
 
        # Separately sort elements before
        # partition and after partition
        quickSort(arr, low, pi-1, draw_info)
        quickSort(arr, pi + 1, high, draw_info)

    
def selection_sort(draw_info):
    lst = draw_info.lst
    for i in range(len(lst)):
        # Find the minimum element in remaining 
        # unsorted array
        min_idx = i
        for j in range(i+1, len(lst)):
            if lst[min_idx] > lst[j]:
                min_idx = j
                
        # Swap the found minimum element with 
        # the first element        
        sleep(.1)
        lst[i], lst[min_idx] = lst[min_idx], lst[i]
        draw_list(draw_info, {i: draw_info.SWAP1, min_idx: draw_info.SWAP2}, True)
    yield True


def merge_sort_wrapper(draw_info):
    mergeSort(draw_info.lst, draw_info)
    yield True
def mergeSort(a, draw_info):
    # start with least partition size of 2^0 = 1
    width = 1   
    n = len(a)                                         
    # subarray size grows by powers of 2
    # since growth of loop condition is exponential,
    # time consumed is logarithmic (log2n)
    while (width < n):
        # always start from leftmost
        l=0;
        while (l < n):
            r = min(l+(width*2-1), n-1)        
            m = min(l+width-1,n-1)
            # final merge should consider
            # unmerged sublist if input arr
            # size is not power of 2             
            merge(a, l, m, r, draw_info)
            l += width*2
        # Increasing sub array size by powers of 2
        width *= 2
    return a
# Merge Function
def merge(a, l, m, r, draw_info):
    n1 = m - l + 1
    n2 = r - m
    L = [0] * n1
    R = [0] * n2
    for i in range(0, n1):
        L[i] = a[l + i]
        draw_list(draw_info, {n1 * i: draw_info.SWAP1, l + i: draw_info.SWAP2}, True)
    for i in range(0, n2):
        draw_list(draw_info, {n2 * i: draw_info.SWAP1, l + i: draw_info.SWAP2}, True)
        R[i] = a[m + i + 1]

    i, j, k = 0, 0, l
    while i < n1 and j < n2:
        if L[i] <= R[j]:
            a[k] = L[i]
            draw_list(draw_info, {k: draw_info.SWAP1, n1 * i: draw_info.SWAP2}, True)
            i += 1
        else:
            a[k] = R[j]
            draw_list(draw_info, {k: draw_info.SWAP1, n2 * j: draw_info.SWAP2}, True)
            j += 1
        k += 1

    while i < n1:
        a[k] = L[i]
        draw_list(draw_info, {k: draw_info.SWAP1, n1 * i: draw_info.SWAP2}, True)
        i += 1
        k += 1

    while j < n2:
        a[k] = R[j]
        draw_list(draw_info, {k: draw_info.SWAP1, n2 * j: draw_info.SWAP2}, True)
        j += 1
        k += 1

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
    lst_max = 100

    draw_info = Draw_info(1000, 500, n, lst_max)

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
            elif event.key == pygame.K_q and not sorting:
                sorting_algorithm  = quick_sort_wrapper
                sorting_algo_name  = "Quick sort"
            elif event.key == pygame.K_m and not sorting:
                sorting_algorithm  = merge_sort_wrapper
                sorting_algo_name  = "Merge sort"
            elif event.key == pygame.K_s and not sorting:
                sorting_algorithm  = selection_sort
                sorting_algo_name  = "Selection sort"
  
  
            
    pygame.quit()

if __name__ == "__main__":
    main()
