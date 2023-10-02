from game_framework.UserInterface import UserInterface
from game_framework.GameManager import *
from game_framework.LogManager import LogManager
from game_framework import helper_functions as hf
from model.define_model import initialize_ml_model

import numpy as np
import torch
import os
import copy as cp


def game_playthrough(cfg):
    """
    Function that plays through a full game of backgammon, using a model to pick the best action
    :param cfg:
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

    # start game by initializing GameManager
    game_manager = GameManager(None, None, None, enable_logs)

    # get log file path for this particular walkthrough
    log_file_path = os.path.join(os.getcwd(),
                                 game_manager.log_manager.outfolder_name,
                                 game_manager.log_manager.outfile_name)

    # initialize a flag that will tell us when to end the game loop below
    end_of_game_flag = False

    # begin the game loop
    while not end_of_game_flag:

        # roll dice -- this function implicitly checks and handles the situation where a player is stuck
        stuck_player_flag = game_manager.dice_rolled()
        if stuck_player_flag:
            continue

        # make sure that it is a player's turn
        assert (game_manager.current_game_state == GameState.PLAYER_1_TURN) or (game_manager.current_game_state == GameState.PLAYER_2_TURN), 'game state is not a player\'s turn!'

        # figure out which player's turn it is
        current_player_id = game_manager.get_current_player_id()

        # get possible action states
        afterstates, _, _ = hf.get_action_space(game_manager.game_board, game_manager.current_dice, current_player_id)

        if afterstates:
            if len(afterstates) == 1:
                # only one move is possible, so no inference is required and the move is not model-dependent
                best_afterstate = afterstates[0]
            else:
                # create list of afterstate values, and pass them through the model to obtain values for each of the afterstates
                afterstate_values = []
                for afterstate in afterstates:
                    afterstate_value = model(torch.from_numpy(afterstate.board_state.flatten()).float())
                    afterstate_values.append(afterstate_value.numpy(force=True)[0])

                # if move is possible, determine best move by picking the afterstate with the best value
                best_afterstate = afterstates[np.argmax(afterstate_values)]

            # determine best move
            source_destination_list = hf.determine_moves_from_board_change(start_board=game_manager.game_board,
                                                                           end_board=best_afterstate,
                                                                           dice_roll=game_manager.current_dice,
                                                                           player_id=current_player_id,
                                                                           enable_check=True)
            # play best move
            if current_player_id == 0:
                for i in range(len(source_destination_list)):
                    _, is_game_over_status = game_manager.move_piece_from_slot_to_slot(source_destination_list[i][0],
                                                                               source_destination_list[i][1],
                                                                               current_player_id)

                    # check for end of game, if so, break the loop
                    if is_game_over_status:
                        return is_game_over_status, log_file_path

            elif current_player_id == 1:
                for i in range(len(source_destination_list) - 1, -1, -1):
                    _, is_game_over_status = game_manager.move_piece_from_slot_to_slot(source_destination_list[i][0],
                                                                               source_destination_list[i][1],
                                                                               current_player_id)

                    # check for end of game, if so, break the loop
                    if is_game_over_status:
                        return is_game_over_status, log_file_path











