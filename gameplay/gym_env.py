import gymnasium as gym
from gymnasium import spaces
import os

from game_framework.UserInterface import UserInterface
from game_framework.GameManager import GameState, GameManager
from game_framework.LogManager import LogManager
from game_framework import helper_functions as hf
from model.define_model import initialize_ml_model
from backgammon_agent import BackgammonAgent

class BackgammonEnv(gym.Env):

    def __init__(self, cfg):

        self.enable_logs = True
        self.gameplay_cfg = cfg['gameplay']

        # start game by initializing GameManager
        self.game_manager = GameManager(None, None, None, self.enable_logs)

        # initialize backgammon agent
        self.agent = BackgammonAgent()

        # get log file path for this particular walkthrough
        self.log_file_path = os.path.join(os.getcwd(),
                                     self.game_manager.log_manager.outfolder_name,
                                     self.game_manager.log_manager.outfile_name)

        # initialize a flag that will tell us when to end the game loop below
        self.end_of_game_flag = False

        # initializing some standard variables that we don't use to None
        self.observation_space = None
        self.action_space = None

    def observation_from_board_state(self):
        """
        This method takes the board state and converts it to an observation that can be fed to the model
        :return:
        """
        # for now, identity passthrough
        return self.game_manager.game_board.board_state

    def reset(self, seed=None, options=None):

        # We need the following line to seed self.np_random
        super().reset(seed=seed)

        # reinitialize GameManager
        self.game_manager = GameManager(None, None, None, self.enable_logs)

        # reinitialize a flag that will tell us when to end the game loop
        self.end_of_game_flag = False

        observation = self.observation_from_board_state()

        return observation, {}

    def step(self, action):

        # roll dice -- this function implicitly checks and handles the situation where a player is stuck
        stuck_player_flag = self.game_manager.dice_rolled()
        if stuck_player_flag:
            return self.observation_from_board_state(), 0, False, False, {}

        # make sure that it is a player's turn
        assert (self.game_manager.current_game_state == GameState.PLAYER_1_TURN) or (self.game_manager.current_game_state == GameState.PLAYER_2_TURN), 'game state is not a player\'s turn!'

        # figure out which player's turn it is
        current_player_id = self.game_manager.get_current_player_id()

        # get possible action states
        afterstates, _, _ = hf.get_action_space(self.game_manager.game_board, self.game_manager.current_dice, current_player_id)

        return observation, reward, terminated, truncated, info





