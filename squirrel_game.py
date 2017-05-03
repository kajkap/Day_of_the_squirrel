import os
import time
import random

"""
black = '\033[30m'
red = '\033[31m'
green = '\033[32m'
orange = '\033[33m'
blue = '\033[34m'
purple = '\033[35m'
cyan = '\033[36m'
lightgrey = '\033[37m'
darkgrey = '\033[90m'
lightred = '\033[91m'
lightgreen = '\033[92m'
yellow = '\033[93m'
lightblue = '\033[94m'
pink = '\033[95m'
lightcyan = '\033[96m'
"""


def create_board(columns, lines):
    """Function creates list representing our gameboard.

    Args:
        columns (int): number of gameboard columns
        lines (int): number of gameboard rows

    Return:
        board (list): list of board rows (list)
    """

    board = []
    full_line = ['X' for i in range(columns)]   # creates full row of the board
    medium_line = [' ' for i in range(columns-2)]   # creates space inside medium rows
    for i in range(lines):  # creates board as list of lists (rows)
        board.append(full_line.copy())
        if i > 0 and i < lines - 1:
            board[i][1:(columns-1)] = medium_line
    return board


def loading_level(level_nr):
    """Function loades list representing our gameboard from text files.

    Args:
        level_nr (int): number of current game level

    Return:
        board (list): list of board rows (list)
    """

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

    board[y_player][x_player] = '\033[95m' + '🐿️' + '\033[0m'
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

    item_colors = {'●': '\033[33m', '⚛': '\033[34m', '✿': '\033[31m', '✡': '\033[94m', '♦': '\033[32m', 'ᴥ': '\033[31m'}
    reset_color = '\033[0m'
    if level == 1:
        food = {'●': 20, '⚛': 8, '✿': 5, '✡': 8, '♦': 10}
    elif level == 2:
        food = {'●': 20, '⚛': 6, '✿': 10, '✡': 6, '♦': 10}
    elif level == 3:
        food = {'●': 20, '⚛': 4, '✿': 15, '✡': 4, '♦': 10}
    else:
        food = {'●': 20, '⚛': 2, '✿': 20, '✡': 2, '♦': 10}

    for key in food:
        for i in range(food[key]):
            ready = False
            while not ready:
                lines = random.randrange(2, 38)
                columnes = random.randrange(2, 118)
                if board[lines][columnes] == ' ':
                    board[lines][columnes] = item_colors[key] + key + reset_color
                    ready = True
    return board


def insert_minions(board, level):
    """Function inserts evil minions into gameboard.

    Args:
        board (list): list of board rows (list)
        level (int): actual game level

    Return:
        board (list): list of board rows (list) after evil minions insertion
    """

    item_colors = {'ᴥ': '\033[31m'}
    reset_color = '\033[0m'
    if level == 1:
        minions = {'ᴥ': 5}
    elif level == 2:
        minions = {}
    elif level == 3:
        minions = {'ᴥ': 5}
    else:
        minions = {}

    minions_location = []
    for key in minions:
        for i in range(minions[key]):
            ready = False
            while not ready:
                lines = random.randrange(2, 38)
                columnes = random.randrange(2, 118)
                if board[lines][columnes] == ' ':
                    board[lines][columnes] = item_colors[key] + key + reset_color
                    ready = True
                minions_location.append([columnes, lines])
    return board, minions_location


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

    if board[y_player][x_player] == '●':
        inventory['●'] += 1
    elif board[y_player][x_player] == '♦':
        inventory['♦'] += 1
    elif board[y_player][x_player] == '⚛':
        inventory['●'] += 20
    elif board[y_player][x_player] == '✡':
        health += 5
    elif board[y_player][x_player] == '✿':
        health -= 5
    return inventory, health


def minion_encounter(x_player, y_player, minions_location, health):
    for enemy_location in minions_location:
        if x_player == enemy_location[0] and y_player == enemy_location[1]:
            health -= 10
            x_player = 1
            y_player = 1
    return x_player, y_player, health


def intro():
    """Function displays game intro"""

    pass


def manage_display(board, x_player, y_player):
    """Function takes care of game pseudo animation.

    Args:
        board (list): list of board rows (list)
        x_player (int): horizontal position of player on the board
        y_player (int): vertical position of player on the board
    """

    os.system('clear')  # clears terminal screen
    board = insert_player(board, x_player, y_player)    # inserts player character on the gameboard
    print_board(board)  # displays gameboard
    board = clear_player(board, x_player, y_player)  # clears place on the gameboard occupied by user


def checking_level_end(level, inventory, x_player, y_player):
    """Function checks if level end conditions were met.

    Args:
        level (int): number of current game level
        x_player (int): horizontal position of player on the board
        y_player (int): vertical position of player on the board
        inventory (dict): collected items(keys) and their amounts (values)

    Return:
        next_level (bool): True if level end conditions were met, False otherwise
    """

    next_level = False
    if level == 1 and inventory['●'] >= 50:
        next_level = True
    elif level == 2 and inventory['●'] >= 40 and x_player == 117 and y_player == 38:
        next_level = True
    return next_level


def setting_next_level(level):
    """Function sets parameters of next game level.

    Args:
        level (int): number of current game level

    Return:
        game_won (bool): True if player managed to finish the game, False otherwise
        level (int): number of next game level
        board (list): list of board rows (list)
        x_player (int): horizontal position of player on the board
        y_player (int): vertical position of player on the board
        inventory (dict): collected items(keys) and their amounts (values)
    """

    x_player = 1    # player's initial horizontal position
    y_player = 1    # player's initial vertical position
    level += 1
    inventory = {'●': 0, '♦': 0}

    if level == 4:
        game_won = True
        board = []
    else:
        board = loading_level(str(level))
        board = insert_food(board, level)
        board, minions_location = insert_minions(board, level)
        game_won = False
    return game_won, level, inventory, board, x_player, y_player, minions_location


def print_end_image(game_won):
    """Function displays final images from text file.

    Args:
        game_won (bool): shows whether a player has won or not
    """

    with open('end_images.txt', 'r') as img_file:
        images = img_file.read().split('***')
        if not game_won:
            for i in range(5):
                for image_nr in range(3):
                    os.system('clear')
                    print(images[image_nr])
                    time.sleep(0.2)
        else:
            for i in range(5):
                for image_nr in range(3, 6):
                    os.system('clear')
                    print(images[image_nr])
                    time.sleep(0.2)


def main():
    intro()
    level = 0
    # sets parameters of next game level
    game_won, level, inventory, board, x_player, y_player, minions_location = setting_next_level(level)

    button_pressed = ''
    health = 20  # player's initial health point
    game_won = False

    while button_pressed != '\\' and health > 0 and not game_won:   # game end conditions
        manage_display(board, x_player, y_player)   # creates current frame of game animation
        button_pressed = getch()    # reads button pressed by user
        # changes user position based on pressed button
        x_player, y_player = user_control(board, x_player, y_player, button_pressed)
        # changes user inventory and health if user collected special items
        inventory, health = collecting_food(board, x_player, y_player, inventory, health)
        x_player, y_player, health = minion_encounter(x_player, y_player, minions_location, health)

        # checks if level end conditions were met
        next_level = checking_level_end(level, inventory, x_player, y_player)
        if next_level:
            # sets parameters of next game level
            game_won, level, inventory, board, x_player, y_player, minions_location = setting_next_level(level)

    print_end_image(game_won)


if __name__ == '__main__':
    main()
