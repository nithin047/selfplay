from Board import Board
from UserInterface import UserInterface
import logging
from GameManager import *
import helper_functions as hf


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    # use this initial position for debugging. Instead of starting from the beginning of the game, one can start from
    # this position instead to save time and target corner cases.
    initial_position = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 1, 2, 2, 0, 0, 0, 1, 2, 2, 0, 0, 1, 1],
                        [3, 2, 1, 7, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    initial_position = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0],
                        [12, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0]]

    # initial dice state
    dice_values = [6, 6]

    # instantiate board object with given initial position
    my_board = Board(24, 15, initial_position)

    # test afterstates functions.
    # TODO: afterstate functions work well for regular states, but will need to be defined for the endgame
    afterstates1 = hf.get_possible_afterstates_single_dice(my_board, dice_values[0], 1)
    afterstates2 = hf.get_possible_afterstates_single_dice(my_board, dice_values[1], 1)
    afterstates = hf.get_action_space(my_board, dice_values, 1)

    # instantiate game manager object. No input parameters: starts the game at the beginning.
    # Alternatively, the object may take initial conditions to start at a desired position.
    # my_game_manager = GameManager()
    my_game_manager = GameManager(my_board, GameState.PLAYER_1_TURN, dice_values)

    # Instantiate GUI object
    my_gui = UserInterface(my_game_manager)
