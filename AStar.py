import math

grid = []

cols = 20
rows = 20

startPoint = [0, 0]
endPoint = [19, 19]

start = None
end = None


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


def setstartAndEndPoint():
    global start, end
    start = grid[startPoint[1]][startPoint[0]]
    end = grid[endPoint[1]][endPoint[0]]

    start.value = " S "
    end.value = " E "


class Node:
    def __init__(self, x, y):
        self.value = " ᛫ "
        self.x = x
        self.y = y
        self.fCost = 0
        self.gCost = 0
        self.hCost = 0
        self.cameFrom = None
        self.neighbours = []

    def __str__(self):
        return self.value

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
        # top left
        if x > 0 and y > 0:
            self.neighbours.append(grid[x-1][y-1])
        # bottom right
        if x < cols-1 and y < rows-1:
            self.neighbours.append(grid[x+1][y+1])
        # bottom left
        if x > 0 and y < rows-1:
            self.neighbours.append(grid[x-1][y+1])
        # top right
        if x < cols-1 and y > 0:
            self.neighbours.append(grid[x+1][y-1])

        return self.neighbours


setGrid()
setstartAndEndPoint()


# A star Path finding Algorithm
def AStar():
    openSet = [start]
    closeSet = []
    path = []

    # heuristic function to calculet the stright distence from given a point to b point

    def heuristic(a, b):
        xDiff = a[0] - b[0]
        yDiff = a[1] - b[1]
        distance = math.sqrt(xDiff*xDiff + yDiff*yDiff)
        return distance

    while len(openSet) > 0:
        # Find the lowest fCost node from the openSet
        current = openSet[0]
        for node in openSet:
            if node.fCost < current.fCost:
                current = node

        if current == end:
            print('found Path')
            temp = current
            path.append(temp)
            while temp.cameFrom != start:
                temp = temp.cameFrom
                temp.value = "   "
                path.append(temp)
            return path

        # Add current to the closeSet and remove from openSet
        closeSet.append(current)
        openSet.remove(current)

        # Adding current node's neighbours
        neighbours = current.getNeighbours()

        # Checking each neighbours of current
        for neighbour in neighbours:
            if neighbour not in closeSet:
                if current.x == neighbour.x or current.y == neighbour.y:
                    temp_gCost = current.gCost + 1
                else:
                    temp_gCost = current.gCost + 1.4

                if neighbour in openSet:
                    if temp_gCost < neighbour.gCost:
                        neighbour.cameFrom = current
                        neighbour.gCost = temp_gCost
                        neighbour.hCost = heuristic(
                            neighbour.getPosition(), end.getPosition())
                        neighbour.fCost = neighbour.gCost + neighbour.hCost
                else:
                    neighbour.cameFrom = current
                    neighbour.gCost = temp_gCost
                    neighbour.hCost = heuristic(
                        neighbour.getPosition(), end.getPosition())
                    neighbour.fCost = neighbour.gCost + neighbour.hCost
                    openSet.append(neighbour)


path = AStar()

# Printing the final grid -----------
for a in grid:
    for b in a:
        print(b, end="")
    print('')
