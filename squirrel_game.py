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
    red = '\033[31m'
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
        board_line = [char.replace('#', red + '#' + reset_color) for char in board_line]
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
    red = '\033[31m'
    reset_color = '\033[0m'
    place_on_right_side = board[y_player][x_player + 1]
    place_on_left_side = board[y_player][x_player - 1]
    place_on_up_side = board[y_player - 1][x_player]
    place_on_down_side = board[y_player + 1][x_player]

    if button_pressed == 'd' and place_on_right_side not in ['X', red + '#' + reset_color]:
        x_player += 1
    elif button_pressed == 'a' and place_on_left_side not in ['X', red + '#' + reset_color]:
        x_player -= 1
    elif button_pressed == 'w' and place_on_up_side not in ['X', red + '#' + reset_color]:
        y_player -= 1
    elif button_pressed == 's' and place_on_down_side not in ['X', red + '#' + reset_color]:
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
        minions_location (list): list containing positions of enemies on the board
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


def insert_friends_and_hamster(board, level):
    """Function inserts evil hamster and squirrel's friends into gameboard.

    Args:
        board (list): list of board rows (list)
        level (int): actual game level

    Return:
        board (list): list of board rows (list) after friends and hamster insertion
    """

    friends = ['🦆', '🦊', '🐰', '🐥', '🐻']
    if level == 4:
        board[24][113] = '🐹'
        lines = 37
        columnes = 35
        for friend in friends:
            board[lines][columnes] = friend
            columnes += 17
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

    if inventory['●'] >= 20 and board[y_player][x_player] in ['🦆', '🦊', '🐰', '🐥', '🐻']:
        inventory['●'] -= 20
        hamster_energy -= 100
    return inventory, hamster_energy


def evil_hamster_defeat(board, x_player, y_player, level, hamster_energy):
    """Function removes the enemy's protection and
        defeats the enemy if the user is on enemy's position.

    Args:
        board (list): list of board rows (list)
        x_player (int): horizontal position of player on the board
        y_player (int): vertical position of player on the board
        level (int): actual game level
        hamster_energy (int): enemy's health points

    Return:
        board (list): list of board rows (list)
        hamster_energy (int): enemy's health points
    """

    if hamster_energy == 100:
        for board[lines][columnes] in board:
            if board[lines][columnes] == '§':
                board[lines][columnes] = ' '
    if board[y_player][x_player] == '🐹':
        hamster_energy = 0
    return board, hamster_energy


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
        print("orzeszek")
    elif board[y_player][x_player] == '♦':
        inventory['♦'] += 1
        print("diamencik")
    elif board[y_player][x_player] == '⚛':
        inventory['●'] += 20
    elif board[y_player][x_player] == '✡':
        health += 5
    elif board[y_player][x_player] == '✿':
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


def move_minions(board, minions_location):
    acceptable_place = [' ', '\033[95m' + '🐿️' + '\033[0m']  # content of place where minion can move
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
    elif level == 3 and inventory['●'] >= 60:
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
        board (list): list of board rows (list)
        x_player (int): horizontal position of player on the board
        y_player (int): vertical position of player on the board
        inventory (dict): collected items(keys) and their amounts (values)
    """

    x_player = 1    # player's initial horizontal position
    y_player = 1    # player's initial vertical position
    level += 1
    inventory = {'●': 0, '♦': 0}

    if level == 5:
        game_won = True
        board = []
    else:
        board = loading_level(str(level))
        board = insert_food(board, level)
        board, minions_location = insert_minions(board, level)
        board = insert_friends_and_hamster(board, level)
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

    with open('end_images.txt', 'r') as img_file:
        images = img_file.read().split('***\n')
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
    #  intro()
    level = 0
    # sets parameters of next game level
    game_won, level, inventory, board, x_player, y_player, minions_location = setting_next_level(level)

    button_pressed = ''
    health = 20  # player's initial health point
    hamster_energy = 600
    game_won = False

    while button_pressed != '\\' and health > 0 and not game_won:   # game end conditions
        manage_display(board, x_player, y_player)   # creates current frame of game animation
        board, minions_location = move_minions(board, minions_location)
        button_pressed = getch()    # reads button pressed by user
        # changes user position based on pressed button
        x_player, y_player = user_control(board, x_player, y_player, button_pressed)
        # checks if user encounters an obstacle and lowers user health
        health = check_obstacle_contact(board, x_player, y_player, button_pressed, health)
        # changes user inventory and health if user collected special items
        inventory, health = collecting_food(board, x_player, y_player, inventory, health)
        # changes evil hamster's energy if user fed his friends with collected items
        inventory, hamster_energy = feeding_friends(board, x_player, y_player, inventory, hamster_energy)
        # checks if user encounters an enemy and chenges user properties if it has happened
        x_player, y_player, health = minion_encounter(x_player, y_player, minions_location, health)
        # checks enemy's energy, removes his protection and defeats him if the user is on his position
        board, hamster_energy = evil_hamster_defeat(board, x_player, y_player, level, hamster_energy)

        # checks if level end conditions were met
        next_level = checking_level_end(level, inventory, x_player, y_player)
        if next_level:
            # sets parameters of next game level
            game_won, level, inventory, board, x_player, y_player, minions_location = setting_next_level(level)

    print_end_image(game_won)


if __name__ == '__main__':
    main()
