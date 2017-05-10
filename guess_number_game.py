import random
import time
import os


def generate_number():
    """Function generates number to be guessed.

    Return:
        number (int): generated number between 1 and 30
    """

    number = random.randrange(1, 31)
    return number


def initial_print():
    """Function prints the game instruction."""

    os.system('clear')
    print("""*** Guess the number! ***
    I'm thinking about a number between 1 and 30. Try to guess it.""")


def guessing():
    """Function asks user for the number.

    Return:
        guess (int): user's guess
    """

    guess = ''
    while not guess.isdigit():
        guess = input()
        if guess.isalpha():
            print("Invalid input. You must guess a number!")
    guess = int(guess)
    return guess


def guess_check(guess, number):
    """Function checks if the user's answer is correct and print it out.

    Args:
        number (int): generated number
        guess (int): user's guess
    """

    you_win = False
    if guess > number:
        print('%d is too high' % guess)
    elif guess < number:
        print('%d is too low' % guess)
    else:
        print('\nCongratulations! You\'ve guessed my number.')
        time.sleep(2)
        you_win = True
    return you_win


def main():
    initial_print()
    number = generate_number()
    guess = 0
    while guess != number:
        guess = guessing()
        you_win = guess_check(guess, number)
    return you_win
