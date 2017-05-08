import os
import time
import datetime
import operator
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

    item_colors = {'●': '\033[33m', '⚛': '\033[34m', '✿': '\033[31m', '✡': '\033[94m', '♦': '\033[32m', 'ᴥ': '\033[31m'}
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
        # changes color of obstacles ('#') on the level map
        board_line = [char.replace('#', item_colors['ᴥ'] + '#' + reset_color) for char in board_line]
        for key in item_colors:
            board_line = [char.replace(key, item_colors[key] + key + reset_color) for char in board_line]
        board.append(board_line)

    return board


def print_board(board):
    """Function prints list representing our gameboard.

    Args:
        board (list): list of board rows (list)
    """

    for row in board:
        print(''.join(row))


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


def getch():
    """Function returns the button pressed by user.

    Return:
        ch (str): button pressed by user
    """

    import sys, tty, termios
    from select import select
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        [i, o, e] = select([sys.stdin.fileno()], [], [], 0.35)
        if i:
            ch = sys.stdin.read(1)
        else:
            ch = ''
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


def user_control(board, x_player, y_player, button_pressed, inventory):
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

    red = '\033[31m'
    reset_color = '\033[0m'
    item_colors = {
        '●': '\033[33m', '⚛': '\033[34m', '✿': '\033[31m', '✡': '\033[94m',
        '♦': '\033[32m', 'ᴥ': '\033[31m', '☀': '\033[33m'}
    place_on_right_side = board[y_player][x_player + 1]
    place_on_left_side = board[y_player][x_player - 1]
    place_on_up_side = board[y_player - 1][x_player]
    place_on_down_side = board[y_player + 1][x_player]
    places_prohibited_to_stand_on = [
            'X', red + '#' + reset_color, '☹', '☃', '♞', '☻', '☬', item_colors['☀'] + '☀' + reset_color, red
            + '☀' + reset_color]

    if button_pressed == 'd' and place_on_right_side not in places_prohibited_to_stand_on:
        x_player += 1
    elif button_pressed == 'a' and place_on_left_side not in places_prohibited_to_stand_on:
        x_player -= 1
    elif button_pressed == 'w' and place_on_up_side not in places_prohibited_to_stand_on:
        y_player -= 1
    elif button_pressed == 's' and place_on_down_side not in places_prohibited_to_stand_on:
        y_player += 1

    #  conditions for level 4 (feeding friends)
    if button_pressed == 'd' and place_on_right_side in ['☹', '☃', '♞', '☻', '☬'] and inventory['●'] > 19:
        x_player += 1
    elif button_pressed == 'a' and place_on_left_side in ['☹', '☃', '♞', '☻', '☬'] and inventory['●'] > 19:
        x_player -= 1
    elif button_pressed == 'w' and place_on_up_side in ['☹', '☃', '♞', '☻', '☬'] and inventory['●'] > 19:
        y_player -= 1
    elif button_pressed == 's' and place_on_down_side in ['☹', '☃', '♞', '☻', '☬'] and inventory['●'] > 19:
        y_player += 1
    return x_player, y_player


def check_obstacle_contact(board, x_player, y_player, button_pressed, health):
    """Function checks user contact with dangerous obstacle and lowers user health points if it occurs.

    Args:
        board (list): list of board rows (list)
        x_player (int): horizontal position of player on the board
        y_player (int): vertical position of player on the board
        button_pressed (str): button pressed by user
        health (int): player's health points

    Return:
        health (int): player's health points
    """

    red = '\033[31m'
    reset_color = '\033[0m'
    place_on_right_side = board[y_player][x_player + 1]
    place_on_left_side = board[y_player][x_player - 1]
    place_on_up_side = board[y_player - 1][x_player]
    place_on_down_side = board[y_player + 1][x_player]

    if button_pressed == 'd' and place_on_right_side == red + '#' + reset_color:
        health -= 5
    elif button_pressed == 'a' and place_on_left_side == red + '#' + reset_color:
        health -= 5
    elif button_pressed == 'w' and place_on_up_side == red + '#' + reset_color:
        health -= 5
    elif button_pressed == 's' and place_on_down_side == red + '#' + reset_color:
        health -= 5
    return health


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
        '♦': '\033[32m', 'ᴥ': '\033[31m', '☀': '\033[33m'}
    reset_color = '\033[0m'
    if level == 1:
        food = {'●': 20, '⚛': 8, '✿': 5, '✡': 8, '♦': 10}
    elif level == 3:
        food = {'●': 20, '⚛': 6, '✿': 10, '✡': 6, '♦': 10}
    elif level == 2:
        food = {'●': 20, '⚛': 4, '✿': 15, '✡': 4, '♦': 10, '☀': 6}
    else:
        food = {'●': 20, '⚛': 5, '✿': 20, '✡': 2, '♦': 10}

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
    if level == 1:
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


def feeding_friends(board, x_player, y_player, inventory, hamster_energy):
    """Function removes collected items from inventory and lowers the enemy's energy
        if the user has enough items in inventory and if he is on one of his friend's position.

    Args:
        board (list): list of board rows (list)
        x_player (int): horizontal position of player on the board
        y_player (int): vertical position of player on the board
        inventory (dict): collected items(keys) and their amounts (values)
        hamster_energy (int): enemy's health points

    Return:
        inventory (dict): collected items(keys) and their amounts (values)
        hamster_energy (int): enemy's health points
    """

    if inventory['●'] >= 20 and board[y_player][x_player] in ['☹', '☃', '♞', '☻', '☬']:
        inventory['●'] -= 20
        hamster_energy -= 100
    return inventory, hamster_energy


def evil_hamster_defeat(board, x_player, y_player, level, hamster_energy, start_time):
    """Function removes the enemy's protection and
        defeats the enemy if the user is on enemy's position.

    Args:
        board (list): list of board rows (list)
        x_player (int): horizontal position of player on the board
        y_player (int): vertical position of player on the board
        level (int): actual game level
        hamster_energy (int): enemy's health points
        start_time (float): game start time in seconds

    Return:
        board (list): list of board rows (list)
        hamster_energy (int): enemy's health points
        your_time (int): whole game time in seconds
    """

    red = '\033[31m'
    reset_color = '\033[0m'
    if hamster_energy == 100:
        for lines in range(40):
            for columnes in range(120):
                if board[lines][columnes] == red + '#' + reset_color:
                    board[lines][columnes] = ' '
    if board[y_player][x_player] == '🐹':
        hamster_energy = 0
    end_time = time.time()
    your_time = int(end_time - start_time)
    return board, hamster_energy, your_time


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

    item_colors = {'●': '\033[33m', '⚛': '\033[34m', '✿': '\033[31m', '✡': '\033[94m', '♦': '\033[32m'}
    reset_color = '\033[0m'
    if board[y_player][x_player] == item_colors['●'] + '●' + reset_color:
        inventory['●'] += 1
    elif board[y_player][x_player] == item_colors['♦'] + '♦' + reset_color:
        inventory['♦'] += 1
    elif board[y_player][x_player] == item_colors['⚛'] + '⚛' + reset_color:
        inventory['●'] += 20
    elif board[y_player][x_player] == item_colors['✡'] + '✡' + reset_color:
        health += 5
    elif board[y_player][x_player] == item_colors['✿'] + '✿' + reset_color:
        health -= 5
    print(inventory)

    return inventory, health


def minion_encounter(x_player, y_player, minions_location, health):
    """Function checks if player encounters an enemy and changes his position on board and health if it has happened.

    Args:
        x_player (int): horizontal position of player on the board
        y_player (int): vertical position of player on the board
        minions_location (list): list containing positions of enemies on the board
        health (int): player's health points

    Return:
        x_player (int): horizontal position of player on the board
        y_player (int): vertical position of player on the board
        health (int): player's health points
    """

    for enemy_location in minions_location:
        if x_player == enemy_location[0] and y_player == enemy_location[1]:
            health -= 10
            x_player = 1
            y_player = 1
    return x_player, y_player, health


def move_minions(board, minions_location, character_color):
    """Function randomly moves evil minions on the board.

    Args:
        board (list): list of board rows (list)
        minions_location (list): list containing positions of enemies on the board
        character_color (str): escape code for chosen character color

    Return:
        board (list): list of board rows (list)
        minions_location (list): list containing positions of enemies on the board
    """

    acceptable_place = [' ', character_color + '🐿️' + '\033[0m']  # content of place where minion can move
    for enemy_location_nr in range(len(minions_location)):     # loop through all minions location
        x_minion = minions_location[enemy_location_nr][0]
        y_minion = minions_location[enemy_location_nr][1]
        possible_moves = []     # list of adjacent places on board where minion can move
        if board[y_minion][x_minion - 1] in acceptable_place:
            possible_moves.append([x_minion - 1, y_minion])
        if board[y_minion][x_minion + 1] in acceptable_place:
            possible_moves.append([x_minion + 1, y_minion])
        if board[y_minion - 1][x_minion] in acceptable_place:
            possible_moves.append([x_minion, y_minion - 1])
        if board[y_minion + 1][x_minion] in acceptable_place:
            possible_moves.append([x_minion, y_minion + 1])

        if len(possible_moves) > 0:
            chosen_move = random.choice(possible_moves)
            board[chosen_move[1]][chosen_move[0]] = board[y_minion][x_minion]
            board[y_minion][x_minion] = ' '
            minions_location[enemy_location_nr] = chosen_move.copy()

    return board, minions_location


def update_board_information(board, level, character_name, health, inventory, start_time):
    # food = {'●': 20, '⚛': 8, '✿': 5, '✡': 8, '♦': 10}
    item_colors = {'●': '\033[33m', '⚛': '\033[34m', '✿': '\033[31m', '✡': '\033[94m', '♦': '\033[32m'}
    reset_color = '\033[0m'
    end_time = time.time()
    your_time = int(end_time - start_time)
    board[0][128] = str(level)
    board[1][129] = character_name
    board[2][129] = str(health)
    board[3][127] = str(your_time)
    board[6][121] = item_colors['●'] + '●' + reset_color + ' : ' + str(inventory['●'])  # inserts nr of nuts
    board[7][121] = item_colors['♦'] + '♦' + reset_color + ' : ' + str(inventory['♦'])  # inserts nr of treasures
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


def checking_level_end(level, inventory, x_player, y_player, hamster_energy):
    """Function checks if level end conditions were met.

    Args:
        level (int): number of current game level
        inventory (dict): collected items(keys) and their amounts (values)
        x_player (int): horizontal position of player on the board
        y_player (int): vertical position of player on the board
        hamster_energy (int) : enemy's health points

    Return:
        next_level (bool): True if level end conditions were met, False otherwise
    """

    next_level = False
    if level == 1 and inventory['●'] >= 50:
        next_level = True
    elif level == 3 and inventory['●'] >= 40 and x_player == 117 and y_player == 38:
        next_level = True
    elif level == 2 and inventory['●'] >= 60:
        next_level = True
    elif level == 4 and hamster_energy == 0:
        next_level = True
    return next_level


def setting_next_level(level):
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
    inventory = {'●': 0, '♦': 0}

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

    return game_won, level, inventory, board, x_player, y_player, minions_location


def intro():
    """Function displays game intro"""

    color = ['\033[31m', '\033[32m', '\033[33m', '\033[34m', '\033[35m', '\033[36m', '\033[37m']
    reset_color = '\033[0m'

    img_file = open('end_images.txt')
    images = img_file.read().split('***\n')
    img_file.close()

    for image_nr in range(len(images)):
        image = images[image_nr]
        image = image.splitlines()

        for i in range(len(image)):
            image[i] = random.choice(color) + image[i] + reset_color

        for i in range(2, len(image)):
            os.system('clear')
            for j in range(i+1):
                print(image[j])
            time.sleep(0.05)

        input('Press ENTER to continue')

        for i in range(len(image)):
            os.system('clear')
            image[i] = ' '
            for j in range(len(image)):
                print(image[j])
            time.sleep(0.05)

        input('Press ENTER to continue')


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


def import_highscores(filename='highscores.txt'):
    """Function imports high scores from .txt file, formats them and put them into highscore list.

    Args:
        filename (str): name of the file with high scores

    Return:
        highscores (list): list of high scores from .txt file
    """

    highscores = []
    highscores_lines = []
    with open(filename, 'r') as highscores_file:  # read high scores from the file and put each line to the list
        scores = highscores_file.read().splitlines()
        for score in scores:  # add separated scores to highscores_lines
            if score != '':
                highscores_lines.append(score)
    for item in highscores_lines:  # add formatted scores to highscores list
        item = item.split(' | ')
        highscores.append(item)
    return highscores


def add_to_highscores(highscores, health, your_time, character_name):
    """Function adds new score to the highscore list.

    Args:
        highscores (list): list of high scores from .txt file
        health (int): player's health points
        your_time (int): whole game time in seconds

    Return:
        highscores (list): list of high scores with new score added
    """

    date = str(datetime.date.today())
    minutes = your_time // 60
    seconds = your_time % 60
    time = '{:3d}:{:02d}'.format(minutes, seconds)
    score = ['{:10s}'.format(character_name), time, '{:5d}'.format(health), date]
    highscores.append(score)
    return highscores


def sort_highscores(highscores):
    """Function sorts high scores in the list (primary key = time of the game, secondary key = user's health points).

    Args:
        highscores (list): list of high scores from .txt file

    Return:
        highscores (list): list of high scores after sorting
    """

    highscores = sorted(highscores, key=operator.itemgetter(2), reverse=True)  # sort highscores list (secondary key)
    highscores = sorted(highscores, key=operator.itemgetter(1))  # sort highscores list (primary key)
    if len(highscores) > 10:
        highscores = highscores[:10]
    return highscores


def export_highscores(highscores, health, your_time, character_name, filename='highscores.txt'):
    """Function exports highscores list to the .txt file after modification.

    Args:
        highscores (list): list of high scores after adding new score and sorting
        health (int): player's health points
        your_time (int): whole game time in seconds
        filename (str): name of the file with high scores

    Return:
        highscores (list): list of high scores
    """

    highscores = add_to_highscores(highscores, health, your_time, character_name)
    highscores = sort_highscores(highscores)
    with open(filename, 'w') as highscores_file:  # save modified high scores into the file
        for item in highscores:
            highscores_file.write(' | '.join(item) + '\n')
    return highscores


def print_highscores(highscores):
    """Function prints highscores table.

    Args:
        highscores (list): list of high scores
    """
    os.system('clear')
    print('\nHigh scores')
    head_row = 'name' + ' '*9 + 'time' + ' '*4 + 'health' + ' '*3 + 'date' + ' '*6
    print('-' * len(head_row))
    print(head_row)
    print('-' * len(head_row))
    for item in highscores:
        print(' | '.join(item))


def menage_highscores(game_won, health, your_time, character_name):
    """Function calls other high scores functions depending on the user's win or loss.

    Args:
        game_won (bool): True if player managed to finish the game, False otherwise
        health (int): player's health points
        your_time (int): whole game time in seconds
    """
    if not game_won:
        highscores = import_highscores()
        print_highscores(highscores)
    else:
        highscores = import_highscores()
        highscores = export_highscores(highscores, health, your_time, character_name)
        print_highscores(highscores)


def light_magic_lamps(board, x_player, y_player, button_pressed, lamps_lit):
    """Function lights magic lamps in contact with user.

    Args:
        board (list): list of board rows (list)
        x_player (int): horizontal position of player on the board
        y_player (int): vertical position of player on the board
        button_pressed (str): button pressed by user
        lamps_lit (int): number of lit magic lamps

    Return:
        board (list): list of board rows (list)
        lamps_lit (int): number of lit magic lamps
    """

    reset_color = '\033[0m'
    lamps_colors = {
        'on': '\033[31m', 'off': '\033[33m'}
    place_on_right_side = board[y_player][x_player + 1]
    place_on_left_side = board[y_player][x_player - 1]
    place_on_up_side = board[y_player - 1][x_player]
    place_on_down_side = board[y_player + 1][x_player]

    if button_pressed == 'd' and place_on_right_side == lamps_colors['off'] + '☀' + reset_color:
        lamps_lit += 1
        board[y_player][x_player + 1] = lamps_colors['on'] + '☀' + reset_color
    elif button_pressed == 'a' and place_on_left_side == lamps_colors['off'] + '☀' + reset_color:
        lamps_lit += 1
        board[y_player][x_player - 1] = lamps_colors['on'] + '☀' + reset_color
    elif button_pressed == 'w' and place_on_up_side == lamps_colors['off'] + '☀' + reset_color:
        lamps_lit += 1
        board[y_player - 1][x_player] = lamps_colors['on'] + '☀' + reset_color
    elif button_pressed == 's' and place_on_down_side == lamps_colors['off'] + '☀' + reset_color:
        lamps_lit += 1
        board[y_player + 1][x_player] = lamps_colors['on'] + '☀' + reset_color
    return board, lamps_lit


def main():
    #  intro()
    character_name, character_color = create_player()
    level = 3
    # sets parameters of next game level
    game_won, level, inventory, board, x_player, y_player, minions_location = setting_next_level(level)

    button_pressed = ''
    health = 20  # player's initial health points
    lamps_lit = 0
    hamster_energy = 600
    game_won = False
    start_time = time.time()

    while button_pressed != '\\' and health > 0 and not game_won:   # game end conditions
        # update text info on board
        board = update_board_information(board, level, character_name, health, inventory, start_time)
        manage_display(board, x_player, y_player, character_color)   # creates current frame of game animation
        board, minions_location = move_minions(board, minions_location, character_color)
        button_pressed = getch()    # reads button pressed by user
        # changes user position based on pressed button
        x_player, y_player = user_control(board, x_player, y_player, button_pressed, inventory)
        # lights magic lamps in contact with user
        board, lamps_lit = light_magic_lamps(board, x_player, y_player, button_pressed, lamps_lit)
        # checks if user encounters an obstacle and lowers user health
        health = check_obstacle_contact(board, x_player, y_player, button_pressed, health)
        # changes user inventory and health if user collected special items
        inventory, health = collecting_food(board, x_player, y_player, inventory, health)
        # changes evil hamster's energy if user fed his friends with collected items
        inventory, hamster_energy = feeding_friends(board, x_player, y_player, inventory, hamster_energy)
        # checks if user encounters an enemy and chenges user properties if it has happened
        x_player, y_player, health = minion_encounter(x_player, y_player, minions_location, health)
        # checks enemy's energy, removes his protection and defeats him if the user is on his position
        board, hamster_energy, your_time = evil_hamster_defeat(
            board, x_player, y_player, level, hamster_energy, start_time)
        # checks if level end conditions were met
        next_level = checking_level_end(level, inventory, x_player, y_player, hamster_energy)
        if next_level:
            # sets parameters of next game level
            game_won, level, inventory, board, x_player, y_player, minions_location = setting_next_level(level)

    print_end_image(game_won)
    menage_highscores(game_won, health, your_time, character_name)


if __name__ == '__main__':
    main()
