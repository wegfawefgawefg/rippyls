import pygame
import random
import time

WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
HEIGHT, WIDTH = 64, 64
CELL_WIDTH = WINDOW_WIDTH / WIDTH
CELL_HEIGHT = WINDOW_HEIGHT / HEIGHT

def step(surface, board1, board2):
    height = len(board1)
    width = len(board1[0])

    for y in range(1, height - 1):
        for x in range(1, width - 1):
            neighborhood_sum = (
                board1[ y     ][ x - 1 ] +
                board1[ y     ][ x + 1 ] +
                board1[ y - 1 ][ x     ] +
                board1[ y + 1 ][ x     ] 
                + board1[ y - 1 ][ x - 1 ] 
                + board1[ y - 1 ][ x + 1 ] 
                + board1[ y + 1 ][ x - 1 ] 
                + board1[ y + 1 ][ x + 1 ] 
            )
            neighborhood_sum = neighborhood_sum // 4
            new_value = neighborhood_sum - board2[y][x]
            new_value *= 0.9
            board2[y][x] = new_value 
            
def draw_board(surface, board2, cell_width, cell_height):
    for y in range(1, HEIGHT - 1):
        for x in range(1, WIDTH - 1):
            val = board2[y][x]
            val = int(min(max(val, 0), 255))
            color = (val, val, val)
            top_left_x = x * CELL_WIDTH
            top_left_y = y * CELL_HEIGHT
            pygame.draw.rect(surface, color, 
                (top_left_x - 1, top_left_y - 1, cell_width + 1, cell_height + 1))

def draw_on_board(mouse_x, mouse_y, board1):
    x = int( mouse_x / WINDOW_WIDTH * WIDTH   )
    y = int( mouse_y / WINDOW_HEIGHT * HEIGHT )
    x = min(max(x, 1), WIDTH - 2)
    y = min(max(y, 1), HEIGHT - 2)
    board1[y][x] = 255 

def main():
    pygame.init()
    surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Ripples")

    board1 = [[0 for col in range(WIDTH)] for row in range(HEIGHT)]
    board2 = [[0 for col in range(WIDTH)] for row in range(HEIGHT)]

    running = True
    mouse_pressed = False  
    while running:
        time.sleep(0.01)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pressed = True
                    draw_on_board(*event.pos, board1)                    

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:   
                    mouse_pressed = False         

            elif event.type == pygame.MOUSEMOTION:
                if mouse_pressed:
                    draw_on_board(*event.pos, board1)                    

        if random.random() < 0.1:
            x = int(random.random() * WIDTH)
            y = int(random.random() * HEIGHT)
            x = min(max(x, 1), WIDTH - 2)
            y = min(max(y, 1), HEIGHT - 2)
            board1[y][x] = int(random.random() * 255)

        step(surface, board1, board2)
        board1, board2 = board2, board1

        draw_board(surface, board2, CELL_WIDTH, CELL_HEIGHT)
        pygame.display.update()

if __name__ == "__main__":
    main()