from game_framework.GameManager import GameManager
from game_framework.UserInterface import UserInterface
import numpy as np
import time


class UserInterfaceLogAnimation(UserInterface):
    def __init__(self, log_file_path):
        my_game_manager = GameManager(None, None, None, False)
        UserInterface.__init__(self, my_game_manager, 2)

        self.log_file_path = log_file_path
        self.player_list = []
        self.source_move_list = []
        self.destination_move_list = []
        self.dice_1_list = []
        self.dice_2_list = []
        self.load_log()

        self.board_canvas.bind("<Button-1>", self.on_button_click_animation_mode)
        self.window.mainloop()

    def load_log(self):
        with open(self.log_file_path) as f:
            lines = f.readlines()  # list containing lines of file

            for line in lines:
                line = line.strip()  # remove leading/trailing white spaces
                if line:
                    if line[0] != "*":
                        split_data = line[15:].replace(' ', '/')
                        split_data = split_data.split('/')

                        while split_data:
                            self.player_list.append(int(line[7]))
                            self.dice_1_list.append(int(line[10]))
                            self.dice_2_list.append(int(line[12]))

                            if split_data[0] != 'X':
                                self.source_move_list.append(int(split_data[0]))
                                self.destination_move_list.append(int(split_data[1]))
                                del split_data[0:2]
                            else:
                                self.source_move_list.append(-2)
                                self.destination_move_list.append(-2)
                                del split_data[0]

    def on_button_click_animation_mode(self, event):
        x_click_coord = event.x
        y_click_coord = event.y

        for i in range(len(self.player_list)):
            if i == 0 or self.player_list[i] != self.player_list[i - 1]:
                self.dice_vals = [self.dice_1_list[i], self.dice_2_list[i]]
                self.game_manager.dice_rolled(self.dice_vals)
                self.on_refresh_gui_event()
                self.window.update()
                time.sleep(0.3)
            self.on_slot_click(self.source_move_list[i])
            self.on_refresh_gui_event()
            self.window.update()
            time.sleep(0.3)
            if self.destination_move_list[i] != -1:
                self.on_slot_click(self.destination_move_list[i])
            elif self.player_list[i] == 1:
                self.on_white_arrow_click()
            elif self.player_list[i] == 2:
                self.on_black_arrow_click()
            else:
                assert False
            self.on_refresh_gui_event()
            self.window.update()
            time.sleep(0.3)

        a = 0

    def run_animation_mode(self):
        for i in range(len(self.player_list)):
            time.sleep(0.5)
            self.dice_vals = [self.dice_1_list[0], self.dice_1_list[1]]
            self.game_manager.dice_rolled(self.dice_vals)
            self.on_refresh_gui_event()
            break

