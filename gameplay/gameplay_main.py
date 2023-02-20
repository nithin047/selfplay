from game_framework.UserInterface import UserInterface
from game_framework.GameManager import *
from game_framework.LogManager import LogManager
from game_framework import helper_functions as hf
from model.define_model import initialize_ml_model

import numpy as np
import torch
import copy as cp


def game_playthrough(cfg):
    """
    Function that plays through a full game of backgammon, using a model for decision making
    :param gameplay_cfg:
    :return:
    """

    enable_logs = True
    gameplay_cfg = cfg['gameplay']
    model_cfg = cfg['model']

    model_choice = gameplay_cfg['model_choice']

    if model_choice == 'random':
        model = initialize_ml_model(model_cfg)
    else:
        raise ValueError(f'Undefined model choice {model_choice} for gameplay provided!')

    #start game
    game_manager = GameManager(None, None, None, enable_logs)
    end_of_game_flag = False

    while not end_of_game_flag:

        # roll dice
        stuck_player_flag = game_manager.dice_rolled()
        if stuck_player_flag:
            continue
        # get possible action states
        afterstates, _, _ = hf.get_action_space(game_manager.game_board, game_manager.current_dice, game_manager.current_game_state.value % 2)

        # check if at least one move is possible
        if afterstates:
            if len(afterstates) == 1:
            # only one move is possible
                best_afterstate = afterstates[0]
            else:
                # create list of afterstate values
                afterstate_values = []
                for afterstate in afterstates:
                    afterstate_value = model(torch.from_numpy(afterstate.board_state.flatten()).float())
                    afterstate_values.append(afterstate_value.numpy(force=True)[0])

                # if move is possible, determine best move
                best_afterstate = afterstates[np.argmax(afterstate_values)]

            # play best move
            game_manager.game_board = cp.deepcopy(best_afterstate)

        # check for end of game
        end_of_game_flag = game_manager.is_game_over()

        if not end_of_game_flag:
            if game_manager.current_game_state == GameState.PLAYER_1_TURN:
                game_manager.transition_to_state(GameState.PLAYER_2_DICE_ROLL)
            elif game_manager.current_game_state == GameState.PLAYER_2_TURN:
                game_manager.transition_to_state(GameState.PLAYER_1_DICE_ROLL)







