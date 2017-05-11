import random
import os


def loading_level(level_nr):
    """Function loades list representing our gameboard from text files.

    Args:
        level_nr (int): number of current game level

    Return:
        board (list): list of board rows (list)
    """

    item_colors = {
        '●': '\033[33m', '⚛': '\033[34m', '✿': '\033[31m', '✡': '\033[94m', 'ᴥ': '\033[31m',
        '#': '\033[31m', '℥': '\033[32m', '☯': '\033[32m', '☂': '\033[32m', '♫': '\033[32m'}
    reset_color = '\033[0m'

    level_file = open('level' + level_nr + '.txt')
    level_content = level_file.readlines()
    level_file.close()

    board = []
    for line in level_content:
        line = line.strip('\n')

        board_line = []
        for character in line:
            board_line.append(character)
        # changes color of elements on the level map
        for key in item_colors:
            board_line = [char.replace(key, item_colors[key] + key + reset_color) for char in board_line]
        board.append(board_line)

    return board


def insert_food(board, level):
    """Function inserts items to collect into gameboard.

    Args:
        board (list): list of board rows (list)
        level (int): actual game level

    Return:
        board (list): list of board rows (list) after food to collect insertion
    """

    item_colors = {
        '●': '\033[33m', '⚛': '\033[34m', '✿': '\033[31m', '✡': '\033[94m',
        'ᴥ': '\033[31m', '☀': '\033[33m', '℥': '\033[32m', '☯': '\033[32m', '☂': '\033[32m', '♫': '\033[32m'}
    reset_color = '\033[0m'
    if level == 1:
        food = {'●': 20, '⚛': 8, '✿': 5, '✡': 8, '☯': 3, '☂': 3, '♫': 3}
    elif level == 3:
        food = {'●': 20, '⚛': 6, '✿': 10, '✡': 6, '℥': 4, '☯': 3, '☂': 3, '♫': 3}
    elif level == 2:
        food = {'●': 20, '⚛': 4, '✿': 15, '✡': 4, '☀': 6, '☯': 3, '☂': 3, '♫': 3}
    else:
        food = {'●': 20, '⚛': 5, '✿': 20, '✡': 2, '☯': 3, '☂': 3, '♫': 3}

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
        minions_location (list): list containing positions of enemies on the board
    """

    item_colors = {'ᴥ': '\033[31m'}
    reset_color = '\033[0m'
    if level == 4:
        minions = {'ᴥ': 5}
    elif level == 2:
        minions = {'ᴥ': 5}
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


def insert_friends(board, level):
    """Function insert squirrel's friends into gameboard.

    Args:
        board (list): list of board rows (list)
        level (int): actual game level

    Return:
        board (list): list of board rows (list) after friends insertion
    """

    friends = ['☹', '☃', '♞', '☻', '☬']
    if level == 4:
        lines = 37
        columnes = 34
        for friend in friends:
            board[lines][columnes] = friend
            columnes += 17
    return board


def colour_hamster(board, level):
    """Function colours hamster image on level4 gameboard.

    Args:
        board (list): list of board rows (list)
        level (int): actual game level

    Return:
        board (list): list of board rows (list) after colouring hamster
    """

    blue = '\033[34m'
    darkgrey = '\033[90m'
    yellow = '\033[93m'
    reset_color = '\033[0m'

    if level == 4:
        for lines in range(20, 31):
            for columnes in range(100, 120):
                if board[lines][columnes] == '&':
                    board[lines][columnes] = blue + '&' + reset_color
                elif board[lines][columnes] == '*':
                    board[lines][columnes] = darkgrey + '*' + reset_color
                elif board[lines][columnes] == '%':
                    board[lines][columnes] = yellow + '%' + reset_color
    return board


def create_player():
    """Function asks user about name and color of the game character.

    Return:
        character_name (str): name of the character chosen by user
        character_color (str): escape code for chosen character color
    """

    choose_colors_text = """
    1. red
    2. green
    3. yellow\n"""
    character_colors = {'1': '\033[31m', '2': '\033[32m', '3': '\033[33m'}
    os.system('clear')
    print('Character creation screen.')
    character_name = input("Choose your character's name: ")
    chosen_character_color = ''
    while chosen_character_color not in ['1', '2', '3']:
        print("Choose your character's color [1, 2 or 3].")
        chosen_character_color = input(choose_colors_text)
    character_color = character_colors[chosen_character_color]
    return character_name, character_color


def setting_next_level(level, inventory):
    """Function sets parameters of next game level.

    Args:
        level (int): number of current game level

    Return:
        game_won (bool): True if player managed to finish the game, False otherwise
        level (int): number of next game level
        inventory (dict): collected items(keys) and their amounts (values)
        board (list): list of board rows (list)
        x_player (int): horizontal position of player on the board
        y_player (int): vertical position of player on the board
        minions_location (list): list containing positions of enemies on the board
    """

    x_player = 1    # player's initial horizontal position
    y_player = 1    # player's initial vertical position
    level += 1
    if level == 1:
        inventory = {'●': 0, '☯': 0, '☂': 0, '♫': 0}
    if level == 3:
        inventory['℥'] = 0
    if level == 4:
        del inventory['℥']
    if level == 5:
        game_won = True
        board = []
        minions_location = []
    else:
        board = loading_level(str(level))
        board = insert_food(board, level)
        board, minions_location = insert_minions(board, level)
        board = insert_friends(board, level)
        board = colour_hamster(board, level)
        game_won = False
    inventory['●'] = 0
    return game_won, level, inventory, board, x_player, y_player, minions_location
