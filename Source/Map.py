import sys
import pygame
import queue

# Kích thước MÀN HÌNH
SCREEN_HEIGHT = 900
SCREEN_WIDTH = 900

# tên game
pygame.display.set_caption("Ares's Adventure")

class Game:
    def is_valid_value(self, char):
        return char in [' ', '#', '@', '.', '+', '$', '*']

    def __init__(self, filename):
        self.queue = queue.LifoQueue()
        self.matrix = []
        self.weights = []
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
                        self.weights.append(int(number))
                except ValueError as e:
                    print(f"ERROR: Dòng đầu tiên chứa giá trị không hợp lệ. Chi tiết lỗi: {e}")
                    sys.exit(1)
            else:
                print("ERROR: Dòng đầu tiên rỗng hoặc không có dữ liệu.")
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
                                self.stones_positions.append({'pos': (i, j), 'weight': self.weights[stone_id]})
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
        self.floor = pygame.transform.scale(pygame.image.load('img/floor.png'), (self.tile_size, self.tile_size))
        self.stone = pygame.transform.scale(pygame.image.load('img/stone.png'), (self.tile_size, self.tile_size))
        self.stone_on_stock = pygame.transform.scale(pygame.image.load('img/stone on stock.png'), (self.tile_size, self.tile_size))
        self.Ares = pygame.transform.scale(pygame.image.load('img/Ares.png').convert_alpha(), (self.tile_size, self.tile_size))
        self.Ares_on_stock = pygame.transform.scale(pygame.image.load('img/Ares on stock.png'), (self.tile_size, self.tile_size))
        self.stock = pygame.transform.scale(pygame.image.load('img/stock.png'), (self.tile_size, self.tile_size))
        
        self.font = pygame.font.SysFont(None, 24)
        
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                if self.matrix[i][j] == '@' or self.matrix[i][j] == '+':
                    self.Ares_pos = (i, j)
                    break
                
                
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
        
        if self.matrix[new_x][new_y] in ['$', '*']:
            if self.can_push(new_x, new_y, dx, dy):
                # Di chuyển cục đá
                self.matrix[new_x][new_y] = ' ' if self.matrix[new_x][new_y] == '$' else '.'
                self.matrix[new_x + dx][new_y + dy] = '*' if self.matrix[new_x + dx][new_y + dy] == '.' else '$'
                for stone in self.stones_positions:
                    if stone['pos'] == (new_x, new_y):
                        # Cập nhật vị trí cục đá trong danh sách
                        stone['pos'] = (new_x + dx, new_y + dy)
                        break
            else:
                return  # Không thể đẩy đá, dừng lại

        # Di chuyển Ares
        self.matrix[x][y] = '.' if self.matrix[x][y] == '+' else ' '
        self.matrix[new_x][new_y] = '@' if self.matrix[new_x][new_y] == ' ' else '+'
        self.Ares_pos = (new_x, new_y)
            
    def is_win(self):
        for line in self.matrix:
            if '.' in line:
                return False
        return True

    
def run_game(filename):
    pygame.init()
    pygame.font.init()
    
    m = Game(filename)
    running = True
    font = pygame.font.SysFont(None, 60) 
    win_message_displayed = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and not win_message_displayed:
                if event.key == pygame.K_UP:
                    m.move(-1, 0)
                elif event.key == pygame.K_DOWN:
                    m.move(1, 0)
                elif event.key == pygame.K_LEFT:
                    m.move(0, -1)
                elif event.key == pygame.K_RIGHT:
                    m.move(0, 1)

        m.draw_map()
        if m.is_win() and not win_message_displayed:
            win_message_displayed = True
            text_surface = font.render("You Win!", True, (0, 255, 0))
            text_rect = text_surface.get_rect(center=(m.screen.get_width() // 2, m.screen.get_height() // 2))
            m.screen.blit(text_surface, text_rect)
            pygame.display.flip()
            pygame.time.wait(2000)
            running = False


    pygame.quit()