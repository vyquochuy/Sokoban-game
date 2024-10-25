import sys
import pygame
import queue
import pyautogui 
import tkinter as tk

pygame.init()

pygame.display.set_caption("Ares's Adventure")

x= 1440
y = 900
SCREEN = pygame.display.set_mode((x, y))
BG = pygame.image.load("img/background.png")
BG = pygame.transform.scale(BG, (x, y))

tile_size = 50

# Load images
wall = pygame.transform.scale(pygame.image.load("img/wall.png"), (tile_size, tile_size))
floor = pygame.transform.scale(pygame.image.load('img/floor.png'), (tile_size, tile_size))
stone = pygame.transform.scale(pygame.image.load('img/stone.png'), (tile_size, tile_size))
box_docked = pygame.transform.scale(pygame.image.load('img/stone on stock.png'), (tile_size, tile_size))
Ares = pygame.transform.scale(pygame.image.load('img/Ares.png').convert_alpha(), (tile_size, tile_size))
Ares_on_stock = pygame.transform.scale(pygame.image.load('img/Ares on stock.png'), (tile_size, tile_size))
stock = pygame.transform.scale(pygame.image.load('img/stock.png'), (tile_size, tile_size))
background = 255, 226, 191

level = ''
method=''
moves = ''

class Game:
    def is_valid_value(self, char):
        return char in [' ', '#', '@', '.', '+', '$', '*']

    def __init__(self, filename):
        self.queue = queue.LifoQueue()
        self.matrix = []
        self.weights = []
        
        with open(filename,'r') as file:
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
                            print ("ERROR: invalid value "+c)
                            sys.exit(1)
                    self.matrix.append(row)
                else:
                    break
                
    def get_matrix(self):
        return self.matrix
    
    def print_matrix(self):
        for row in self.matrix:
            for char in row:
                sys.stdout.write(char)
                sys.stdout.flush()
            sys.stdout.write('\n')
    
    def draw_map(self):
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                if self.matrix[i][j] == ' ':
                    SCREEN.blit(floor, (j*50, i*50))
                elif self.matrix[i][j] == '#':
                    SCREEN.blit(wall, (j*50, i*50))
                elif self.matrix[i][j] == '@':
                    SCREEN.blit(Ares, (j*50, i*50))
                elif self.matrix[i][j] == '.':
                    SCREEN.blit(stock, (j*50, i*50))
                elif self.matrix[i][j] == '+':
                    SCREEN.blit(Ares_on_stock, (j*50, i*50))
                elif self.matrix[i][j] == '$':
                    SCREEN.blit(stone, (j*50, i*50))
                elif self.matrix[i][j] == '*':
                    SCREEN.blit(box_docked, (j*50, i*50))
        pygame.display.flip()
                
filename = input("Enter the level: ")
game = Game('input/input-'+filename+'.txt')

game.print_matrix()

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
