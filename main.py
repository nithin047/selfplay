import xmltodict
import argparse
from model.define_model import initialize_ml_model

from game_framework.UserInterface import UserInterface
from game_framework.GameManager import *
from game_framework.UserInterfaceLogAnimation import UserInterfaceLogAnimation
from game_framework.UserInterfaceGameplay import UserInterfaceGameplay
from game_framework import helper_functions as hf
from utilities.format_cfg import format_cfg
from gameplay.gameplay_main import game_playthrough

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

    if main_cfg['test_functionality']:
        # use this initial position for debugging. Instead of starting from the beginning of the game, one can start
        # from this position instead to save time and target corner cases.
        # initial_position = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 1, 2, 2, 0, 0, 0, 1, 2, 2, 0, 0, 1, 1],
        #                     [3, 2, 1, 7, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

        # initial_position = [[2, 2, 2, 2, 2, 2, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 15],
        #                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

        initial_position = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 14, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 14, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

        final_position = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 14, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

        # initial dice state
        dice_values = [6, 6]

        # instantiate board object with given initial position
        my_board = Board(24, 15, initial_position)
        my_board2 = Board(24, 15, final_position)

        # test afterstates functions.
        # afterstates1 = hf.get_possible_afterstates_single_dice(my_board, dice_values[0], 1)
        # afterstates2 = hf.get_possible_afterstates_single_dice(my_board, dice_values[1], 1)
        afterstates, _, _ = hf.get_action_space(my_board, dice_values, 1)

        source_destination_list = hf.determine_moves_from_board_change(my_board, my_board2, dice_values, 1, True)

    if main_cfg['enable_gui']:
        enable_logs = bool(main_cfg['enable_logs'])

        log_file_path = "Logs/20230310/game_log_20230310_002406.txt"
        my_game_manager = GameManager(None, None, None, enable_logs)
        # my_game_manager = GameManager(my_board, GameState.PLAYER_1_TURN, dice_values, False)

        # Instantiate GUI object
        my_gameplay_gui = UserInterfaceGameplay(my_game_manager)
        my_log_animation_gui = UserInterfaceLogAnimation(log_file_path)

    if main_cfg['init_model']:
        model = initialize_ml_model(cfg_dict['model'])

    if main_cfg['game_playthrough']:
        game_playthrough(cfg_dict)
