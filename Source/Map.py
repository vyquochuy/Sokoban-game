import sys
import pygame
import queue

pygame.init()

# Kích thước ô vuông
tile_size = 50

# tiêu đề
pygame.display.set_caption("Ares's Adventure")

class Game:
    cost = 0

    def is_valid_value(self, char):
        return char in [' ', '#', '@', '.', '+', '$', '*']

    def __init__(self, filename):
        self.queue = queue.LifoQueue()
        self.matrix = []
        self.weights = []

        with open(filename, 'r') as file:
            if not file:
                print("ERROR: file " + filename + " not found")
                sys.exit(1)

            line = file.readline()
            for c in line:
                if c != '\n':
                    self.weights.append(c)
                elif c == '\n':
                    break

            for line in file:
                row = []
                if line.strip() != "":
                    row = []
                    for c in line:
                        if c != '\n' and self.is_valid_value(c):
                            row.append(c)
                        elif c == '\n':
                            continue
                        else:
                            print("ERROR: invalid value " + c)
                            sys.exit(1)
                    self.matrix.append(row)
                else:
                    break

        # Tính kích thước màn hình dựa trên ma trận
        self.screen_width = max(len(row) for row in self.matrix) * tile_size
        self.screen_height = len(self.matrix) * tile_size
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        # Tải hình ảnh và thay đổi kích thước
        self.wall = pygame.transform.scale(pygame.image.load("img/wall.png"), (tile_size, tile_size))
        self.floor = pygame.transform.scale(pygame.image.load('img/floor.png'), (tile_size, tile_size))
        self.stone = pygame.transform.scale(pygame.image.load('img/stone.png'), (tile_size, tile_size))
        self.stone_on_stock = pygame.transform.scale(pygame.image.load('img/stone on stock.png'), (tile_size, tile_size))
        self.Ares = pygame.transform.scale(pygame.image.load('img/Ares.png').convert_alpha(), (tile_size, tile_size))
        self.Ares_on_stock = pygame.transform.scale(pygame.image.load('img/Ares on stock.png'), (tile_size, tile_size))
        self.stock = pygame.transform.scale(pygame.image.load('img/stock.png'), (tile_size, tile_size))

    def in_of_wall(self, x, y):
        # Kiểm tra có bao quanh bởi ít nhất 4 bức tường hay không
        if x == 0 or y == 0 or x == len(self.matrix) - 1 or y == len(self.matrix[x]) - 1:
            return False
        
        wall_count = 0
        # qua phải
        for i in range(y, len(self.matrix[x])):
            if self.matrix[x][i] == '#':
                wall_count += 1
                break
            
        # qua trái
        for i in range(y, -1, -1):
            if self.matrix[x][i] == '#':
                wall_count += 1
                break
            
        # xuống dưới
        for i in range(x, len(self.matrix)):
            try:
                if self.matrix[i][y] == '#':
                    wall_count += 1
                    break
            except:
                continue
            
        # lên trên
        for i in range(x, -1, -1):
            try:
                if self.matrix[i][y] == '#':
                    wall_count += 1
                    break
            except:
                continue
        return wall_count >= 4
    
    def draw_map(self):                    
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                # Vẽ nền
                if self.in_of_wall(i, j):
                    self.screen.blit(self.floor, (j * tile_size, i * tile_size))
                
                # Vẽ các đối tượng dựa trên ký tự trong ma trận
                if self.matrix[i][j] == '#':
                    self.screen.blit(self.wall, (j * tile_size, i * tile_size))
                elif self.matrix[i][j] == '@':
                    self.screen.blit(self.Ares, (j * tile_size, i * tile_size))
                elif self.matrix[i][j] == '.':
                    self.screen.blit(self.stock, (j * tile_size, i * tile_size))
                elif self.matrix[i][j] == '+':
                    self.screen.blit(self.Ares_on_stock, (j * tile_size, i * tile_size))
                elif self.matrix[i][j] == '$':
                    self.screen.blit(self.stone, (j * tile_size, i * tile_size))
                elif self.matrix[i][j] == '*':
                    self.screen.blit(self.stone_on_stock, (j * tile_size, i * tile_size))

        pygame.display.flip()

# Khởi tạo trò chơi
filename = input("Enter the level: ")
game = Game('input/input-' + filename + '.txt')

# Vòng lặp chính
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Vẽ lại bản đồ
    game.draw_map()

# Thoát pygame
pygame.quit()
sys.exit()
