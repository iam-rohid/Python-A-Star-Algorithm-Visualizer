import pygame
import sys
import random
import math

# Grid variable
grid = []

# Rows and Columns
nodeSize = 14
rows = 60
cols = 60

# Select start and end point ---------------
startPoint = [10, 10]
endPoint = [rows-11, cols-11]
start = None
end = None

# Colors
black = (30, 30, 30)
white = (255, 255, 255)
red = (255, 30, 30)
blue = (30, 30, 255)
green = (30, 255, 30)
yellow = (255, 255, 30)

# height and width of the window
winHeight = nodeSize * rows
winWidth = nodeSize * cols
# Title of the window
caption = "A Star Visualizer"

# Initial setup for pygame ----------
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((winWidth, winHeight))
pygame.display.set_caption(caption)


# Node class -----------------


class Node:
    def __init__(self, x, y):
        self.value = "OPEN"
        self.x = x
        self.y = y
        self.fCost = 0
        self.gCost = 0
        self.hCost = 0
        self.color = white
        self.cameFrom = None
        self.neighbours = []

    def __str__(self):
        return self.value

    def show(self):
        pygame.draw.rect(
            screen, self.color,
            [self.x * nodeSize, self.y * nodeSize, nodeSize, nodeSize]
        )
        pygame.draw.rect(
            screen, white,
            [self.x * nodeSize, self.y * nodeSize, nodeSize, nodeSize], 1
        )

    def setColor(self):
        if self.value == "OPEN":
            self.color = white
        if self.value == "START":
            self.color = blue
        if self.value == "END":
            self.color = blue
        if self.value == "WALL":
            self.color = black
        if self.value == "PATH":
            self.color = yellow
        if self.value == "OPENSET":
            self.color = green
        if self.value == "CLOSESET":
            self.color = red

    def getPosition(self):
        return [self.x, self.y]

    def getNeighbours(self):
        x = self.x
        y = self.y
        # Left
        if x > 0:
            self.neighbours.append(grid[x-1][y])
        # top
        if y > 0:
            self.neighbours.append(grid[x][y-1])
        # right
        if x < cols-1:
            self.neighbours.append(grid[x+1][y])
        # bottom
        if y < rows-1:
            self.neighbours.append(grid[x][y+1])

        # Diagonal Path --------------
        # # top left
        # if x > 0 and y > 0:
        #     self.neighbours.append(grid[x-1][y-1])
        # # bottom right
        # if x < cols-1 and y < rows-1:
        #     self.neighbours.append(grid[x+1][y+1])
        # # bottom left
        # if x > 0 and y < rows-1:
        #     self.neighbours.append(grid[x-1][y+1])
        # # top right
        # if x < cols-1 and y > 0:
        #     self.neighbours.append(grid[x+1][y-1])

        return self.neighbours

# This function use to change value and color of the given node


def changeTo(node, value):
    node.value = value
    node.setColor()

# Genarete random walls on the grid


def randomWalls():
    i = 0
    while i < (rows * cols)/3:
        x = int(random.random() * rows)
        y = int(random.random() * cols)
        changeTo(grid[x][y], "WALL")
        i += 1

# Adding the given startPoint and endPoint to the grid


def setStartAndEnd(a, b):
    global start, end
    # Start
    start = grid[a[0]][a[1]]
    changeTo(start, "START")
    # End
    end = grid[b[0]][b[1]]
    changeTo(end, "END")

# It randomly select a start point and a end point on the grid


def randomStartAndEnd():
    global start, end

    # Start
    a = int(random.random() * rows)
    b = int(random.random() * cols)
    start = grid[a][b]
    changeTo(start, "START")
    # End
    a = int(random.random() * rows)
    b = int(random.random() * cols)
    end = grid[a][b]
    changeTo(end, "END")


# Set grid based on cols and rows and each grid will be a Node obj
def setGrid():
    x = 0
    while x < rows:
        y = 0
        col = []
        while y < cols:
            col.append(Node(x, y))
            y += 1
        grid.append(col)
        x += 1
    randomWalls()
    randomStartAndEnd()
    # setStartAndEnd(startPoint, endPoint)


setGrid()


# Astar ---------------------------------
openSet = [start]
closeSet = []
path = []

pathFound = False
noPathFound = False

# Heuristic Function to find a stright distance between two points


def heuristic(a, b):
    xDiff = a[0] - b[0]
    yDiff = a[1] - b[1]
    distance = math.sqrt(xDiff*xDiff + yDiff*yDiff)
    return distance

# Main A* Algorithm -----------------------------------------


def Astar():
    global pathFound, noPathFound
    global openSet, closeSet
    if len(openSet) > 0:
        current = openSet[0]
        for node in openSet:
            if node.fCost < current.fCost:
                current = node

        if current == end:
            temp = current
            while temp.cameFrom != start:
                temp = temp.cameFrom
                path.append(temp)
            pathFound = True

        # Add current to the closeSet and remove current from openSet
        closeSet.append(current)
        openSet.remove(current)

        # For COloring and animation --------------
        if current != start and current != end:
            changeTo(current, "CLOSESET")

        neighbours = current.getNeighbours()
        for neighbour in neighbours:
            if neighbour not in closeSet and neighbour.value != "WALL":
                # For COloring and animation --------------
                if neighbour != start and neighbour != end:
                    changeTo(neighbour, "OPENSET")

                # Checking if the neighbour is diagonal or not ---------------
                if current.x == neighbour.x or current.y == neighbour.y:
                    temp_gCost = current.gCost + 1
                else:
                    temp_gCost = current.gCost + 1.4

                if neighbour in openSet:
                    if temp_gCost < neighbour.gCost:
                        neighbour.cameFrom = current
                        neighbour.gCost = temp_gCost
                        neighbour.hCost = heuristic(
                            neighbour.getPosition(),
                            end.getPosition()
                        )
                        neighbour.fCost = neighbour.gCost + neighbour.hCost
                else:
                    neighbour.cameFrom = current
                    neighbour.gCost = temp_gCost
                    neighbour.hCost = heuristic(
                        neighbour.getPosition(),
                        end.getPosition()
                    )
                    neighbour.fCost = neighbour.gCost + neighbour.hCost
                    openSet.append(neighbour)
    else:
        print("No Solution")
        noPathFound = True


def gridShow():
    for row in grid:
        for col in row:
            col.show()


i = 0
# Main loop for pygame ---------------
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(white)
    gridShow()

    # Animating the final path
    if pathFound:
        changeTo(path[i], "PATH")
        i -= 1
        if i < 0:
            i = 0

    # A star algorithm
    if pathFound != True and noPathFound != True:
        Astar()
        i = len(path)-1

    pygame.display.flip()
    clock.tick(60)
