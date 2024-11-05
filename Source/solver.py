import Map
import collections
import copy
import os
import time
import psutil
from queue import PriorityQueue

class Solver:
    def __init__(self, game):
        self.total_cost = 0
        self.completed = 0
        
        self.init_x, self.init_y = game.Ares_pos 
        self.stones_positions = game.stones_positions
        self.stones_weight = game.stones_weight
        self.matrix = game.matrix
        
        self.path = []
        self.boxRobot = []
        self.visitedMoves = []
        self.wallsStorageSpaces = []
        self.lines = len(self.matrix)
        self.maxRowLength = max(len(row) for row in self.matrix)
        self.possibleMoves = {'U': [-1, 0], 'R': [0, 1], 'D': [1, 0], 'L': [0, -1]}
        self.queue = collections.deque([])
        
        # Khởi tạo bản sao ma trận
        for i in range(self.lines):
            self.boxRobot.append(['-'] * self.maxRowLength)
            self.wallsStorageSpaces.append(['-'] * self.maxRowLength)

        for i in range(self.lines):
            for j in range(len(self.matrix[i])):
                if self.matrix[i][j] == '$' or self.matrix[i][j] == '@':
                    self.boxRobot[i][j] = self.matrix[i][j]
                    self.wallsStorageSpaces[i][j] = ' '
                elif self.matrix[i][j] == '.' or self.matrix[i][j] == '#':
                    self.wallsStorageSpaces[i][j] = self.matrix[i][j]
                    self.boxRobot[i][j] = ' '
                elif self.matrix[i][j] == ' ':
                    self.boxRobot[i][j] = ' '
                    self.wallsStorageSpaces[i][j] = ' '
                elif self.matrix[i][j] == '*':
                    self.boxRobot[i][j] = '$'
                    self.wallsStorageSpaces[i][j] = '.'
                elif self.matrix[i][j] == '+':
                    self.boxRobot[i][j] = '@'
                    self.wallsStorageSpaces[i][j] = '.'

    def complete(self, time_start, memory_start):           
        if self.completed == 0:
            print("Can't make it")  
            return []
        time_end = time.perf_counter()
        memory_end = psutil.Process().memory_info().rss / (1024 * 1024)  # Convert to MB
        run_time = round((time_end - time_start) * 1000, 4)
        memory_used = memory_end - memory_start
        return self.path, len(self.visitedMoves), run_time, memory_used
    
    def get_visited(self):
        return len(self.visitedMoves)
    
    def dfs(self):
        print("Solving using DFS")
        time_start = time.perf_counter()
        memory_start = psutil.Process().memory_info().rss / (1024 * 1024)  # Convert to MB
        
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
                    if curPosition[i][j] == '@':
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
        return self.complete(time_start, memory_start)
    
    
    def bfs(self):
        print("Solving using BFS")
        time_start = time.perf_counter()
        memory_start = psutil.Process().memory_info().rss / (1024 * 1024)  # Convert to MB

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
            current_cost = 0

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
                # Calculate new robot position
                robotNew_x = robot_x + self.possibleMoves[key][0]
                robotNew_y = robot_y + self.possibleMoves[key][1]

                # Check if the new robot position is within bounds
                if robotNew_x < 0 or robotNew_x >= len(curPosition) or robotNew_y < 0 or robotNew_y >= len(curPosition[0]):
                    continue  # Skip this move if it's out of bounds

                curPositionCopy = copy.deepcopy(curPosition)  # Create a copy of the current position

                # Initialize movesTillNowCopy here
                movesTillNowCopy = list(movesTillNow)  # Make a copy of movesTillNow

                if curPositionCopy[robotNew_x][robotNew_y] == '$':

                    boxNew_x = robotNew_x + self.possibleMoves[key][0]
                    boxNew_y = robotNew_y + self.possibleMoves[key][1]

                    # Check if the box position is within bounds
                    if boxNew_x < 0 or boxNew_x >= len(curPositionCopy) or boxNew_y < 0 or boxNew_y >= len(curPositionCopy[0]):
                        continue  # Skip this move if the box position is out of bounds

                    # Check if the next cell after the box is either a box or a wall
                    if curPositionCopy[boxNew_x][boxNew_y] == '$' or self.wallsStorageSpaces[boxNew_x][boxNew_y] == '#':
                        continue  # Avoid further steps

                    # If the robot can push the block
                    curPositionCopy[boxNew_x][boxNew_y] = '$'
                    curPositionCopy[robotNew_x][robotNew_y] = '@'
                    curPositionCopy[robot_x][robot_y] = ' '
                    
                    # Find the index of the stone being pushed
                    stone_index = sum(row.count('$') for row in curPosition)  # Count total stones (or find a more specific way to identify)
                    if stone_index < len(self.stones_weight):
                        current_cost += self.stones_weight[stone_index]  # Add the weight to the current total_cost
                        

                    if curPositionCopy not in self.visitedMoves:
                        matches = 0
                        for k in range(0, self.lines):
                            for l in range(0, self.maxRowLength):
                                if self.wallsStorageSpaces[k][l] == '.':
                                    if curPositionCopy[k][l] != '$':
                                        matches = 1 
                        movesTillNowCopy.append(key)
                        
                        if matches == 0:
                            self.path.append(movesTillNowCopy)
                            self.completed = 1
                            
                            for i in range(len(movesTillNowCopy)):
                                direct = movesTillNowCopy[i]
                                if(direct.islower()):
                                    direct = direct.upper()
                                self.init_x += self.possibleMoves[direct][0]
                                self.init_y += self.possibleMoves[direct][1]
                                
                                for j in range(len(self.stones_positions)):
                                    if((self.init_x == self.stones_positions[j]['pos'][0]) and (self.init_y == self.stones_positions[j]['pos'][1])):
                                        while(i < len(movesTillNowCopy) and movesTillNowCopy[i].isupper()):
                                            if movesTillNowCopy[i].isupper():
                                                self.total_cost += self.stones_weight[j]
                                            i += 1
                                        break
                                        
                                
                            print(f"Moves: {movesTillNowCopy}")  # Print the total total_cost
                            print(f"Total Cost: {self.total_cost}")
                        else:
                            self.queue.append([curPositionCopy, movesTillNowCopy, current_cost])  # Append current total_cost to the queue
                            self.visitedMoves.append(curPositionCopy)
                else:
                    # Check if the robot moves into a wall
                    if self.wallsStorageSpaces[robotNew_x][robotNew_y] == '#':
                        continue  # Skip this move if it's a wall
                    
                    # If the robot moves into empty space
                    curPositionCopy[robotNew_x][robotNew_y] = '@'
                    curPositionCopy[robot_x][robot_y] = ' '
                    
                    if curPositionCopy not in self.visitedMoves:
                        movesTillNowCopy.append(key.lower())
                        self.queue.append([curPositionCopy, movesTillNowCopy, current_cost])  # Append current total_cost to the queue
                        self.visitedMoves.append(curPositionCopy)
        return self.complete(time_start, memory_start)
    
    def manhattan(self, state, storages):
        distance = 0
        for i in range(self.lines):
            for j in range(self.maxRowLength):
                if state[i][j] == '$':
                    if state[i][j] == '$':
                        temp = 9999999
                        for storage in storages:
                            distanceToNearest = abs(storage[0] - i) + abs(storage[1] - j)
                            temp = min(temp, distanceToNearest) + 1
                        distance += temp
        return distance
    
    def Astar(self):
        print("Solving using A* with manhattan heuristic")
        time_start = time.perf_counter()
        memory_start = psutil.Process().memory_info().rss / (1024 * 1024)  # Convert to MB
        
        storages = []
        for i in range(self.lines):
            for j in range(self.maxRowLength):
                if self.wallsStorageSpaces[i][j] == '.':
                    storages.append((i, j))
                    
        movesList = []
        
        queue = PriorityQueue()
        source = [self.boxRobot, movesList]
        if self.boxRobot not in self.visitedMoves:
            self.visitedMoves.append(self.boxRobot)
        queue.put((self.manhattan(self.boxRobot, storages), source))
        robot_x = -1
        robot_y = -1
        
        while not queue.empty() and self.completed == 0:
            temp = queue.get()
            curPosition = temp[1][0]
            movesTillNow = temp[1][1]
            stepsTillNow = len(movesTillNow)
            
            for i in range(self.lines):
                for j in range(self.maxRowLength):
                    if curPosition[i][j] == '@':
                        robot_y = j
                        robot_x = i
                        break
                else:
                    continue
                break
            
            for key in self.possibleMoves:
                robotNew_x = robot_x + self.possibleMoves[key][0]
                robotNew_y = robot_y + self.possibleMoves[key][1]
                curPositionCopy = copy.deepcopy(curPosition)
                movesTillNowCopy = copy.deepcopy(movesTillNow)
                
                if curPositionCopy[robotNew_x][robotNew_y] == '$':
                    boxNew_x = robotNew_x + self.possibleMoves[key][0]
                    boxNew_y = robotNew_y + self.possibleMoves[key][1]
                    if curPositionCopy[boxNew_x][boxNew_y] == '$' or self.wallsStorageSpaces[boxNew_x][boxNew_y] == '#':
                        continue
                    else:
                        curPositionCopy[boxNew_x][boxNew_y] = '$'
                        curPositionCopy[robotNew_x][robotNew_y] = '@'
                        curPositionCopy[robot_x][robot_y] = ' '
                        
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
                                self.path.append(movesTillNowCopy)
                                for i in range(len(movesTillNowCopy)):
                                    direct = movesTillNowCopy[i]
                                    if(direct.islower()):
                                        direct = direct.upper()
                                    self.init_x += self.possibleMoves[direct][0]
                                    self.init_y += self.possibleMoves[direct][1]
                                    for j in range(len(self.stones_positions)):
                                        if((self.init_x == self.stones_positions[j]['pos'][0]) and (self.init_y == self.stones_positions[j]['pos'][1])):
                                            while(i < len(movesTillNowCopy) and movesTillNowCopy[i].isupper()):
                                                if movesTillNowCopy[i].isupper():
                                                    self.total_cost += self.stones_weight[j]
                                                i += 1
                                            break
                                        
                                print(f"Moves: {movesTillNowCopy}")
                                print(f"Total cost: {self.total_cost}")
                            else:
                                queue.put((self.manhattan(curPositionCopy, storages) + stepsTillNow, [curPositionCopy, movesTillNowCopy]))
                                self.visitedMoves.append(curPositionCopy)
                else:
                    if self.wallsStorageSpaces[robotNew_x][robotNew_y] == '#' or curPositionCopy[robotNew_x][robotNew_y] != ' ':
                        continue
                    else:
                        curPositionCopy[robotNew_x][robotNew_y] = '@'
                        curPositionCopy[robot_x][robot_y] = ' '
                        if curPositionCopy not in self.visitedMoves:
                            movesTillNowCopy.append(key.lower())
                            queue.put((self.manhattan(curPositionCopy, storages) + stepsTillNow, [curPositionCopy, movesTillNowCopy]))
                            self.visitedMoves.append(curPositionCopy)
                        
        return self.complete(time_start, memory_start)
    
    def ucs(self):
        print("Solving using UCS with manhattan heuristic")
        time_start = time.perf_counter()
        memory_start = psutil.Process().memory_info().rss / (1024 * 1024)  # Convert to MB
        
        storages = []
        for i in range(self.lines):
            for j in range(self.maxRowLength):
                if self.wallsStorageSpaces[i][j] == '.':
                    storages.append([i, j])
                            
        boxRobtDistance = 999999
        boxes = []
        storagesLeft = len(storages)
        for i in range(self.lines):
            for j in range(self.maxRowLength):
                if self.boxRobot[i][j] == '$':
                    if self.wallsStorageSpaces[i][j] == '.':
                        storagesLeft -= 1
                    boxes.append([i, j])
                    
        for i in range(self.lines):
            for j in range(self.maxRowLength):
                if self.boxRobot[i][j] == '@':
                    for k in boxes:
                        if boxRobtDistance > abs(k[0]-i)+abs(k[1]-j):
                            boxRobtDistance+=abs(k[0]-i)+abs(k[1]-j)
        
        movesList = []
        queue = PriorityQueue()
        source = [self.boxRobot, movesList]
        if self.boxRobot not in self.visitedMoves:
            self.visitedMoves.append(self.boxRobot)
        queue.put((boxRobtDistance, source))
        
        robot_x = -1
        robot_y = -1
        self.completed = 0
        self.total_cost = 0
        
        while not queue.empty() and self.completed == 0:
            temp = queue.get()
            curPosition = temp[1][0]
            movesTillNow = temp[1][1]
            stepsTillNow = len(movesTillNow)
            
            for i in range(self.lines):
                for j in range(self.maxRowLength):
                    if curPosition[i][j] == '@':
                        robot_y = j
                        robot_x = i
                        break
                else:
                    continue
                break
            
            for key in self.possibleMoves:
                robotNew_x = robot_x + self.possibleMoves[key][0]
                robotNew_y = robot_y + self.possibleMoves[key][1]
                curPositionCopy  = copy.deepcopy(curPosition)
                movesTillNowCopy = copy.deepcopy(movesTillNow)
                
                if curPositionCopy[robotNew_x][robotNew_y] == '$':
                    boxNew_x = robotNew_x + self.possibleMoves[key][0]
                    boxNew_y = robotNew_y + self.possibleMoves[key][1]
                    if curPositionCopy[boxNew_x][boxNew_y] == '$' or self.wallsStorageSpaces[boxNew_x][boxNew_y] == '#':
                        continue
                    else:
                        curPositionCopy[boxNew_x][boxNew_y] = '$'
                        curPositionCopy[robotNew_x][robotNew_y] = '@'
                        curPositionCopy[robot_x][robot_y] = ' '
                        
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
                                self.path.append(movesTillNowCopy)
                                
                                for i in range(len(movesTillNowCopy)):
                                    direct = movesTillNowCopy[i]
                                    if(direct.islower()):
                                        direct = direct.upper()
                                    self.init_x += self.possibleMoves[direct][0]
                                    self.init_y += self.possibleMoves[direct][1]
                                    for j in range(len(self.stones_positions)):
                                        if((self.init_x == self.stones_positions[j]['pos'][0]) and (self.init_y == self.stones_positions[j]['pos'][1])):
                                            while(i < len(movesTillNowCopy) and movesTillNowCopy[i].isupper()):
                                                if movesTillNowCopy[i].isupper():
                                                    self.total_cost += self.stones_weight[j]
                                                i += 1
                                            break
                                        
                                print(f"Moves: {movesTillNowCopy}")
                                print(f"Total cost: {self.total_cost}")
                            else:
                                boxRobtDistance = 999999
                                boxes = []
                                storagesLeft = len(storages)
                                
                                for i in range(self.lines):
                                    for j in range(self.maxRowLength):
                                        if curPositionCopy[i][j] == '$':
                                            if self.wallsStorageSpaces[i][j] == '.':
                                                storagesLeft -= 1
                                            boxes.append([i, j])
                                            
                                for i in range(self.lines):
                                    for j in range(self.maxRowLength):
                                        if curPositionCopy[i][j] == '@':
                                            for k in boxes:
                                                boxRobtDistance = min(boxRobtDistance, abs(k[0] - i) + abs(k[1] - j))
                                
                                storagesLeft = 0
                                queue.put((self.manhattan(curPositionCopy, storages)+ boxRobtDistance+storagesLeft*2+stepsTillNow,[curPositionCopy,movesTillNowCopy]))
                                self.visitedMoves.append(curPositionCopy)
                else:
                    if self.wallsStorageSpaces[robotNew_x][robotNew_y] == '#' or curPositionCopy[robotNew_x][robotNew_y] != ' ':
                        continue
                    else:
                        curPositionCopy[robotNew_x][robotNew_y] = '@'
                        curPositionCopy[robot_x][robot_y] = ' '
                        if curPositionCopy not in self.visitedMoves:
                            movesTillNowCopy.append(key.lower())
                            boxRobtDistance = 999999
                            boxes = []
                            storagesLeft = len(storages)
                            for i in range(self.lines):
                                for j in range(self.maxRowLength):
                                    if curPositionCopy[i][j] == '$':
                                        if self.wallsStorageSpaces[i][j] == '.':
                                            storagesLeft -= 1
                                        boxes.append((i, j))
                                        
                            for i in range(self.lines):
                                for j in range(self.maxRowLength):
                                    if curPositionCopy[i][j] == '@':
                                        for k in boxes:
                                            boxRobtDistance = min(boxRobtDistance, abs(i - k[0]) + abs(j - k[1]))
                            
                            storagesLeft = 0
                            queue.put((self.manhattan(curPositionCopy, storages)+ boxRobtDistance+storagesLeft*2+stepsTillNow,[curPositionCopy,movesTillNowCopy]))
                            self.visitedMoves.append(curPositionCopy)
                            
        return self.complete(time_start, memory_start)