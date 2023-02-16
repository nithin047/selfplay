from datetime import *
import os


class LogManager:
    def __init__(self, log_enabled=False):
        self.log_data_string = []

        today = datetime.now()
        self.outfile_name = "game_log_" \
                            + str('%04.0f' % today.year) \
                            + str('%02.0f' % today.month) \
                            + str('%02.0f' % today.day) \
                            + "_" \
                            + str('%02.0f' % today.hour) \
                            + str('%02.0f' % today.minute) \
                            + str('%02.0f' % today.second) \
                            + ".txt"

        self.outfolder_name = "Logs\\" \
                              + str('%04.0f' % today.year) \
                              + str('%02.0f' % today.month) \
                              + str('%02.0f' % today.day)

        self.source_list = []
        self.destination_list = []
        self.dice_roll = []
        self.player_id = -1
        self.log_enabled = log_enabled

    def write_move_to_log(self):

        assert self.player_id >= 0
        # assert self.source_list
        # assert self.destination_list
        assert self.dice_roll

        logged_string = "Player " \
                        + str(self.player_id+1) \
                        + ": " \
                        + str(self.dice_roll[0]) \
                        + "-" \
                        + str(self.dice_roll[1]) \
                        + ": "

        for i in range(len(self.source_list)):
            logged_string += str(self.source_list[i]) + "/" + str(self.destination_list[i]) + " "

        self.log_data_string.append(logged_string)
        self.source_list = []
        self.destination_list = []
        self.dice_roll = []
        self.player_id = -1

    def add_move(self, source, destination):
        self.source_list.append(source)
        self.destination_list.append(destination)

    def set_player(self, player_id):
        self.player_id = player_id

    def set_dice_roll(self, dice_roll):
        self.dice_roll = dice_roll

    def write_log_to_file(self):
        if self.log_enabled:
            if not os.path.isdir(os.getcwd() + "\\" + self.outfolder_name):
                os.makedirs(os.getcwd() + "\\" + self.outfolder_name)

            with open(os.getcwd() + "\\" + self.outfolder_name + "\\" + self.outfile_name, "w+") as text_file:
                for i in range(len(self.log_data_string)):
                    text_file.write(self.log_data_string[i] + "\n")


