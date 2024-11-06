import sys
import pygame
import collections
import copy
import os
import time
import solver
sys.stdout.reconfigure(encoding='utf-8')

# Kích thước MÀN HÌNH
SCREEN_HEIGHT = 720
SCREEN_WIDTH = 720

# tên game
pygame.display.set_caption("Ares's Adventure")

class Game:
    def is_valid_value(self, char):
        return char in [' ', '#', '@', '.', '+', '$', '*']

    def __init__(self, filename):
        self.total_cost = 0
        self.total_weight = 0
        self.visitedNodes = 0
        self.path = []
        self.matrix = []
        self.stones_weight = []
        self.stones_positions = []

        with open(filename, 'r') as file:
            if not file:
                print("ERROR: file " + filename + " not found")
                sys.exit(1)

            # Đọc và xử lý dòng đầu tiên
            line = file.readline().strip()
            if line:
                numbers = line.split()
                try:
                    for number in numbers:
                        self.stones_weight.append(int(number))
                except ValueError as e:
                    print(f"ERROR: The first line contains invalid values. Error details: {e}")
                    sys.exit(1)
            else:
                print("ERROR: The first line is empty or contains no data.")
                sys.exit(1)

            stone_id = 0
            for i, line in enumerate(file):
                row = []
                if line.strip() != "":
                    row = []
                    for j, c in enumerate(line):
                        if c != '\n' and self.is_valid_value(c):
                            row.append(c)
                            if c in ['$', '*']:
                                self.stones_positions.append({'pos': (i, j), 'weight': self.stones_weight[stone_id]})
                                stone_id += 1
                        elif c == '\n':
                            continue
                        else:
                            print("ERROR: invalid value " + c)
                            sys.exit(1)
                    self.matrix.append(row)
                else:
                    break

        # Tính kích thước màn hình dựa trên ma trận
        self.tile_size = SCREEN_HEIGHT // len(self.matrix)
        SCREEN_WIDTH = max(len(row) for row in self.matrix) * self.tile_size
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        # Tải hình ảnh và thay đổi kích thước
        self.wall = pygame.transform.scale(pygame.image.load("img/wall.png"), (self.tile_size, self.tile_size))
        self.Ares = pygame.transform.scale(pygame.image.load('img/Ares.png'), (self.tile_size, self.tile_size))
        self.floor = pygame.transform.scale(pygame.image.load('img/floor.png'), (self.tile_size, self.tile_size))
        self.stone = pygame.transform.scale(pygame.image.load('img/stone.png'), (self.tile_size, self.tile_size))
        self.stock = pygame.transform.scale(pygame.image.load('img/stock.png'), (self.tile_size, self.tile_size))
        self.Ares_on_stock = pygame.transform.scale(pygame.image.load('img/Ares on stock.png'), (self.tile_size, self.tile_size))
        self.stone_on_stock = pygame.transform.scale(pygame.image.load('img/stone on stock.png'), (self.tile_size, self.tile_size))
        
        self.font = pygame.font.SysFont(None, 24)
        
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                if self.matrix[i][j] == '@' or self.matrix[i][j] == '+':
                    self.Ares_pos = (i, j)
                    break
                
                
    def in_wall(self, x, y):
        # Kiểm tra nếu tọa độ (x, y) nằm ở rìa ngoài của ma trận
        if x == 0 or y == 0 or x == len(self.matrix) - 1 or y == len(self.matrix[x]) - 1:
            return False
        
        # sử dụng hàm try để bắt lỗi nếu x, y không hợp lệ
        try:
            checks = [
                any(self.matrix[x][i] == '#' for i in range(y + 1, len(self.matrix[x]))),  # phải
                any(self.matrix[i][y] == '#' for i in range(x + 1, len(self.matrix))),     # xuống
                any(self.matrix[x][i] == '#' for i in range(y - 1, -1, -1)),               # trái
                any(self.matrix[i][y] == '#' for i in range(x - 1, -1, -1))                # lên
            ]
        except:
            return False
        return all(checks)
    
    def draw_map(self):
        self.screen.fill((154, 126, 111))
        
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                # Vẽ nền
                if self.in_wall(i, j):
                    self.screen.blit(self.floor, (j * self.tile_size, i * self.tile_size))
                
                # Vẽ các đối tượng dựa trên ký tự trong ma trận
                if self.matrix[i][j] == '#':
                    self.screen.blit(self.wall, (j * self.tile_size, i * self.tile_size))
                elif self.matrix[i][j] == '@':
                    self.screen.blit(self.Ares, (j * self.tile_size, i * self.tile_size))
                elif self.matrix[i][j] == '.':
                    self.screen.blit(self.stock, (j * self.tile_size, i * self.tile_size))
                elif self.matrix[i][j] == '+':
                    self.screen.blit(self.Ares_on_stock, (j * self.tile_size, i * self.tile_size))
                    
                elif self.matrix[i][j] in ['$', '*']:
                    if self.matrix[i][j] == '$':
                        self.screen.blit(self.stone, (j * self.tile_size, i * self.tile_size))
                    else:
                        self.screen.blit(self.stone_on_stock, (j * self.tile_size, i * self.tile_size))
                        
                    for stone in self.stones_positions:
                        if stone['pos'] == (i, j):
                            weight_text = str(stone['weight'])
                            text_surface = self.font.render(weight_text, True, (255, 255, 255))
                            text_rect = text_surface.get_rect(center=(j * self.tile_size + self.tile_size // 2, 
                                                                      i * self.tile_size + self.tile_size // 2))
                            self.screen.blit(text_surface, text_rect)
                            break
        
        # Draw total_cost and total weight in a separate box
        cost_box_width = 200
        cost_box_height = 60
        cost_box_x = (self.screen.get_width() - cost_box_width) // 2
        cost_box_y = 10

        pygame.draw.rect(self.screen, (0, 0, 0), (cost_box_x, cost_box_y, cost_box_width, cost_box_height))
        pygame.draw.rect(self.screen, (255, 255, 255), (cost_box_x, cost_box_y, cost_box_width, cost_box_height), 2)

        cost_text = f"Total Cost: {self.total_cost}"
        text_surface = self.font.render(cost_text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(cost_box_x + cost_box_width // 2, cost_box_y + cost_box_height // 2))
        self.screen.blit(text_surface, text_rect)
        
        total_weight_text = f"Total Weight: {self.total_weight}"
        total_weight_surface = self.font.render(total_weight_text, True, (255, 255, 255))
        total_weight_rect = total_weight_surface.get_rect(center=(cost_box_x + cost_box_width // 2, cost_box_y + cost_box_height // 2 + 20))
        self.screen.blit(total_weight_surface, total_weight_rect)
        
        pygame.display.flip()
                
    def can_push(self, x, y, dx, dy):
        new_x, new_y = x + dx, y + dy
        if not self.in_wall(new_x, new_y):
            return False
        return self.matrix[new_x][new_y] in [' ', '.']
       
    
    def move(self, dx, dy):
        x, y = self.Ares_pos
        new_x, new_y = x + dx, y + dy
        
        if self.matrix[new_x][new_y] == '#':
            return
        # đẩy đá nếu có thể
        if self.matrix[new_x][new_y] in ['$', '*']:
            if self.can_push(new_x, new_y, dx, dy):
                # Di chuyển cục đá
                self.matrix[new_x][new_y] = ' ' if self.matrix[new_x][new_y] == '$' else '.'
                self.matrix[new_x + dx][new_y + dy] = '*' if self.matrix[new_x + dx][new_y + dy] == '.' else '$'
                for stone in self.stones_positions:
                    if stone['pos'] == (new_x, new_y):
                        # Cập nhật vị trí cục đá trong danh sách
                        stone['pos'] = (new_x + dx, new_y + dy)
                        self.total_cost += stone['weight']
                        self.total_weight += stone['weight']
                        break
            else:
                return  # Không thể đẩy đá, dừng lại

        # Di chuyển Ares
        self.matrix[x][y] = '.' if self.matrix[x][y] == '+' else ' '
        self.matrix[new_x][new_y] = '@' if self.matrix[new_x][new_y] == ' ' else '+'
        self.Ares_pos = (new_x, new_y)
        self.total_cost += 1
        
            
    def move_left(self):
        self.move(0, -1)
    def move_right(self):
        self.move(0, 1)
    def move_up(self):
        self.move(-1, 0)
    def move_down(self):
        self.move(1, 0)        
    
    def is_win(self):
        for line in self.matrix:
            if '$' in line:
                return False
        return True

    
    
    
    def run_game(self, solution):
        font = pygame.font.SysFont(None, 60)
        running = True
        win_message_displayed = False
        
        if not solution:
            text_surface = font.render("UNSOLVABLE WITH CURRENT ALGORITHM", True, (255, 0, 0))
            text_rect = text_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
            self.screen.blit(text_surface, text_rect)
            pygame.display.flip()
            pygame.time.wait(2000)
            running = False
            pygame.quit()
            return False
        else:
            for word in solution:
                for char in word:
                    if char in ['r', 'R', 'l', 'L', 'u', 'U', 'd', 'D']:
                        self.path.append(char)
            
        while running:
            pygame.time.wait(500)
            
            for char in self.path:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        
                if not running:
                    break
                
                if char in ['r', 'R']:
                    self.move_right()
                elif char in ['l', 'L']:
                    self.move_left()
                elif char in ['u', 'U']:
                    self.move_up()
                elif char in ['d', 'D']:
                    self.move_down()

                self.draw_map()
                pygame.time.wait(200)
                
                if self.is_win() and not win_message_displayed:
                    win_message_displayed = True
                    text_surface = font.render("You Win!", True, (0, 255, 0))
                    text_rect = text_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
                    self.screen.blit(text_surface, text_rect)
                    pygame.display.flip()
                    
                    # Button Close
                    button_color = (195, 109, 55)   # Màu nền của nút
                    border_color = (255, 255, 255)  # Màu viền
                    button_font = pygame.font.Font(None, 36)
                    button_text = button_font.render("Close", True, (255, 255, 255))

                    # Xác định vị trí và kích thước nút
                    button_rect = button_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 50))
                    button_rect = button_rect.inflate(40, 20)
                    border_rect = button_rect.inflate(4, 4) 

                    # Vẽ viền cho nút
                    pygame.draw.rect(self.screen, border_color, border_rect)
                    
                    # Vẽ hình chữ nhật của nút chính bên trong viền
                    pygame.draw.rect(self.screen, button_color, button_rect)

                    # Vẽ văn bản "Close" lên nút
                    #self.screen.blit(button_text, button_rect)
                    self.screen.blit(button_text, button_text.get_rect(center=button_rect.center))
                    pygame.display.flip()
                    
                    waiting = True
                    while waiting:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                return
                            elif event.type == pygame.MOUSEBUTTONDOWN:
                                if button_rect.collidepoint(event.pos):
                                    pygame.quit()
                                    return

def init_game(filename):
    pygame.init()
    pygame.font.init()
    return Game(filename)

def solve(algo, Map):
    if algo == "DFS":
        return solver.Solver(Map).dfs()
    elif algo == "BFS":
        return solver.Solver(Map).bfs()
    elif algo == "UCS":
        return solver.Solver(Map).ucs()
    elif algo == "A*":
        return solver.Solver(Map).Astar()
    else:
        return None