import pygame
from queue import PriorityQueue
import math

#create screen object
screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Path Visualizer")

# save RGB values of colors
LT_BLUE = (178, 178, 255) #initial color
BLUE = (0, 0, 255)   #visited color
PINK = (255, 0, 255)    #visiting color
BLACK = (0, 0, 0)   #obstacle color
WHITE = (255, 255, 255)
RED = (255, 0, 0)       #path color
ORANGE = (255, 110, 0)  #ending color
GREEN = (0, 185, 13)    #starting color

#create node class
class Node:
    def __init__(self, row, col, width, tot_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = LT_BLUE
        self.neighbors = []
        self.width = width
        self.tot_rows = tot_rows

    def get_pos(self):
        return self.row, self.col

    def visited(self):
        return self.color == BLUE

    def to_visit(self):
        return self.color == PINK

    def is_obst(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == GREEN

    def is_end(self):
        return self.color == ORANGE

    def reset(self):
        self.color = LT_BLUE

    def make_visited(self):
        self.color = BLUE

    def visit(self):
        self.color = PINK

    def make_obst(self):
        self.color = BLACK

    def make_start(self):
        self.color = GREEN

    def make_end(self):
        self.color = ORANGE

    def make_path(self):
        self.color = RED

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []

        if self.row < self.tot_rows - 1 and not grid[self.row + 1][self.col].is_obst(): #move down by 1 row
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_obst(): #move up by 1 row
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.tot_rows - 1 and not grid[self.row][self.col + 1].is_obst(): #move right by 1 column
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_obst(): #move left by 1 column
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False

def h(n1, n2):
    x_1, y_1 = n1
    x_2, y_2 = n2
    return abs(x_1 - x_2) + abs(y_1 - y_2)

def reconstr_path(prev,curr,draw):  #helper func to draw the path in reverse
    while curr in prev:
        curr = prev[curr]
        curr.make_path()
        draw()

def a_star(draw, grid, start, end):
    count = 0
    pq = PriorityQueue()

    pq.put((0, count, start))
    prev = {}
    g = {Node: float("inf") for row in grid for Node in row}
    g[start] = 0
    f = {Node: float("inf") for row in grid for Node in row}
    f[start] = h(start.get_pos(), end.get_pos())

    pq_hash = {start}

    for row in grid:
        for node in row:
            if(node.color == BLUE or node.color == RED):
                node.color = LT_BLUE

    while not pq.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        curr = pq.get()[2]
        pq_hash.remove(curr)

        if curr == end: #draw the path
            reconstr_path(prev,end,draw)
            start.make_start()
            end.make_end()
            return True

        for neighbor in curr.neighbors:
            temp = g[curr] + 1

            if temp < g[neighbor]:  #if there is a new lowest g-score
                prev[neighbor] = curr
                g[neighbor] = temp
                f[neighbor] = temp + h(neighbor.get_pos(), end.get_pos())

                if neighbor not in pq_hash:
                    count += 1
                    pq.put((f[neighbor], count, neighbor))
                    pq_hash.add(neighbor)

        draw()

        if curr != start:
            curr.make_visited()

    return False

def make_grid(rows, width):
    grid = []
    gap = width // rows

    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)

    return grid

def draw_grid(screen, rows, width):
    gap = width // rows

    for i in range(rows):
        pygame.draw.line(screen, WHITE, (0, i*gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(screen, WHITE, (j * gap, 0), (j * gap, width))

def draw(screen, grid, rows, width):
    screen.fill(LT_BLUE)

    for row in grid:
        for node in row:
            node.draw(screen)

    draw_grid(screen, rows, width)
    pygame.display.update()

def get_mouse_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col

