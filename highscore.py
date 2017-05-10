import os
import datetime
import operator


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


def manage_highscores(game_won, health, your_time, character_name):
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
