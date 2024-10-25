import sys
import pygame
import queue


# Kích thước MÀN HÌNH
SCREEN_HEIGHT = 900
SCREEN_WIDTH = 900

# khởi tạo pygame
pygame.init()
pygame.display.set_caption("Ares's Adventure")

class map:
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

            # Đọc và xử lý dòng đầu tiên
            line = file.readline().strip()
            if line:  # Kiểm tra nếu dòng đầu tiên không trống
                numbers = line.split()  # Tách các số trong dòng dựa trên khoảng trắng
                try:
                    for number in numbers:
                        self.weights.append(int(number))  # Lưu số vào danh sách weights dưới dạng số nguyên
                except ValueError as e:
                    print(f"ERROR: Dòng đầu tiên chứa giá trị không hợp lệ. Chi tiết lỗi: {e}")
                    sys.exit(1)
            else:
                print("ERROR: Dòng đầu tiên rỗng hoặc không có dữ liệu.")
                sys.exit(1)

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
        self.tile_size = SCREEN_HEIGHT // len(self.matrix)
        SCREEN_WIDTH = max(len(row) for row in self.matrix) * self.tile_size
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        # Tải hình ảnh và thay đổi kích thước
        self.wall = pygame.transform.scale(pygame.image.load("img/wall.png"), (self.tile_size, self.tile_size))
        self.floor = pygame.transform.scale(pygame.image.load('img/floor.png'), (self.tile_size, self.tile_size))
        self.stone = pygame.transform.scale(pygame.image.load('img/stone.png'), (self.tile_size, self.tile_size))
        self.stone_on_stock = pygame.transform.scale(pygame.image.load('img/stone on stock.png'), (self.tile_size, self.tile_size))
        self.Ares = pygame.transform.scale(pygame.image.load('img/Ares.png').convert_alpha(), (self.tile_size, self.tile_size))
        self.Ares_on_stock = pygame.transform.scale(pygame.image.load('img/Ares on stock.png'), (self.tile_size, self.tile_size))
        self.stock = pygame.transform.scale(pygame.image.load('img/stock.png'), (self.tile_size, self.tile_size))
        
        self.font = pygame.font.SysFont(None, 24)
    def in_wall(self, x, y):
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
        self.screen.fill((154, 126, 111))
        
        weight_index = 0
        
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
                elif self.matrix[i][j] == '$':
                    self.screen.blit(self.stone, (j * self.tile_size, i * self.tile_size))
                    if weight_index < len(self.weights):
                        weight_text = str(self.weights[weight_index])
                        weight_index += 1
                        text_surface = self.font.render(weight_text, True, (255, 255, 255))  # Màu trắng
                        text_rect = text_surface.get_rect(center=(j * self.tile_size + self.tile_size // 2, 
                                                                  i * self.tile_size + self.tile_size // 2))
                        self.screen.blit(text_surface, text_rect)  # Hiển thị trọng lượng trên hòn đá
                        
                elif self.matrix[i][j] == '*':
                    self.screen.blit(self.stone_on_stock, (j * self.tile_size, i * self.tile_size))
                    if weight_index < len(self.weights):
                        weight_text = str(self.weights[weight_index])
                        weight_index += 1
                        text_surface = self.font.render(weight_text, True, (255, 255 ,255))  # Màu trắng
                        text_rect = text_surface.get_rect(center=(j * self.tile_size + self.tile_size // 2, 
                                                                  i * self.tile_size + self.tile_size // 2))
                        self.screen.blit(text_surface, text_rect)  # Hiển thị trọng lượng trên hòn đá

        pygame.display.flip()

    # animation move
    def move(self):
        print("move")
        

def run_game(filename):
    pygame.init()
    pygame.font.init()
    
    m = map(filename)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    
        m.draw_map()

    pygame.quit()
