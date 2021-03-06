import pygame
import random
from time import sleep

pygame.init()


class Draw_info:
    TEXT_COLOR = 0, 0, 0
    TITLE_COLOR = 240, 240, 240
    BACKGROUND_COLOR = 100, 140, 150
    MENU_BG_COLOR = 80, 120, 120
    I_COLOR = 180, 250, 0
    J_COLOR = 250, 80, 0
    GREYS_COLOR_LIST = []

    FONT = pygame.font.SysFont("calibri", 20)
    LARGE_FONT = pygame.font.SysFont("cansolas", 50)

    SIDE_PAD = 100
    MENU_WIDTH = 200
    TOP_PAD = 75
    BOTTOM_PAD = 50

    def __init__(self, width, height, n, lst_max):
        self.width = width
        self.height = height
        self.n = n
        self.lst_max = lst_max
        self.lst = self.build_list()
        self.GREYS_COLOR_LIST = self.build_greys()
        self.bar_width = round((self.width - self.SIDE_PAD - self.MENU_WIDTH) / self.n)
        self.graph_height = self.height - self.TOP_PAD
        self.scale = self.graph_height / self.lst_max
        self.start_x = self.SIDE_PAD // 2 + self.MENU_WIDTH

        # create the pygame window
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Visualizer")

    def build_greys(self):
        # returns list of tuples representing n shades (r,g,b) from darkest to lightest
        greys = []
        lightest = 250
        darkest = 10
        color_range = lightest - darkest
        for i in range(self.n + 1):
            rgb_val = darkest + (color_range / self.n) * i
            greys.append((rgb_val, rgb_val, rgb_val))
        return greys

    def build_list(self):
        lst = []
        for _ in range(self.n):
            val = random.randint(0, self.lst_max)
            lst.append(val)
        return lst


def draw_window(info, algo_name):
    info.window.fill(info.BACKGROUND_COLOR)
    menu_rect = (0, 0, info.MENU_WIDTH, info.height)
    pygame.draw.rect(info.window, info.MENU_BG_COLOR, menu_rect)

    title = info.LARGE_FONT.render(f"{algo_name}", 1, info.TITLE_COLOR)
    info.window.blit(
        title,
        (info.width / 2 + info.MENU_WIDTH / 2 - title.get_width() / 2, 10),
    )

    menu_text = [
        "I - Insertion Sort",
        "B - Bubble Sort",
        "Q - Quick Sort",
        "M - Merge Sort",
        "S - Selection Sort",
        "H - Heap Sort",
    ]
    controls_text = [
        "R - Reset",
        "SPACE - Start",
    ]

    def render_menu_option(option_str, x, y):
        if option_str[4:] == algo_name:
            option = info.FONT.render(option_str, 1, info.TITLE_COLOR)
        else:
            option = info.FONT.render(option_str, 1, info.TEXT_COLOR)
        info.window.blit(option, (x, y))

    for i in range(len(menu_text)):
        render_menu_option(menu_text[i], 20, 20 + i * 30)

    for i in range(len(controls_text)):
        render_menu_option(controls_text[i], 20, 20 + len(menu_text * 30) + 30 + i * 30)

    draw_list(info)
    pygame.display.update()


def draw_list(info, swap_positions={}, clear_bg=False):
    lst = info.lst
    if clear_bg:
        clear_rect = (
            info.SIDE_PAD // 2 + info.MENU_WIDTH,
            info.TOP_PAD,
            info.width - info.SIDE_PAD,
            info.height - info.TOP_PAD,
        )
        pygame.draw.rect(info.window, info.BACKGROUND_COLOR, clear_rect)

    for i, val in enumerate(lst):
        x = info.start_x + i * info.bar_width
        y = info.TOP_PAD + (info.graph_height - (info.scale * val))

        proportion = int((val / info.lst_max * info.n))
        color = info.GREYS_COLOR_LIST[proportion]

        if i in swap_positions:
            color = swap_positions[i]

        pygame.draw.rect(info.window, color, (x, y, info.bar_width, info.height))

    if clear_bg:
        pygame.display.update()


##############################################################################
# Sorting algorithm definitions
##############################################################################
def bubble_sort(info):
    lst = info.lst
    for i in range(len(lst) - 1):
        for j in range(len(lst) - 1 - i):
            num1 = lst[j]
            num2 = lst[j + 1]
            if num1 > num2:
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
                draw_list( info, {j: info.I_COLOR, j + 1: info.J_COLOR}, True,)
                yield True
    return lst


def insertion_sort(info):
    lst = info.lst

    for i in range(1, len(lst)):
        current = lst[i]
        while i > 0 and lst[i - 1] > current:
            lst[i] = lst[i - 1]
            i -= 1
            lst[i] = current
            draw_list( info, {i - 1: info.I_COLOR, i: info.J_COLOR}, True,)
            yield True


def quick_sort_wrapper(info):
    quickSort(info.lst, 0, info.n - 1, info)
    yield True


def partition(arr, low, high, info):

    sleep(0.2)
    i = low - 1  # index of smaller element
    pivot = arr[high]  # pivot

    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
            draw_list(info, {i: info.I_COLOR, j: info.J_COLOR}, True)

    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    draw_list(info, {i + 1: info.I_COLOR, high: info.J_COLOR}, True)
    return i + 1


def quickSort(arr, low, high, info):
    if low < high:
        pi = partition(arr, low, high, info)
        quickSort(arr, low, pi - 1, info)
        quickSort(arr, pi + 1, high, info)


def selection_sort(info):
    lst = info.lst
    for i in range(len(lst)):
        min_idx = i
        for j in range(i + 1, len(lst)):
            if lst[min_idx] > lst[j]:
                min_idx = j
        sleep(0.1)
        lst[i], lst[min_idx] = lst[min_idx], lst[i]
        draw_list(info, {i: info.I_COLOR, min_idx: info.J_COLOR}, True)
    yield True


def merge_sort_wrapper(info):
    mergeSort(info.lst, info)
    yield True


def mergeSort(a, info):
    width = 1
    n = len(a)
    while width < n:
        l = 0
        while l < n:
            r = min(l + (width * 2 - 1), n - 1)
            m = min(l + width - 1, n - 1)
            merge(a, l, m, r, info)
            l += width * 2
        width *= 2
    return a


def merge(a, l, m, r, info):
    n1 = m - l + 1
    n2 = r - m
    L = [0] * n1
    R = [0] * n2
    for i in range(0, n1):
        L[i] = a[l + i]
        draw_list( info, {n1 * i: info.I_COLOR, l + i: info.J_COLOR}, True,)
    for i in range(0, n2):
        draw_list(
            info, {n2 * i: info.I_COLOR, l + i: info.J_COLOR}, True,)
        R[i] = a[m + i + 1]

    i, j, k = 0, 0, l
    while i < n1 and j < n2:
        if L[i] <= R[j]:
            a[k] = L[i]
            draw_list( info, {k: info.I_COLOR, n1 * i: info.J_COLOR}, True,)
            i += 1
        else:
            a[k] = R[j]
            draw_list( info, {k: info.I_COLOR, n2 * j: info.J_COLOR}, True,)
            j += 1
        k += 1

    while i < n1:
        a[k] = L[i]
        draw_list(info, {k: info.I_COLOR, n1 * i: info.J_COLOR}, True)
        i += 1
        k += 1

    while j < n2:
        a[k] = R[j]
        draw_list(info, {k: info.I_COLOR, n2 * j: info.J_COLOR}, True)
        j += 1
        k += 1


def heap_sort_wrapper(info):
    lst = info.lst
    heapify(lst, len(lst), 0, info)
    heapSort(info.lst, info)
    yield True


def heapify(arr, n, i, info):
    sleep(0.025)
    largest = i  # Initialize largest as root
    l = 2 * i + 1  # left = 2*i + 1
    r = 2 * i + 2  # right = 2*i + 2
    if l < n and arr[largest] < arr[l]:
        largest = l
    if r < n and arr[largest] < arr[r]:
        largest = r
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]  # swap
        draw_list(info, {i: info.I_COLOR, largest: info.J_COLOR}, True)
        heapify(arr, n, largest, info)


def heapSort(arr, info):
    sleep(0.025)
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i, info)
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]  # swap
        draw_list(info, {i: info.I_COLOR, 0: info.J_COLOR}, True)
        heapify(arr, i, 0, info)


##############################################################################
# main
##############################################################################
def main():
    # render the screen
    # define the main event loop
    n = 100
    lst_max = 100
    run = True
    sorting = False

    algorithm = bubble_sort
    algo_name = "Bubble Sort"
    algorithm_generator = None

    clock = pygame.time.Clock()

    info = Draw_info(1000, 500, n, lst_max)

    while run:
        clock.tick(60)  # tps
        if sorting:
            try:
                next(algorithm_generator)
            except StopIteration:
                sorting = False
        else:
            draw_window(info, algo_name)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type != pygame.KEYDOWN:
                continue
            if event.key == pygame.K_r:
                info.lst = info.build_list()
                sorting = False
            elif event.key == pygame.K_SPACE and not sorting:
                sorting = True
                algorithm_generator = algorithm(info)
            elif event.key == pygame.K_i and not sorting:
                algorithm = insertion_sort
                algo_name = "Insertion Sort"
            elif event.key == pygame.K_b and not sorting:
                algorithm = bubble_sort
                algo_name = "Bubble Sort"
            elif event.key == pygame.K_q and not sorting:
                algorithm = quick_sort_wrapper
                algo_name = "Quick Sort"
            elif event.key == pygame.K_m and not sorting:
                algorithm = merge_sort_wrapper
                algo_name = "Merge Sort"
            elif event.key == pygame.K_s and not sorting:
                algorithm = selection_sort
                algo_name = "Selection Sort"
            elif event.key == pygame.K_h and not sorting:
                algorithm = heap_sort_wrapper
                algo_name = "Heap Sort"
    pygame.quit()


if __name__ == "__main__":
    main()
