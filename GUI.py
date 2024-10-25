import sys
import pygame
import queue
import pyautogui 

wall = pygame.image.load("img/wall.png")
floor = pygame.image.load('img/floor.png')
stone = pygame.image.load('img/stone.png')
box_docked = pygame.image.load('img/stone on stock.png')
Ares = pygame.image.load('img/Ares.png')
Ares_on_stock = pygame.image.load('img/Ares on stock.png')
stock = pygame.image.load('img/stock.png')
background = 255, 226, 191
pygame.init()

x= 1440
y = 900
SCREEN = pygame.display.set_mode((x, y))
pygame.display.set_caption("Menu")
BG = pygame.image.load("img/background.png")
BG = pygame.transform.scale(BG, (x, y))
level = ''
method=''
moves = ''

class Button():
	def __init__(self, image, pos, text_input, font, base_color, hovering_color):
		self.image = image
		self.x_pos = pos[0]
		self.y_pos = pos[1]
		self.font = font
		self.base_color, self.hovering_color = base_color, hovering_color
		self.text_input = text_input
		self.text = self.font.render(self.text_input, True, self.base_color)
		if self.image is None:
			self.image = self.text
		self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
		self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

	def update(self, screen):
		if self.image is not None:
			screen.blit(self.image, self.rect)
		screen.blit(self.text, self.text_rect)

	def checkForInput(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			return True
		return False

	def changeColor(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			self.text = self.font.render(self.text_input, True, self.hovering_color)
		else:
			self.text = self.font.render(self.text_input, True, self.base_color)

class Game:
    def is_valid_value(self, char):
        return char in {' ', '#', '$', '@', '.', '*', '+'}

    def __init__(self,filename,level):
        self.queue = queue.LifoQueue()
        self.matrix = []
        
        if level < 1:
            print ("ERROR: Level "+str(level)+" is out of range")
            sys.exit(1)

        with open(filename,'r') as file:
            level_found = False
            for line in file:
                row = []
                if not level_found:
                    if  "Level "+str(level) == line.strip():
                        level_found = True
                else:
                    if line.strip() != "":
                        row = []
                        for c in line:
                            if c != '\n' and self.is_valid_value(c):
                                row.append(c)
                            elif c == '\n': #jump to next row when newline
                                continue
                            else:
                                print ("ERROR: Level "+str(level)+" has invalid value "+c)
                                sys.exit(1)
                        self.matrix.append(row)
                    else:
                        break
                    
    def load_size(self):
        x = 0
        y = len(self.matrix)
        for row in self.matrix:
            if len(row) > x:
                x = len(row)
        return (x * 32+ 350, y * 32)

    def get_matrix(self):
        return self.matrix

    def print_matrix(self):
        for row in self.matrix:
            for char in row:
                sys.stdout.write(char)
                sys.stdout.flush()
            sys.stdout.write('\n')

    def get_content(self,x,y):
        return self.matrix[y][x]

    def set_content(self,x,y,content):
        if self.is_valid_value(content):
            self.matrix[y][x] = content
        else:
            print ("ERROR: Value '"+content+"' to be added is not valid")

                
def print_game(matrix,screen):
    screen.fill(background)
    x = 0
    y = 0
    for row in matrix:
        for char in row:
            if char == ' ': #floor
                screen.blit(floor,(x,y))
            elif char == '#': #wall
                screen.blit(wall,(x,y))
            elif char == '@': #Ares on floor
                screen.blit(Ares,(x,y))
            elif char == '.': #dock
                screen.blit(docker,(x,y))
            elif char == '*': #stone on stock
                screen.blit(box_docked,(x,y))
            elif char == '$': #stone on floor
                screen.blit(box,(x,y))
            elif char == '+': #Ares on dock
                screen.blit(worker_docked,(x,y))
            x = x + 32
        x = 0
        y = y + 32

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("font.ttf", size)

def play():
    Game
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.fill("black")
        print_game(game.get_matrix(),SCREEN)
        OPTIONS_BUTTON = Button(image=None, pos=(x-200,y-800),
                    text_input="OPTIONS", font=get_font(40), base_color="White", hovering_color="Green")
        PLAY_BACK = Button(image=None, pos=(x-200,y-500), 
                    text_input="BACK", font=get_font(40), base_color="White", hovering_color="Green")
        CALCULATE_BUTTON = Button(image=None, pos=(x-200,y-700), 
                    text_input="CALCULATE", font=get_font(40), base_color="White", hovering_color="Green")
        AUTO_SOLVE_BUTTON = Button(image=None, pos=(x-200,y-600), 
                    text_input="SOLVE", font=get_font(40), base_color="White", hovering_color="Green")      
        PLAY_BACK.update(SCREEN)
        OPTIONS_BUTTON.changeColor(PLAY_MOUSE_POS)
        OPTIONS_BUTTON.update(SCREEN)

        if method: 
            CALCULATE_BUTTON.changeColor(PLAY_MOUSE_POS)
            CALCULATE_BUTTON.update(SCREEN)
        if moves: 
            AUTO_SOLVE_BUTTON.changeColor(PLAY_MOUSE_POS)
            AUTO_SOLVE_BUTTON.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    select_Level()
                if OPTIONS_BUTTON.checkForInput(PLAY_MOUSE_POS):
                    Solve_choice()
                if CALCULATE_BUTTON.checkForInput(PLAY_MOUSE_POS):
                    Calculate()
                if AUTO_SOLVE_BUTTON.checkForInput(PLAY_MOUSE_POS):
                    Start_Solve()

        pygame.display.update()
        
def start_game():
    start = pygame.display.set_mode((320,240))
    level = int(ask(start,"Select Level"))
    if level > 0:
        return level
    else:
        print ("ERROR: Invalid Level: "+str(level))
        sys.exit(2)
        
def select_Level():
    global game
    global level
    global moves
    global method
    input_rect = pygame.Rect(800, 140, 150, 50)
    level = ""  # Khởi tạo level là chuỗi rỗng
    
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()
        
        SCREEN.fill("black")
        pygame.draw.rect(SCREEN, "white", input_rect, 2)
        
        level_input = get_font(45).render(level, True, "white")
        SCREEN.blit(level_input, (input_rect.x + 40, input_rect.y + 5))

        PLAY_TEXT = get_font(45).render("Enter your level", True, "White")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(400, 160))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)

        PLAY_BACK = Button(image=None, pos=(740, 600), text_input="BACK", font=get_font(40), base_color="White", hovering_color="Green")
        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        PLAY_START = Button(image=None, pos=(740, 400), text_input="START", font=get_font(40), base_color="White", hovering_color="Green")
        PLAY_START.changeColor(PLAY_MOUSE_POS)
        PLAY_START.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Kiểm tra sự kiện nhấn chuột
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()
                elif PLAY_START.checkForInput(PLAY_MOUSE_POS):
                    game = Game('input/input-'+ str(int(level)) + '.txt',int(level))
                    method = ''
                    moves = ''
                    play()

            # Kiểm tra sự kiện bàn phím
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    level = level[:-1]  # Xóa ký tự cuối cùng
                else:
                    level += event.unicode  # Thêm ký tự mới vào level

        pygame.display.flip()

def main_menu():
    global game
    while True:
        SCREEN.blit(BG, (0, 0))
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(740, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("img/Play Rect.png"), pos=(740, 350),
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        
        QUIT_BUTTON = Button(image=pygame.image.load("img/Quit Rect.png"), pos=(740, 550), 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    select_Level()

                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()