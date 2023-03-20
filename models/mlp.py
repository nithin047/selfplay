import torch
import torch.nn as nn
import torch.nn.functional as F

class generalMLP(nn.Module):

    def __init__(self, input_size=100, hidden_layers=[50, 50], output_size=10):

        super(generalMLP, self).__init__()

        num_hidden_layers = len(hidden_layers)

        for ii, hidden_layer_size in hidden_layers:
            if ii == 1:
                