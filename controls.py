import os
import time
import guess_number_game
import add_numbers_game
import remember_number_game


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

    friends = ['☹', '☃', '♞', '☻', '☬']
    #  conditions for level 4 (feeding friends)
    if button_pressed == 'd' and place_on_right_side in friends and inventory['●'] > 19:
        x_player += 1
    elif button_pressed == 'a' and place_on_left_side in friends and inventory['●'] > 19:
        x_player -= 1
    elif button_pressed == 'w' and place_on_up_side in friends and inventory['●'] > 19:
        y_player -= 1
    elif button_pressed == 's' and place_on_down_side in friends and inventory['●'] > 19:
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


def checking_level_end(level, inventory, x_player, y_player, hamster_energy, board):
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
    if level == 1 and board[y_player][x_player] == '⇵':
        print_level_title(4)
        you_win = guess_number_game.main()
        if you_win:
            next_level = True

    elif level == 2 and board[y_player][x_player] == '⇵':
        print_level_title(4)
        won = add_numbers_game.main()
        if won:
            next_level = True

    elif level == 3 and board[y_player][x_player] == '⇵':
        print_level_title(4)
        win = remember_number_game.main()
        if win:
            next_level = True

    elif level == 4 and hamster_energy == 0:
        next_level = True
    return next_level


def print_level_title(number):
    """Function displays level title"""

    color = ['\033[31m', '\033[32m', '\033[33m', '\033[34m', '\033[35m', '\033[36m', '\033[37m']
    reset_color = '\033[0m'

    img_file = open('levels_title.txt')
    images = img_file.read().split('***\n')
    img_file.close()

    os.system('clear')
    print(color[0] + images[number] + reset_color)
    time.sleep(3)


def enable_level_exit(board, level, inventory, lamps_lit):
    """Function removes barrier around exit enabling player go to the next level.

    Args:
        board (list): list of board rows (list)
        inventory (dict): collected items(keys) and their amounts (values)
        level (int): current game level
        lamps_lit (int): number of lit magical lamps

    Return:
        board (list): list of board rows (list)
    """

    red = '\033[31m'
    reset_color = '\033[0m'
    if (level == 1 and inventory['●'] > 59) or (level == 2 and inventory['●'] > 59 and lamps_lit == 6) or (
            level == 3 and inventory['●'] > 59 and inventory['℥'] == 4):
        for lines in range(37, 39):
            for columnes in range(116, 119):
                if board[lines][columnes] == red + '#' + reset_color:
                    board[lines][columnes] = ' '

    return board
