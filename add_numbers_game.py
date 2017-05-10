import random
import time
import os


def initial_print():
    """Function prints the game instruction."""

    os.system('clear')
    print("""
    *** Add 2 numbers! ***
     You have 10 seconds.
     """)


def generate_numbers():
    """Function generates 2 numbers to be summed.

    Return:
        total (int): sum of two generated numbers
    """

    a = random.randrange(100, 1000)
    b = random.randrange(100, 1000)
    print('{} + {} = '.format(a, b))
    total = a + b
    return total


def guessing():
    """Function asks user for result of addition.

    Return:
        guess (int): user's answer
    """

    guess = ''
    while not guess.isdigit():
        guess = input()
    guess = int(guess)
    return guess


def check_answer(total, guess, your_time):
    """Function checks if the user's answer is correct
    and if the user doesn't exceed the time.

    Args:
        total (int): sum of two generated numbers
        guess (int): user's guess
        your_time (int): time since the beginning of the task

    Return:
        won (bool): True if the user's answer is correct, False otherwise
    """

    won = False
    if your_time <= 15:
        if guess != total:
            print('Wrong answer. Try again')
        else:
            print('Well done!')
            time.sleep(2)
            won = True
    else:
        print('You\'ve exceeded the time. Try again.')
        time.sleep(2)
    return won


def main():
    won = False
    while not won:
        initial_print()
        total = generate_numbers()
        guess = 0
        your_time = 0
        start_guess = time.time()
        while guess != total and your_time <= 15:
            guess = guessing()
            end_guess = time.time()
            your_time = int(end_guess - start_guess)
            won = check_answer(total, guess, your_time)
    return won
