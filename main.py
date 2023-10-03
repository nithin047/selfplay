import xmltodict
import argparse
import numpy.random as rd
import torch
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

    # set random seed for reproducibility
    random_seed = cfg_dict.get('global_random_seed', None)
    if random_seed is not None:
        rd.seed(random_seed)
        torch.manual_seed(random_seed)

    if main_cfg['game_playthrough']:
        game_result, log_file_path = game_playthrough(cfg_dict)
        if game_result > 0:
            print(f'White wins by {abs(game_result)} points!')
        else:
            print(f'Black wins by {abs(game_result)} points!')

    if main_cfg['log_runthrough']:
        if cfg_dict['log_runthrough']['use_cfg_log_path']:
            log_file_path = cfg_dict['log_runthrough']['log_path']

        # Instantiate GUI object and playthrough the log
        my_log_animation_gui = UserInterfaceLogAnimation(log_file_path)


