import os
import time
import random
import highscore
from environment import *
from controls import *
from display import *
from actions import *


def main():
    intro()
    character_name, character_color = create_player()
    level = 0
    # sets parameters of next game level
    inventory = {}
    game_won, level, inventory, board, x_player, y_player, minions_location = setting_next_level(level, inventory)

    button_pressed = ''
    health = 30  # player's initial health points
    lamps_lit = 0
    hamster_energy = 600
    game_won = False
    start_time = time.time()

    print_level_title(level - 1)

    while button_pressed != '\\' and health > 0 and not game_won:   # game end conditions
        # update text info on board
        board = update_board_information(board, level, character_name, health, inventory, start_time, hamster_energy)
        manage_display(board, x_player, y_player, character_color)   # creates current frame of game animation
        board, minions_location = move_minions(board, minions_location, character_color)

        button_pressed = getch()    # reads button pressed by user

        if button_pressed == 'i':
            print_additional_game_info(inventory)

        # developer_cheat_mode
        if button_pressed == ',':
            x_player = 114
            y_player = 37

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
        # opens passage to the next level
        board = enable_level_exit(board, level, inventory, lamps_lit)
        # checks if level end conditions were met
        next_level = checking_level_end(level, inventory, x_player, y_player, hamster_energy, board)

        if next_level:
            # sets parameters of next game level
            game_won, level, inventory, board, x_player, y_player, minions_location = setting_next_level(
                level, inventory)
            if level in [1, 2, 3, 4]:
                print_level_title(level - 1)

    print_end_image(game_won)
    highscore.manage_highscores(game_won, health, your_time, character_name)


if __name__ == '__main__':
    main()
