from enum import Enum
import random as rd
import logging
from game_framework.Board import Board
import numpy as np
from game_framework import helper_functions as hf
from game_framework.LogManager import LogManager


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

        # indicates whether both dice are playable (and need to be played)
        self.are_both_dice_playable = True

        # import initial conditions or display 6,6 with starting position by default
        if dice is None:
            self.current_dice = [6, 6]
            self.remaining_dice_moves = []
        else:
            self.dice_rolled(dice_roll=dice)
            # self.current_dice = dice
            #
            # if dice[0] == dice[1]:
            #     self.remaining_dice_moves = [dice[0], dice[0], dice[0], dice[0]]
            # else:
            #     self.remaining_dice_moves = dice

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

    def determine_first_player(self):
        # This function selects a first player at random
        first_player = rd.randint(1, 2)
        if first_player == 1:
            self.transition_to_state(GameState.PLAYER_1_DICE_ROLL)
            logging.info("White Starts!")
        else:
            self.transition_to_state(GameState.PLAYER_2_DICE_ROLL)
            logging.info("Black Starts!")

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

        if dice_1 != dice_2:
            afterstates, forced_dice, self.are_both_dice_playable \
                = hf.get_action_space(self.game_board, self.current_dice, current_player)

            if forced_dice == dice_1:
                self.remaining_dice_moves = [dice_1]
                logging.info('Forced to play die %s', dice_1)
            elif forced_dice == dice_2:
                self.remaining_dice_moves = [dice_2]
                logging.info('Forced to play die %s', dice_2)
            elif forced_dice == 0:
                self.remaining_dice_moves = [dice_1, dice_2]
            else:
                logging.error("Dice roll error")
                assert False

        else:
            self.remaining_dice_moves = [dice_1, dice_1, dice_1, dice_1]

        # if white's turn
        if current_player == 0:
            self.transition_to_state(GameState.PLAYER_1_TURN)

            # if white is stuck, end turn
            if self.is_player_stuck():
                logging.info('Player stuck! Switching turns.')
                # self.log_manager.set_player(1)
                # self.log_manager.write_move_to_log()
                self.transition_to_state(GameState.PLAYER_2_DICE_ROLL)
                logging.info('Game State Changed: %s --> %s', GameState.PLAYER_1_TURN, GameState.PLAYER_2_DICE_ROLL)

        # else if black's turn
        elif current_player == 1:
            self.transition_to_state(GameState.PLAYER_2_TURN)

            # if black is stuck, end turn
            if self.is_player_stuck():
                logging.info('Player stuck! Switching turns.')
                # self.log_manager.set_player(1)
                # self.log_manager.write_move_to_log()
                self.transition_to_state(GameState.PLAYER_1_DICE_ROLL)
                logging.info('Game State Changed: %s --> %s', GameState.PLAYER_2_TURN, GameState.PLAYER_1_DICE_ROLL)

    def is_valid_move(self, destination_slot):
        # This functions returns true if the destination slot leads to a valid move, assuming the origin slot is the
        # current_selected_slot

        # if regular move
        if destination_slot >= 0:
            # if white's turn
            if self.current_game_state == GameState.PLAYER_1_TURN:

                # invalid move if land on occupied of pinned slot
                if self.game_board.board_state[1, destination_slot] > 1 \
                        or self.game_board.board_state[2, destination_slot] == -1:
                    return False

                # else it's a valid move if one of the dice corresponds to the desired jump
                else:
                    for i in range(len(self.remaining_dice_moves)):
                        local_dice_value = self.remaining_dice_moves[i]
                        if self.current_selected_slot + local_dice_value == destination_slot:
                            if len(self.remaining_dice_moves) == 2:
                                future_remaining_dice_move = self.remaining_dice_moves[1-i]
                                if self.are_both_dice_playable and hf.would_move_get_player_stuck(self.game_board, self.current_selected_slot, destination_slot, 0, future_remaining_dice_move):
                                    return False
                            return True

            # else if black's turn
            elif self.current_game_state == GameState.PLAYER_2_TURN:

                # invalid move if land on occupied of pinned slot
                if self.game_board.board_state[0, destination_slot] > 1 \
                        or self.game_board.board_state[2, destination_slot] == 1:
                    return False

                # else it's a valid move if one of the dice corresponds to the desired jump
                else:
                    for i in range(len(self.remaining_dice_moves)):
                        local_dice_value = self.remaining_dice_moves[i]
                        if self.current_selected_slot - local_dice_value == destination_slot:
                            if len(self.remaining_dice_moves) == 2:
                                future_remaining_dice_move = self.remaining_dice_moves[1 - i]
                                if self.are_both_dice_playable and hf.would_move_get_player_stuck(self.game_board, self.current_selected_slot, destination_slot, 1, future_remaining_dice_move):
                                    return False
                            return True
            else:
                logging.error("State Error")
                assert False

        # else if endgame
        elif destination_slot == -1:
            # if white's turn
            if self.current_game_state == GameState.PLAYER_1_TURN and self.game_board.is_white_endgame():
                # loop over remaining dice moves
                for i in range(len(self.remaining_dice_moves)):
                    local_dice_value = self.remaining_dice_moves[i]

                    # valid move if the jump corresponds exactly to the dice value
                    if local_dice_value == self.game_board.n_slots - self.current_selected_slot:
                        return True
                    # valid move if the dice value is larger than the jump and no further pieces are still there
                    elif local_dice_value > self.game_board.n_slots - self.current_selected_slot \
                            and np.all(self.game_board.board_state[0,
                                       round(self.game_board.n_slots * 0.75):self.current_selected_slot] == 0):
                        return True
            # else if black's turn
            elif self.current_game_state == GameState.PLAYER_2_TURN and self.game_board.is_black_endgame():
                # loop over remaining dice moves
                for i in range(len(self.remaining_dice_moves)):
                    local_dice_value = self.remaining_dice_moves[i]

                    # valid move if the jump corresponds exactly to the dice value
                    if local_dice_value == self.current_selected_slot + 1:
                        return True
                    # valid move if the dice value is larger than the jump and no further pieces are still there
                    elif local_dice_value > self.current_selected_slot + 1 \
                            and np.all(self.game_board.board_state[1,
                                       self.current_selected_slot + 1:round(self.game_board.n_slots * 0.25)] == 0):
                        return True

            else:
                logging.error("State Error")
                assert False

        else:
            logging.error("Destination Error")
            assert False

        return False

    def remove_value_from_remaining_dice_moves(self, value_to_remove):
        # This function removes a specific dice value from the remaining_dice_moves list after it has been played
        self.remaining_dice_moves.remove(value_to_remove)

        # check if game over
        if self.game_board.is_game_over_player_1() == 1:
            self.transition_to_state(GameState.PLAYER_1_GAME_OVER_1_POINT)
            self.log_manager.set_player(0)
            self.log_manager.write_move_to_log()
            self.log_manager.write_log_to_file()
            logging.info('White wins! 1 Point.')
        elif self.game_board.is_game_over_player_1() == 2:
            self.transition_to_state(GameState.PLAYER_1_GAME_OVER_2_POINTS)
            self.log_manager.set_player(0)
            self.log_manager.write_move_to_log()
            self.log_manager.write_log_to_file()
            logging.info('White wins! 2 Points!')
        elif self.game_board.is_game_over_player_2() == 1:
            self.transition_to_state(GameState.PLAYER_2_GAME_OVER_1_POINT)
            self.log_manager.set_player(1)
            self.log_manager.write_move_to_log()
            self.log_manager.write_log_to_file()
            logging.info('Black wins! 1 Point.')
        elif self.game_board.is_game_over_player_2() == 2:
            self.transition_to_state(GameState.PLAYER_2_GAME_OVER_2_POINTS)
            self.log_manager.set_player(1)
            self.log_manager.write_move_to_log()
            self.log_manager.write_log_to_file()
            logging.info('Black wins! 2 Points!')
        else:

            # check if player is stuck
            is_current_player_stuck = self.is_player_stuck()

            # if remaining_dice_moves is empty or if player stuck, switch turns
            if not self.remaining_dice_moves or is_current_player_stuck:

                # self.log_manager.write_move_to_log()

                if is_current_player_stuck and self.remaining_dice_moves:
                    logging.info('Player stuck! Switching turns.')

                if self.current_game_state == GameState.PLAYER_1_TURN:
                    self.transition_to_state(GameState.PLAYER_2_DICE_ROLL)
                    # logging.info('Game State Changed: %s --> %s', GameState.PLAYER_1_TURN, GameState.PLAYER_2_DICE_ROLL)
                elif self.current_game_state == GameState.PLAYER_2_TURN:
                    self.transition_to_state(GameState.PLAYER_1_DICE_ROLL)
                    # logging.info('Game State Changed: %s --> %s', GameState.PLAYER_2_TURN, GameState.PLAYER_1_DICE_ROLL)
                else:
                    logging.error("State Error")
                    return False

    def is_player_stuck(self):
        # This function checks whether the player is stuck

        # figure out the player's turn and return false if we are in this player's endgame
        if self.current_game_state == GameState.PLAYER_1_TURN:
            player_id = 0
            if self.game_board.is_white_endgame():
                return False
        elif self.current_game_state == GameState.PLAYER_2_TURN:
            player_id = 1
            if self.game_board.is_black_endgame():
                return False
        else:
            logging.error("State Error")
            assert False

        # run the afterstate function and check if empty. Empty means stuck.
        for i in range(len(self.remaining_dice_moves)):
            action_space = hf.get_possible_afterstates_single_dice(self.game_board,
                                                                   self.remaining_dice_moves[i],
                                                                   player_id)

            # if action_space is not empty, player is not stuck
            if action_space:
                return False

        return True

    def move_piece_from_slot_to_slot(self, origin, destination, player_id):
        is_successful_move = self.game_board.move_piece_from_slot_to_slot(origin, destination, player_id)
        if is_successful_move:
            self.log_manager.add_move(origin, destination)

        return is_successful_move


