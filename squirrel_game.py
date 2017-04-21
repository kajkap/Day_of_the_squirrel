import os


def create_board(width, height):
    board = []
    for row in range(height):
        board.append(['X'] * width)
    for column in range(height)[1:-1]:
        for i in range(width)[1:-1]:
            board[column][i] = ' '
    return board


def print_board(board):
    for row in board:
        print(''.join(row))


def insert_player(board, x_player, y_player):
    board[y_player][x_player] = '@'
    return board


def getch():
    import sys, tty, termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


def user_control(board, x_player, y_player):
    button_pressed = getch()
    if button_pressed == 'd' and board[y_player][x_player + 1] != 'X':
        x_player += 1
    elif button_pressed == 'a' and board[y_player][x_player - 1] != 'X':
        x_player -= 1
    elif button_pressed == 'w' and board[y_player - 1][x_player] != 'X':
        y_player -= 1
    elif button_pressed == 's' and board[y_player + 1][x_player] != 'X':
        y_player += 1
    elif button_pressed == '\\':
        x_player = 'quit'
    return x_player, y_player


def main():
    button_pressed = ''
    x_player = 1
    y_player = 1
    while x_player != 'quit':
        os.system('clear')
        board = create_board(120, 40)
        board = insert_player(board, x_player, y_player)
        print_board(board)
        x_player, y_player = user_control(board, x_player, y_player)


main()
