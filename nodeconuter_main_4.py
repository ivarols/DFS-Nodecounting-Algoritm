import pygame

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("DFS")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 156, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)


class square:

    def __init__(self, row, col, width, total_rows):

        self.neighbors = []
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.width = width
        self.total_rows = total_rows
        self.neighbor_is_node = []
        self.neighbor_node_is_passed = []

    def make_start(self):
        self.color = BLUE

    def make_node(self):
        self.color = BLACK

    def make_neighbor(self):
        self.color = PURPLE

    def make_traybackNode(self):
        self.color = YELLOW

    def make_passed_node(self):
        self.color = RED

    def make_current_node(self):
        self.color = ORANGE

    def is_node(self):
        return self.color == BLACK

    def is_neighbor(self):
        return self.color == PURPLE

    def is_traybackNode(self):
        return self.color == YELLOW

    def is_passed_node(self):
        return self.color == RED

    def reset(self):
        self.color = WHITE

    def get_pos(self):
        return self.row, self.col

    def draw(self, WIN):
        pygame.draw.rect(WIN, self.color, (self.x, self.y, self.width, self.width))

    def identify_neighbors(self, grid):

        self.neighbors = []

        if self.col > 0 and grid[self.row][self.col - 1].is_node():
            self.neighbors.append(grid[self.row][self.col - 1])

        if self.col < self.total_rows - 1 and grid[self.row][self.col + 1].is_node():
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.row > 0 and grid[self.row - 1][self.col].is_node():
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.row < self.total_rows - 1 and grid[self.row + 1][self.col].is_node():
            self.neighbors.append(grid[self.row + 1][self.col])

        if grid[0][0].is_node() and (grid[0][1] == grid[self.row][self.col] or grid[1][0] == grid[self.row][self.col]):
            self.neighbors.append(grid[0][0])


def algoritm(draw, rows, start, grid):
    current = start
    traybackNodes = []
    passed_nodes = []
    number_of_vertices = 0
    counted_vertices = [start.get_pos()]
    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        for neighbor in current.neighbors:

            if neighbor.is_passed_node():
                current.neighbors.remove(neighbor)
            if neighbor.is_traybackNode():
                current.neighbors.remove(neighbor)
            else:
                neighbor.make_neighbor()

        for neighbor in current.neighbors:
            if neighbor.get_pos() not in counted_vertices:
                counted_vertices.append(neighbor.get_pos())

        if current not in passed_nodes:
            passed_nodes.append(current)
        for node in passed_nodes:
            node.make_passed_node()

        if len(current.neighbors) >= 2:
            traybackNodes.append(current)
            current.make_traybackNode()

        if len(current.neighbors) == 0:
            if len(traybackNodes) < 1:
                for node in counted_vertices:
                    for node1 in counted_vertices:
                        if (node[0] == node1[0] + 1 and node[1] == node1[1]) or (node[0] == node1[0] and node[1] == node1[1] + 1):
                            number_of_vertices += 1

                print(f'The number of node in the graph is: {len(passed_nodes)}')
                print(f'The number  of vertices in the graph is: {number_of_vertices}')
                break
            current = traybackNodes[-1]
            traybackNodes.pop(-1)
        else:
            for neighbor in current.neighbors:
                current = neighbor
        draw()

def make_grid(width, rows):
    grid = []
    square_size = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            SQUARE = square(i, j, square_size, rows)
            grid[i].append(SQUARE)
    return grid


def draw_grid(WIN, rows, width):
    square_size = width // rows
    for i in range(rows):
        pygame.draw.line(WIN, BLACK, (0, i * square_size), (width, i * square_size), 1)
        for j in range(rows):
            pygame.draw.line(WIN, BLACK, (j * square_size, 0), (j * square_size, width), 1)


def draw(WIN, grid, rows, width):
    WIN.fill(WHITE)
    for row in grid:
        for square in row:
            square.draw(WIN)
    draw_grid(WIN, rows, width)
    pygame.display.update()


def get_clicked_pos(pos, rows, width):
    square_gap = width // rows
    y, x = pos

    row = y // square_gap
    col = x // square_gap

    return row, col


def main(WIN, width):
    rows = 20

    node = None
    start = False
    running = True
    started = False
    grid = make_grid(width, rows)

    while running:

        draw(WIN, grid, rows, width)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if started:
                continue

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, rows, width)
                square = grid[row][col]

                if not start:
                    start = square
                    start.make_start()

                elif square is not node and square is not start:
                    node = square
                    node.make_node()

            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, rows, width)
                square = grid[row][col]
                square.reset()

                if square == start:
                    start = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start:
                    for row in grid:
                        for square in row:
                            square.identify_neighbors(grid)
                    algoritm(lambda: draw(WIN, grid, rows, width), grid, start, square)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and start:
                    for row in grid:
                        for square in row:
                            square.reset()
                start = False


main(WIN, WIDTH)
