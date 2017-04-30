import os
import time
import random


# def create_board(columns, lines):
#     """Function creates list representing our gameboard.
#
#     Args:
#         columns (int): number of gameboard columns
#         lines (int): number of gameboard rows
#
#     Return:
#         board (list): list of board rows (list)
#     """
#
#     board = []
#     full_line = ['X' for i in range(columns)]   # creates full row of the board
#     medium_line = [' ' for i in range(columns-2)]   # creates space inside medium rows
#     for i in range(lines):  # creates board as list of lists (rows)
#         board.append(full_line.copy())
#         if i > 0 and i < lines - 1:
#             board[i][1:(columns-1)] = medium_line
#     return board


def loading_level(level_nr):
    level_file = open('level' + level_nr + '.txt')
    level_content = level_file.readlines()
    level_file.close()

    board = []
    for line in level_content:
        line = line.strip('\n')

        board_line = []
        for character in line:
            board_line.append(character)
        board.append(board_line)

    return board


def print_board(board):
    """Function prints list representing our gameboard.

    Args:
        board (list): list of board rows (list)
    """

    for row in board:
        print(''.join(row))


def insert_player(board, x_player, y_player):
    """Function inserts player character into the list representing our gameboard.

    Args:
        board (list): list of board rows (list)

    Return:
        board (list): list of board rows (list) after player insertion
    """

    board[y_player][x_player] = '@' + '\033[32m'
    return board


def clear_player(board, x_player, y_player):
    """Function clears the place occupied by the player character in the list representing our gameboard.

    Args:
        board (list): list of board rows (list)
        x_player (int): horizontal position of player on the board
        y_player (int): vertical position of player on the board

    Return:
        board (list): list of board rows (list) after clearing the player position
    """

    board[y_player][x_player] = ' '
    return board


def getch():
    """Function returns the button pressed by user.

    Return:
        ch (str): button pressed by user
    """

    import sys, tty, termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


def user_control(board, x_player, y_player, button_pressed):
    """Function controls user position on the board based on the button pressed by user.
        Movent towards the obstacle ('X') is forbidden.

    Args:
        board (list): list of board rows (list)
        x_player (int): horizontal position of player on the board
        y_player (int): vertical position of player on the board
        button_pressed (str): button pressed by user

    Return:
        x_player (int): horizontal position of player on the board
        y_player (int): vertical position of player on the board
    """

    place_on_right_side = board[y_player][x_player + 1]
    place_on_left_side = board[y_player][x_player - 1]
    place_on_up_side = board[y_player - 1][x_player]
    place_on_down_side = board[y_player + 1][x_player]

    if button_pressed == 'd' and place_on_right_side != 'X':
        x_player += 1
    elif button_pressed == 'a' and place_on_left_side != 'X':
        x_player -= 1
    elif button_pressed == 'w' and place_on_up_side != 'X':
        y_player -= 1
    elif button_pressed == 's' and place_on_down_side != 'X':
        y_player += 1
    return x_player, y_player


def insert_food(board, level):
    """Function inserts items to collect into gameboard.

    Args:
        board (list): list of board rows (list)
        level (int): actual game level

    Return:
        board (list): list of board rows (list) after food to collect insertion
    """
    if level == 1:
        food = {'🌰': 20, '🍄': 8, '🍏': 5, '🍓': 8, '💎': 10}
    elif level == 2:
        food = {'🌰': 20, '🍄': 6, '🍏': 10, '🍓': 6, '💎': 10}
    elif level == 3:
        food = {'🌰': 20, '🍄': 4, '🍏': 15, '🍓': 4, '💎': 10}
    else:
        food = {'🌰': 20, '🍄': 2, '🍏': 20, '🍓': 2, '💎': 10}

    for key in food:
        for i in range(food[key]):
            lines = random.randrange(2, 38)
            columnes = random.randrange(2, 118)
            while board[lines][columnes] != key:
                if board[lines][columnes] == ' ':
                    board[lines][columnes] = key
                else:
                    lines = random.randrange(2, 38)
                    columnes = random.randrange(2, 118)
    return board


def collecting_food(board, x_player, y_player, inventory, health):
    """Function adds collected items into inventory.

    Args:
        board (list): list of board rows (list)
        x_player (int): horizontal position of player on the board
        y_player (int): vertical position of player on the board
        inventory (dict): collected items(keys) and their amounts (values)
        health (int): player's health points

    Return:
        inventory (dict): collected items(keys) and their amounts (values)
        health (int): player's health points
    """
    if board[y_player][x_player] == '🌰':
        inventory['🌰'] += 1
    elif board[y_player][x_player] == '💎':
        inventory['💎'] += 1
    elif board[y_player][x_player] == '🍄':
        inventory['🌰'] += 20
    elif board[y_player][x_player] == '🍓':
        health += 5
    elif board[y_player][x_player] == '🍏':
        health -= 5
    return inventory, health


def main():
    button_pressed = ''
    x_player = 1    # player's initial horizontal position
    y_player = 1    # player's initial vertical position
    level = 1
    inventory = {'🌰': 0, '💎': 0}
    # board = create_board(120, 40)   # creation of the gameboard
    board = loading_level(str(level))   # creation of the gameboard
    board = insert_food(board, level)
    health = 20  # player's initial health points

    while button_pressed != '\\':
        os.system('clear')  # clears terminal screen
        board = insert_player(board, x_player, y_player)    # inserts player character on the gameboard
        print_board(board)  # displays gameboard
        board = clear_player(board, x_player, y_player)  # clears place on the gameboard occupied by user
        button_pressed = getch()    # reads button pressed by user
        # changes user position based on pressed button
        x_player, y_player = user_control(board, x_player, y_player, button_pressed)
        inventory, health = collecting_food(board, x_player, y_player, inventory, health)
        if inventory['🌰'] >= 20:  # next level condition
            level += 1
            inventory = {'🌰': 0, '💎': 0}
            # board = create_board(120, 40)
            board = loading_level(str(level))
            board = insert_food(board, level)


if __name__ == '__main__':
    main()
