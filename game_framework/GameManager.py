from enum import Enum
import random as rd
import logging
from game_framework.Board import Board
import numpy as np
from game_framework import helper_functions as hf
from game_framework.LogManager import LogManager
import copy as cp


# Enum listing all the possible game states
class GameState(Enum):
    PLAYER_SELECTION = 0
    PLAYER_1_TURN = 1
    PLAYER_2_TURN = 2
    PLAYER_1_DICE_ROLL = 3
    PLAYER_2_DICE_ROLL = 4
    PLAYER_1_GAME_OVER_1_POINT = 5
    PLAYER_2_GAME_OVER_1_POINT = 6
    PLAYER_1_GAME_OVER_2_POINTS = 7
    PLAYER_2_GAME_OVER_2_POINTS = 8


class GameManager:
    def __init__(self, board=None, state=None, dice=None, enable_logs=False):
        self.current_game_state = GameState.PLAYER_SELECTION
        logging.info('Game State Changed: --> PLAYER_SELECTION')

        self.is_log_enabled = enable_logs
        self.log_manager = LogManager(self.is_log_enabled)

        # contains the slot id that is currently selected by the player
        self.current_selected_slot = -1

        # contains all valid afterstates after each dice roll
        self.afterstates = []

        # contains all valid afterstates and intermediate states after each dice roll
        self.combined_afterstates_and_intermediate_states = []

        # contains remaining dice for all valid afterstates and intermediate states after each dice roll
        self.combined_afterstates_and_intermediate_states_remaining_dice = []

        # import initial conditions or display 6,6 with starting position by default
        if board is None:
            self.game_board = Board(24, 15)
        else:
            self.game_board = board

        if state is None:
            if board is None:
                self.determine_first_player()
            else:
                self.current_game_state = GameState.PLAYER_1_DICE_ROLL
                logging.info('Game State Changed: --> %s', GameState.PLAYER_1_DICE_ROLL)
        else:
            self.current_game_state = state

        if dice is None:
            self.current_dice = [6, 6]
            # self.remaining_dice_moves = []
        else:
            if self.current_game_state == GameState.PLAYER_1_TURN:
                self.current_game_state = GameState.PLAYER_1_DICE_ROLL
            elif self.current_game_state == GameState.PLAYER_2_TURN:
                self.current_game_state = GameState.PLAYER_2_DICE_ROLL
            self.dice_rolled(dice_roll=dice)

    def transition_to_state(self, new_state):
        # This function transitions the game state to new_state
        old_state = self.current_game_state
        self.current_game_state = new_state

        if new_state == GameState.PLAYER_SELECTION:
            old_state = new_state

        logging.info('Game State Changed: %s --> %s', old_state, new_state)

        if new_state == GameState.PLAYER_1_DICE_ROLL:
            if old_state != GameState.PLAYER_SELECTION:
                self.log_manager.set_player(1)
                self.log_manager.write_move_to_log()
            self.log_manager.set_player(0)
        elif new_state == GameState.PLAYER_2_DICE_ROLL:
            if old_state != GameState.PLAYER_SELECTION:
                self.log_manager.set_player(0)
                self.log_manager.write_move_to_log()
            self.log_manager.set_player(1)

    def determine_first_player(self, player_id=None):
        # This function selects a first player at random or from input if provided
        if player_id is None:
            first_player = rd.randint(0, 1)
        else:
            first_player = player_id

        if first_player == 0:
            self.transition_to_state(GameState.PLAYER_1_DICE_ROLL)
            logging.info("White Starts!")
        else:
            self.transition_to_state(GameState.PLAYER_2_DICE_ROLL)
            logging.info("Black Starts!")

    def get_current_player_id(self):
        # returns current player id using current game state

        if self.current_game_state == GameState.PLAYER_1_TURN or self.current_game_state == GameState.PLAYER_1_DICE_ROLL:
            return 0
        elif self.current_game_state == GameState.PLAYER_2_TURN or self.current_game_state == GameState.PLAYER_2_DICE_ROLL:
            return 1
        else:
            return -1

    def dice_rolled(self, dice_roll=None):
        # This function rolls the dice and populates the remaining_dice_moves list

        if dice_roll is None:
            dice_1, dice_2 = hf.roll_dice(6)
        else:
            dice_1 = dice_roll[0]
            dice_2 = dice_roll[1]

        self.current_dice = [dice_1, dice_2]
        self.log_manager.set_dice_roll(self.current_dice)

        if self.current_game_state == GameState.PLAYER_1_DICE_ROLL:
            current_player = 0
        elif self.current_game_state == GameState.PLAYER_2_DICE_ROLL:
            current_player = 1
        else:
            logging.error("Wrong State Transition from dice roll")
            assert False

        self.afterstates, \
            self.combined_afterstates_and_intermediate_states, \
            self.combined_afterstates_and_intermediate_states_remaining_dice \
            = hf.get_action_space(self.game_board, self.current_dice, current_player)

        # if white's turn
        if current_player == 0:
            self.transition_to_state(GameState.PLAYER_1_TURN)

            # if white is stuck, end turn
            if self.is_current_board_state_afterstate():
                logging.info('Player stuck! Switching turns.')
                self.transition_to_state(GameState.PLAYER_2_DICE_ROLL)
                logging.info('Game State Changed: %s --> %s', GameState.PLAYER_1_TURN, GameState.PLAYER_2_DICE_ROLL)
                return True
            else:
                return False

        # else if black's turn
        elif current_player == 1:
            self.transition_to_state(GameState.PLAYER_2_TURN)

            # if black is stuck, end turn
            if self.is_current_board_state_afterstate():
                logging.info('Player stuck! Switching turns.')
                self.transition_to_state(GameState.PLAYER_1_DICE_ROLL)
                logging.info('Game State Changed: %s --> %s', GameState.PLAYER_2_TURN, GameState.PLAYER_1_DICE_ROLL)
                return True
            else:
                return False

    def is_valid_move(self, destination_slot):
        # This functions returns true if the destination slot leads to a valid move, assuming the origin slot is the
        # current_selected_slot

        # if white's turn
        if self.current_game_state == GameState.PLAYER_1_TURN:
            current_player = 0
        # else if black's turn
        elif self.current_game_state == GameState.PLAYER_2_TURN:
            current_player = 1
        else:
            logging.error("State Error")
            assert False

        # look at what the board would look like if the move was played
        potential_next_board = cp.deepcopy(self.game_board)
        is_successful_move = potential_next_board.move_piece_from_slot_to_slot(self.current_selected_slot,
                                                                               destination_slot,
                                                                               current_player)

        if not is_successful_move:
            return False, []

        # look for this board in the combined_afterstates_and_intermediate_states list
        board_loc_in_combined_afterstates_and_intermediate_states_list = -1
        for i in range(len(self.combined_afterstates_and_intermediate_states)-1, -1, -1):
            # looping in reverse to take into account the corner case where a combined_afterstate and an
            # intermediate_afterstate are the same state. In this case we want to look at the remaining dice of the
            # intermediate_afterstate. The combined_afterstates have smaller indices than the
            # intermediate_afterstates..
            if potential_next_board == self.combined_afterstates_and_intermediate_states[i]:
                board_loc_in_combined_afterstates_and_intermediate_states_list = i
                break

        remaining_dice = self.combined_afterstates_and_intermediate_states_remaining_dice[
            board_loc_in_combined_afterstates_and_intermediate_states_list]

        if board_loc_in_combined_afterstates_and_intermediate_states_list != -1:
            return True, remaining_dice
        else:
            return False, []

    def move_piece_from_slot_to_slot(self, origin, destination, player_id):
        is_successful_move = self.game_board.move_piece_from_slot_to_slot(origin, destination, player_id)
        self.current_selected_slot = -1

        if is_successful_move:
            self.log_manager.add_move(origin, destination)

            # check if game is over
            if not self.is_game_over() and self.is_current_board_state_afterstate():
                if self.current_game_state == GameState.PLAYER_1_TURN:
                    self.transition_to_state(GameState.PLAYER_2_DICE_ROLL)
                elif self.current_game_state == GameState.PLAYER_2_TURN:
                    self.transition_to_state(GameState.PLAYER_1_DICE_ROLL)
                else:
                    logging.error("State Error")
                    return False

        return is_successful_move

    def is_current_board_state_afterstate(self):
        if not self.afterstates:
            # if no move available
            return True
        elif len(self.afterstates) == 1 and self.game_board == self.afterstates[0]:
            # if forced move
            return True

        for i in range(len(self.combined_afterstates_and_intermediate_states)-1, -1, -1):
            if self.game_board == self.combined_afterstates_and_intermediate_states[i]:
                # check whether this is not also an intermediate state
                if not self.combined_afterstates_and_intermediate_states_remaining_dice[i]:
                    return True
                else:
                    return False

        return False

    def is_game_over(self):

        # check if game over
        if self.game_board.is_game_over_player_1() == 1:
            self.transition_to_state(GameState.PLAYER_1_GAME_OVER_1_POINT)
            self.log_manager.set_player(0)
            self.log_manager.write_move_to_log()
            self.log_manager.mark_game_over(0, 1)
            self.log_manager.write_log_to_file()
            logging.info('White wins! 1 Point.')
            return 1

        elif self.game_board.is_game_over_player_1() == 2:
            self.transition_to_state(GameState.PLAYER_1_GAME_OVER_2_POINTS)
            self.log_manager.set_player(0)
            self.log_manager.write_move_to_log()
            self.log_manager.mark_game_over(0, 2)
            self.log_manager.write_log_to_file()
            logging.info('White wins! 2 Points!')
            return 2

        elif self.game_board.is_game_over_player_2() == 1:
            self.transition_to_state(GameState.PLAYER_2_GAME_OVER_1_POINT)
            self.log_manager.set_player(1)
            self.log_manager.write_move_to_log()
            self.log_manager.mark_game_over(1, 1)
            self.log_manager.write_log_to_file()
            logging.info('Black wins! 1 Point.')
            return 1

        elif self.game_board.is_game_over_player_2() == 2:
            self.transition_to_state(GameState.PLAYER_2_GAME_OVER_2_POINTS)
            self.log_manager.set_player(1)
            self.log_manager.write_move_to_log()
            self.log_manager.mark_game_over(1, 2)
            self.log_manager.write_log_to_file()
            logging.info('Black wins! 2 Points!')
            return 2

        else:
            return 0
