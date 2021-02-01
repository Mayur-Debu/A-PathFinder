import pygame
from queue import PriorityQueue
import os
import random

"""
This software is a A* Pathfinding visualizer, that shows the working of the A* algort.
"""

os.environ['SDL_VIDEO_CENTERED'] = '1'

WIDTH = 700
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption('A* ALGORITHM VISUALIZER  (Dev: Mayur)')
# gameIcon = pygame.image.load('Images\\69750394.png')
# pygame.display.set_icon(gameIcon)

# Color codes for different color cubes for path visualizer
RED = (255, 0, 0)
GREEN = (0, 100, 0)
BLUE = (30, 144, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 140, 0)
GREY = (204, 229, 255)
TURQUOISE = (64, 224, 208)


class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width  # Determining the size of the individual cubes
        self.y = col * width  # Determining the size of the individual cubes
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        '''Returns the position of the node'''
        return self.row, self.col

    def is_closed(self):
        '''Denotes the visited node'''
        self.color == BLUE

    def is_open(self):
        '''Denotes the open node'''
        return self.color == TURQUOISE

    def is_barrier(self):
        '''Denotes the barrier node that cannot be visited'''
        return self.color == BLACK

    # def is_start(self):
    #     '''Denotes the start node'''
    #     return self.color == ORANGE
    #
    # def is_end(self):
    #     '''Denotes the end node'''
    #     return self.color == TURQUOISE

    def reset_spot(self):
        self.color = WHITE

    def reset(self):
        '''This function changes the color of the grid to white'''
        self.color = WHITE

    def make_start(self):
        self.color = RED

    def make_closed(self):
        self.color = BLUE

    def make_open(self):
        self.color = TURQUOISE

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = GREEN

    def make_path(self):
        self.color = YELLOW

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        '''checking for the barrier node in the neighbor'''
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():  # Down
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():  # Up
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():  # Right
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():  # Left
            self.neighbors.append(grid[self.row][self.col - 1])

    # def __lt__(self, other):
    #     '''lt represents the Less Than we'll use this method to compare the two nodes'''
    #     return False


def h(p1, p2):
    '''This is the heuristic function used in the algorithm...
    The distance between the two nodes is calculated using the manhattan's distance method,
    where the L distance between the two nodes is calculated.'''
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def reconstruct_path(came_from, current, draw):
    counter = -1
    current.make_end()
    while current in came_from:
        counter += 1
        current = came_from[current]
        current.make_path()
        draw()
    pygame.display.set_caption(f'The distance between the start and end is [{counter} Blocks].')
    current.make_start()


def algorithm(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return False

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    pygame.display.set_caption('ERROR: NO PATH FOUND')
    return False


def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)

    return grid


def draw_grid(win, rows, width):
    """ This function draws the grid"""
    GAP = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * GAP), (width, i * GAP))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * GAP, 0), (j * GAP, width))


def draw(win, grid, rows, width):
    win.fill(WHITE)

    for row in grid:
        for spot in row:
            spot.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()


def get_clicked_pos(pos, rows, width):
    """ This function returns the position of the mouse click event """
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col


def main(win, width):
    """ This is the driver function """
    ROWS = 50
    grid = make_grid(ROWS, width)

    start = None
    end = None

    run = True

    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:  # Left
                pygame.display.set_caption('A* ALGORITHM VISUALIZER  (Dev: Mayur)')
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                if not start and spot != end:
                    start = spot
                    start.make_start()

                elif not end and spot != start:
                    end = spot
                    end.make_end()

                elif spot != end and spot != start:
                    spot.make_barrier()



            elif pygame.mouse.get_pressed()[2]:  # Right
                pygame.display.set_caption('A* ALGORITHM VISUALIZER  (Dev: Mayur)')
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                spot.reset()
                if spot == start:
                    start = None
                elif spot == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    pygame.display.set_caption('A* ALGORITHM VISUALIZER  (Dev: Mayur)')
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                            if spot.color == TURQUOISE or spot.color == BLUE or spot.color == YELLOW:
                                spot.reset_spot()
                    algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)

                if event.key == pygame.K_c:
                    pygame.display.set_caption('A* ALGORITHM VISUALIZER  (Dev: Mayur)')
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)

                if event.key == pygame.K_r:
                    try:
                        for _ in range(250):
                            row = random.randint(0, 50)
                            col = random.randint(0, 50)
                            spot = grid[row][col]
                            if spot != end and spot != start:
                                spot.make_barrier()
                    except IndexError:
                        continue

    pygame.quit()


main(WIN, WIDTH)
