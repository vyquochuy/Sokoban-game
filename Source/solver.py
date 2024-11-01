import collections
import copy
import os
import time

class DFSSolver:
    def __init__(self, matrix, stone_weights):
        self.stone_weights = stone_weights
        self.maxRowLength = max(len(row) for row in matrix)
        self.lines = len(matrix)
        self.boxRobot = []
        self.wallsStorageSpaces = []
        self.possibleMoves = {'U': [-1, 0], 'R': [0, 1], 'D': [1, 0], 'L': [0, -1]}
        self.completed = 0
        self.visitedMoves = []
        self.queue = collections.deque([])
        self.path = []

        for i in range(self.lines):
            self.boxRobot.append(['-'] * self.maxRowLength)
            self.wallsStorageSpaces.append(['-'] * self.maxRowLength)

        for i in range(self.lines):
            for j in range(len(matrix[i])):
                if matrix[i][j] == '$' or matrix[i][j] == '@':
                    self.boxRobot[i][j] = matrix[i][j]
                    self.wallsStorageSpaces[i][j] = ' '
                elif matrix[i][j] == '.' or matrix[i][j] == '#':
                    self.wallsStorageSpaces[i][j] = matrix[i][j]
                    self.boxRobot[i][j] = ' '
                elif matrix[i][j] == ' ':
                    self.boxRobot[i][j] = ' '
                    self.wallsStorageSpaces[i][j] = ' '
                elif matrix[i][j] == '*':
                    self.boxRobot[i][j] = '$'
                    self.wallsStorageSpaces[i][j] = '.'
                elif matrix[i][j] == '+':
                    self.boxRobot[i][j] = '@'
                    self.wallsStorageSpaces[i][j] = '.'

    def solve(self):
        print("Solving using DFS")
        time_start = time.perf_counter()

        movesList = []
        source = [self.boxRobot, movesList]
        if self.boxRobot not in self.visitedMoves:
            self.visitedMoves.append(self.boxRobot)
        self.queue.append(source)
        robot_x = -1
        robot_y = -1

        while len(self.queue) != 0 and self.completed == 0:
            temp = self.queue.popleft()
            curPosition = temp[0]
            movesTillNow = temp[1]

            # Locate robot position
            for i in range(self.lines):
                for j in range(self.maxRowLength):
                    if curPosition[i][j] == '@':  # Assume '@' is the robot symbol
                        robot_y = j
                        robot_x = i
                        break
                else:
                    continue
                break

            for key in self.possibleMoves:
                robotNew_x = robot_x + self.possibleMoves[key][0]
                robotNew_y = robot_y + self.possibleMoves[key][1]

                # Check if new robot position is within bounds
                if 0 <= robotNew_x < self.lines and 0 <= robotNew_y < self.maxRowLength:
                    curPositionCopy = copy.deepcopy(curPosition)
                    movesTillNowCopy = copy.deepcopy(movesTillNow)

                    # Check if the robot is trying to push a box (assuming '$' is the box)
                    if curPositionCopy[robotNew_x][robotNew_y] == '$':
                        boxNew_x = robotNew_x + self.possibleMoves[key][0]
                        boxNew_y = robotNew_y + self.possibleMoves[key][1]

                        # Check box's new position is within bounds
                        if 0 <= boxNew_x < self.lines and 0 <= boxNew_y < self.maxRowLength:
                            if curPositionCopy[boxNew_x][boxNew_y] == '.' or self.wallsStorageSpaces[boxNew_x][boxNew_y] == '#':
                                continue  # Can't push the box
                            else:
                                # Move the box
                                curPositionCopy[boxNew_x][boxNew_y] = '$'
                                curPositionCopy[robotNew_x][robotNew_y] = '@'  # Move the robot
                                curPositionCopy[robot_x][robot_y] = ' '  # Clear old robot position
                                
                                
                                if curPositionCopy not in self.visitedMoves:
                                    matches = 0
                                    for k in range(self.lines):
                                        for l in range(self.maxRowLength):
                                            if self.wallsStorageSpaces[k][l] == '.':
                                                if curPositionCopy[k][l] != '$':
                                                    matches = 1
                                    movesTillNowCopy.append(key)
                                    if matches == 0:
                                        self.completed = 1
                                        print(movesTillNowCopy)
                                        self.path.append(movesTillNowCopy)
                                    else:
                                        self.queue.appendleft([curPositionCopy, movesTillNowCopy])
                                        self.visitedMoves.append(curPositionCopy)
                    else:
                        # Check if the new position is a wall or free space
                        if self.wallsStorageSpaces[robotNew_x][robotNew_y] == '#' or curPositionCopy[robotNew_x][robotNew_y] != ' ':
                            continue  # Can't move
                        else:
                            # Move the robot
                            curPositionCopy[robotNew_x][robotNew_y] = '@'
                            curPositionCopy[robot_x][robot_y] = ' '

                            if curPositionCopy not in self.visitedMoves:
                                movesTillNowCopy.append(key.lower())
                                self.queue.appendleft([curPositionCopy, movesTillNowCopy])
                                self.visitedMoves.append(curPositionCopy)
                                
        
        if self.completed == 0:
            print("Can't make it")

        time_end = time.perf_counter()
        print(f"Run time: {time_end - time_start}")

        if self.completed == 0:
            print("Can't make it")
        time_end = time.perf_counter()
        print(f"Run time: {time_end - time_start}")
        
def choose_Algo(algo, matrix, stone_weights):
    if algo == "DFS":
        return DFSSolver(matrix, stone_weights)
    else:
        return None