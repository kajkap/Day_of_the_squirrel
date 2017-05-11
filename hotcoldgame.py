import random
import os

COLD = '\033[34m'
WARM = '\033[33m'
HOT = '\033[31m'
ENDC = '\033[37m'


def hint(number, guess):
    """Function checks if user's guess is correct and print the appropriate hint.

    Args:
        number (int): number to be guessed
        guess (int): user's guess
    Return:
        hot (int): amount of guessed digits (correct digit on the correct position)
    """

    number = str(number)
    guess = str(guess)
    hot = 0
    warm = 0
    cold = 0
    for digit in enumerate(number):
        if digit[1] == guess[digit[0]]:
            hot += 1
        elif digit[1] in guess:
            warm += 1
    if hot + warm == 0:
        cold = 1
    print((HOT + 'hot ') * hot +
          (WARM + 'warm ') * warm +
          (COLD + 'cold ') * cold +
          ENDC
          )
    return hot


def input_guess():
    """Function asks user for guessing a 3-digit number.

    Return:
        guess (int): user's guess
    """

    guess = ''
    while len(guess) != 3 or not guess.isdigit():
        guess = input()
        if not guess.isdigit() or len(guess) != 3:
            print('Try again! You should provide only 3-digit number!')
    return guess


def generate_number():
    """Function generates 3-digit number to be guessed.

    Return:
        number (int): number to be guessed
    """

    number = []
    while len(number) < 3:
        digit = str(random.randint(0, 9))
        if digit not in number:
            number.append(digit)
    number = ''.join(number)
    return number


def initial_print():
    """Function prints the game instruction."""

    print(ENDC + '''
    I am thinking of a 3-digit number. Try to guess what it is.

    Here are some clues:

    When I say:    That means:

      Cold       No digit is correct.
      Warm       One digit is correct but in the wrong position.
      Hot        One digit is correct and in the right position.

    I have thought up a number. You have 10 guesses to get it.
    ''')


def guessing_loop(hot_amount, turn, number):
    """Main guesssing loop. Function calls guessing and guess checking functions until the user win or lose.

    Args:
        hot_amount (int): amount of guessed digits (correct digit on the correct position)
        turn (int): number of guessings
        number (int): number to be guessed
    Return:
        hot_amount (int): amount of guessed digits (correct digit on the correct position)
    """

    while hot_amount != 3 and turn <= 10:
        print('Guess #', turn)
        guess = input_guess()
        hot_amount = hint(number, guess)
        turn += 1
    return hot_amount


def final_print(hot_amount):
    """Function prints the result of the game.

    Args:
        hot_amount (int): amount of guessed digits (correct digit on the correct position)
    """

    win = False
    if hot_amount == 3:
        print('You got it!')
        win = True
    else:
        print('You lost!')
    return win


def main():
    os.system('clear')
    initial_print()
    turn = 1
    hot_amount = 0
    number = generate_number()
    print(number)
    hot_amount = guessing_loop(hot_amount, turn, number)
    win = final_print(hot_amount)
    return win


if __name__ == '__main__':
    main()
