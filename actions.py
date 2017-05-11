import time
import random
import hotcoldgame
from controls import print_level_title


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
    win = False
    if level == 4:
        if y_player in range(20, 29) and x_player in range(100, 118):
            print_level_title(5)
            win = hotcoldgame.main()
            x_player = 1
            y_player = 1
        if win:
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

    item_colors = {
        '●': '\033[33m', '⚛': '\033[34m', '✿': '\033[31m', '✡': '\033[94m', '℥': '\033[32m', '☯': '\033[32m',
        '☂': '\033[32m', '♫': '\033[32m'}
    reset_color = '\033[0m'
    if board[y_player][x_player] == item_colors['●'] + '●' + reset_color:
        inventory['●'] += 1
    elif board[y_player][x_player] == item_colors['☯'] + '☯' + reset_color:
        inventory['☯'] += 1
    elif board[y_player][x_player] == item_colors['☂'] + '☂' + reset_color:
        inventory['☂'] += 1
    elif board[y_player][x_player] == item_colors['♫'] + '♫' + reset_color:
        inventory['♫'] += 1
    elif board[y_player][x_player] == item_colors['⚛'] + '⚛' + reset_color:
        inventory['●'] += 20
    elif board[y_player][x_player] == item_colors['✡'] + '✡' + reset_color:
        health += 5
    elif board[y_player][x_player] == item_colors['✿'] + '✿' + reset_color:
        health -= 5
    elif board[y_player][x_player] == item_colors['℥'] + '℥' + reset_color:
        inventory['℥'] += 1
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
