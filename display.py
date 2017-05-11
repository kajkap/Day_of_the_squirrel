import os
import time
import random


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


def print_board(board):
    """Function prints list representing our gameboard.

    Args:
        board (list): list of board rows (list)
    """

    for row in board:
        print(''.join(row))


def print_end_image(game_won):
    """Function displays final images from text file.

    Args:
        game_won (bool): shows whether a player has won or not
    """

    color = ['\033[31m', '\033[32m', '\033[33m', '\033[34m', '\033[35m', '\033[36m', '\033[37m']
    reset_color = '\033[0m'

    with open('end_images.txt', 'r') as img_file:
        images = img_file.read().split('***\n')
        if not game_won:
            for i in range(5):
                for image_nr in range(3):
                    os.system('clear')
                    print(random.choice(color) + images[image_nr] + reset_color)
                    time.sleep(0.2)
        else:
            for i in range(5):
                for image_nr in range(3, 6):
                    os.system('clear')
                    print(random.choice(color) + images[image_nr] + reset_color)
                    time.sleep(0.2)


def update_board_information(board, level, character_name, health, inventory, start_time, hamster_energy):
    item_colors = {'●': '\033[33m', '⚛': '\033[34m', '✿': '\033[31m', '✡': '\033[94m'}
    reset_color = '\033[0m'
    end_time = time.time()
    your_time = int(end_time - start_time)
    board[0][128] = str(level)
    board[1][129] = character_name
    board[2][129] = str(health)
    board[3][127] = str(your_time)
    board[6][121] = item_colors['●'] + '●' + reset_color + ' : ' + str(inventory['●'])  # inserts nr of nuts
    board[7][139] = str(inventory['☯'] + inventory['☂'] + inventory['♫'])  # inserts total amount of treasures
    if level == 4:
        board[4][134] = str(hamster_energy)
    return board


def manage_display(board, x_player, y_player, character_color):
    """Function takes care of game pseudo animation.

    Args:
        board (list): list of board rows (list)
        x_player (int): horizontal position of player on the board
        y_player (int): vertical position of player on the board
        character_color (str): escape code for chosen character color
    """

    os.system('clear')  # clears terminal screen
    board = insert_player(board, x_player, y_player, character_color)    # inserts player character on the gameboard
    print_board(board)  # displays gameboard
    board = clear_player(board, x_player, y_player)  # clears place on the gameboard occupied by user


def prepare_board_to_print(inventory, board):
    """Function creates board and inserts additional info on it.

    Args:
        inventory (dict): collected items(keys) and their amounts (values)
        board (list): list of board rows (list)

    Return:
        board (list): list of board rows (list)
    """

    inventory_info = {
        '●': ('nut', 'food', 0.1), '☯': ('legendary cookie', 'treasure', 0.5),
        '☂': ('ancient umbrella', 'treasure', 0.5), '♫': ('magic note', 'treasure', 0.5),
        '℥': ('key shard', 'tool', 0.25)}

    board = insert_text_into_board(3, 3, 'Kasia Perkowska and Maciej Nowak present:', board)
    board = insert_text_into_board(4, 3, 'The Day Of The Squirrel', board)

    table_title = ('Item'.rjust(4) + 'Name'.rjust(22) + 'Type'.rjust(10)
                   + 'Weight'.rjust(8) + 'Amount'.rjust(8))
    board = insert_text_into_board(7, 3, 'Inventory', board)
    board = insert_text_into_board(8, 3, table_title, board)
    board = insert_text_into_board(9, 3, '_' * 60, board)

    total_weight = 0
    line_nr = 10
    for key in inventory:
        line_to_print = (key.rjust(4) + inventory_info[key][0].rjust(22) + inventory_info[key][1].rjust(10)
                         + str(inventory_info[key][2]).rjust(8) + str(inventory[key]).rjust(8))
        board = insert_text_into_board(line_nr, 3, line_to_print, board)
        line_nr += 2
        total_weight += inventory[key] * inventory_info[key][2]
    board = insert_text_into_board(line_nr - 1, 3, '_' * 60, board)
    board = insert_text_into_board(line_nr, 3, 'Your inventory total weight: ' + '{:.2f}'.format(total_weight), board)
    return board


def print_additional_game_info(inventory):
    """Function creates and prints screen with additional game info.

    Args:
        inventory (dict): collected items(keys) and their amounts (values)

    """

    info_table = create_board(120, 40)
    os.system('clear')
    info_table = prepare_board_to_print(inventory, info_table)
    print_board(info_table)
    input('Press ENTER to return to the game.')


def insert_text_into_board(y, x, text, board):
    """Function inserts text on the board in the specific location.

    Args:
        y (int): vertical coordinate of the place on the board where text will be inserted
        x (int): horizontal coordinate of the place on the board where text will be inserted
        text (str): text to insert on the board
        board (list): list of board rows (list)

    Return:
        board (list): list of board rows (list)
    """

    for i in range(len(text)):
        board[y][x+i] = text[i]
    return board


def intro():
    """Function displays game intro"""

    color = ['\033[31m', '\033[32m', '\033[33m', '\033[34m', '\033[35m', '\033[36m', '\033[37m']
    reset_color = '\033[0m'

    img_file = open('intro.txt')
    images = img_file.read().split('***\n')
    img_file.close()

    for image_nr in range(len(images)):
        image = images[image_nr]
        image = image.splitlines()

        for i in range(len(image)):
            image[i] = random.choice(color) + image[i] + reset_color

        for i in range(len(image)):
            os.system('clear')
            for j in range(i+1):
                print(image[j])
            time.sleep(0.1)

        input('Press ENTER to continue')

        for i in range(len(image)):
            os.system('clear')
            image[i] = ' '
            for j in range(len(image)):
                print(image[j])
            time.sleep(0.1)


def insert_player(board, x_player, y_player, character_color):
    """Function inserts player character into the list representing our gameboard.

    Args:
        board (list): list of board rows (list)
        character_color (str): escape code for chosen character color

    Return:
        board (list): list of board rows (list) after player insertion
    """

    board[y_player][x_player] = character_color + '🐿️' + '\033[0m'
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
