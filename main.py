import xmltodict
import argparse

from game_framework.UserInterface import UserInterface
from game_framework.GameManager import *
from game_framework import helper_functions as hf
from utilities.format_cfg import format_cfg

parser = argparse.ArgumentParser()
parser.add_argument('--xmlpath', nargs='?', default='./cfg/default_backgammon_cfg.xml', type=str)
args = parser.parse_args()

cfg_path = args.xmlpath

if __name__ == '__main__':

    with open(cfg_path) as f:
        cfg_file = f.read()
    cfg_dict = format_cfg(xmltodict.parse(cfg_file))

    main_cfg = cfg_dict['main_options']

    logging.basicConfig(level=logging.INFO)

    # use this initial position for debugging. Instead of starting from the beginning of the game, one can start from
    # this position instead to save time and target corner cases.
    # initial_position = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 1, 2, 2, 0, 0, 0, 1, 2, 2, 0, 0, 1, 1],
    #                     [3, 2, 1, 7, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    initial_position = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0],
                        [12, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0]]


    # initial dice state
    dice_values = [6, 1]

    # instantiate board object with given initial position
    my_board = Board(24, 15, initial_position)

    # test afterstates functions.
    afterstates1 = hf.get_possible_afterstates_single_dice(my_board, dice_values[0], 0)
    afterstates2 = hf.get_possible_afterstates_single_dice(my_board, dice_values[1], 0)
    afterstates = hf.get_action_space(my_board, dice_values, 0)

    # instantiate game manager object. No input parameters: starts the game at the beginning.
    # Alternatively, the object may take initial conditions to start at a desired position.
    my_game_manager = GameManager()
    # my_game_manager = GameManager(my_board, GameState.PLAYER_1_TURN, dice_values)

    if int(main_cfg['enable_gui']):
        # Instantiate GUI object
        my_gui = UserInterface(my_game_manager)
