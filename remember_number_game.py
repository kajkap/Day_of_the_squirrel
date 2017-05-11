import random
import time
import os


def initial_print():
    """Function prints the game instruction."""

    os.system('clear')
    print("""
    *** Remember telephone number!
    Write it down in the same format (divided into 3-digits blocks)***
    """)


def generate_number():
    """Function generates 9 random digits.

    Return:
        number (int): 9-digit number
    """

    number = []
    for i in range(3):
        for i in range(3):
            number.append(str(random.randint(0, 9)))
        number.append(' ')
    number = (''.join(number)).strip(' ')
    print('telephone: ', number)
    return number


def guessing():
    """Function asks user for typing remembered number.

    Return:
        guess (int): user's answer
    """

    guess = input()
    return guess


def check_answer(number, guess):
    """Function checks if the user's answer is correct.

    Args:
        number (int): generated number
        guess (int): user's guess

    Return:
        won (bool): True if the user's answer is correct, False otherwise
    """

    win = False
    if guess != number:
        print('Wrong answer. Try again')
        time.sleep(2)
    else:
        print('Well done!')
        time.sleep(2)
        win = True
    return win


def main():
    guess = ''
    number = '0'
    while guess != number:
        initial_print()
        number = generate_number()
        time.sleep(5)
        initial_print()
        guess = guessing()
        win = check_answer(number, guess)
    return win


if __name__ == '__main__':
    main()
