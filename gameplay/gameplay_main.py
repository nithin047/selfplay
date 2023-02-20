from game_framework.UserInterface import UserInterface
from game_framework.GameManager import *
from game_framework.LogManager import LogManager
from game_framework import helper_functions as hf


def game_playthrough(gameplay_cfg):

    enable_logs = True

    #start game
    game_manager = GameManager(None, None, None, enable_logs)
    # roll dice
    game_manager.dice_rolled()
    # get possible action states
    afterstates, _, _ = hf.get_action_space(game_manager.game_board, game_manager.current_dice, game_manager.current_game_state.value%2)

    # TODO: check if at least one move is possible

    # TODO: if move is possible, determine best move

    # TODO: play best move

    # TODO: switch players

    # TODO: check for end of game

    # TODO: loop until end of game







