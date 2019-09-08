import sys
import pygame
import numpy
import os

ROWS = 6
COLS = 7

PLAYER_ONE = 1
PLAYER_TWO = 2
REGULAR_MOVE = 0
WINNING_MOVE = 1
INVALID_MOVE = 2
HUMAN = 0
AI = 1
PYGAME_CELL_WIDTH = 110
PYGAME_CELL_HEIGHT = 110
PYGAME_WINDOW_WIDTH = PYGAME_CELL_WIDTH * COLS
PYGAME_WINDOW_HEIGHT = PYGAME_CELL_HEIGHT * ROWS

board = numpy.zeros((ROWS, COLS))
RESOURCES_PATH = os.path.join(os.path.dirname(__file__), "resources")
PYGAME_BLANK_CELL = pygame.image.load(os.path.join(RESOURCES_PATH, "blank.png"))
PYGAME_RED_CELL = pygame.image.load(os.path.join(RESOURCES_PATH, "red.png"))
PYGAME_YELLOW_CELL = pygame.image.load(os.path.join(RESOURCES_PATH, "yellow.png"))


def play(board, col, player):
    for i in range(ROWS):
        if board[ROWS - i - 1][col] == 0:
            board[ROWS - i - 1][col] = player
            return


def is_valid(board, col):
    return 0 <= col < COLS and board[0][col] == 0


def process(board, player, playertype):
    if playertype == HUMAN:
        return process_human(board, player)
    if playertype == AI:
        return process_ai(board, player)
    if playertype == API:
        return process_ai(board, player)
    else:
        exit(1)


def process_human(board, player, pos):
    if not is_valid(board, pos):
        return INVALID_MOVE
    play(board, pos, player)
    if has_won(board, player):
        return WINNING_MOVE
    return REGULAR_MOVE


def has_won(board, player):
    for c in range(COLS - 3):
        for r in range(ROWS):
            if board[r][c] == board[r][c + 1] == board[r][c + 2] == board[r][c + 3] == player:
                return True
    for c in range(COLS):
        for r in range(ROWS - 3):
            if board[r][c] == board[r + 1][c] == board[r + 2][c] == board[r + 3][c] == player:
                return True
    for c in range(COLS - 3):
        for r in range(ROWS - 3):
            if board[r][c] == board[r + 1][c + 1] == board[r + 2][c + 2] == board[r + 3][c + 3] == player:
                return True
    for c in range(COLS - 3):
        for r in range(3, ROWS):
            if board[r][c] == board[r - 1][c + 1] == board[r - 2][c + 2] == board[r - 3][c + 3] == player:
                return True
    return False

def is_draw(board):
    for c in range(COLS):
        for r in range(ROWS):
            if board[r][c] == 0:
                return False
    return True

def process_ai(board, player):
    valid_moves = numpy.zeros(0)
    for i in range(COLS):
        temp_board = numpy.copy(board)
        if is_valid(temp_board, i):
            valid_moves = numpy.append(valid_moves, i)
            play(temp_board, i, player)
            if has_won(temp_board, player):
                return i
    numpy.random.shuffle(valid_moves)
    return valid_moves[0]



player_one_type = HUMAN
player_two_type = HUMAN
while True:
    inp = int(input("Setup player 1 (0 = human, 1 = AI):"))
    if 0 <= inp <= 1:
        player_one_type = inp
        break
while True:
    inp = int(input("Setup player 2 (0 = human, 1 = AI):"))
    if 0 <= inp <= 1:
        player_two_type = inp
        break

pygame.init()
screen = pygame.display.set_mode((PYGAME_WINDOW_WIDTH, PYGAME_WINDOW_HEIGHT))


def render(board):
    for c in range(COLS):
        for r in range(ROWS):
            if board[r][c] == 0:
                screen.blit(PYGAME_BLANK_CELL, (c * PYGAME_CELL_WIDTH, r * PYGAME_CELL_HEIGHT))
            elif board[r][c] == 1:
                screen.blit(PYGAME_RED_CELL, (c * PYGAME_CELL_WIDTH, r * PYGAME_CELL_HEIGHT))
            elif board[r][c] == 2:
                screen.blit(PYGAME_YELLOW_CELL, (c * PYGAME_CELL_WIDTH, r * PYGAME_CELL_HEIGHT))


def notify(msg):
    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render(msg, True, (0, 255, 0), (0, 0, 0))
    screen.blit(text, (0, 0))


def render_win(player):
    notify('Player ' + str(player) + ' won!')

def render_draw():
    notify('It\'s a draw!')

turn = 1
running = True
is_over = False
winner = None
while running:
    # print(board)

    render(board)
    if is_over:
        if winner != None:
            render_win(winner)
        else:
            render_draw()
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and is_over:
            turn = 1
            is_over = False
            winner = None
            board = numpy.zeros((ROWS, COLS))
        elif event.type == pygame.MOUSEBUTTONDOWN and not is_over:
            pos = int(pygame.mouse.get_pos()[0] / PYGAME_CELL_WIDTH)
            if turn % 2 != 0:
                if player_one_type == HUMAN:
                    if is_valid(board, pos):
                        play(board, pos, PLAYER_ONE)
                        if has_won(board, PLAYER_ONE):
                            winner = PLAYER_ONE
                            is_over = True
                        elif is_draw(board):
                            is_over = True
                    else:
                        turn -= 1
                elif player_one_type == AI:
                    pos = int(process_ai(board, PLAYER_ONE))
                    play(board, pos, PLAYER_ONE)
                    if has_won(board, PLAYER_ONE):
                        winner = PLAYER_ONE
                        is_over = True
                    elif is_draw(board):
                        is_over = True
            else:
                if player_two_type == HUMAN:
                    if is_valid(board, pos):
                        play(board, pos, PLAYER_TWO)
                        if has_won(board, PLAYER_TWO):
                            winner = PLAYER_TWO
                            is_over = True
                        elif is_draw(board):
                            is_over = True
                    else:
                        turn -= 1
                elif player_two_type == AI:
                    pos = int(process_ai(board, PLAYER_TWO))
                    play(board, pos, PLAYER_TWO)
                    if has_won(board, PLAYER_TWO):
                        winner = PLAYER_TWO
                        is_over = True
                    elif is_draw(board):
                        is_over = True
            turn += 1

print(board)
