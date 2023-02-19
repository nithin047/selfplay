import torch
import torch.nn as nn
import numpy.random as rn

from model.model_utils import get_activation


class GeneralMLP(nn.Module):

    def __init__(self, input_size, output_size, hidden_layers, hidden_layer_activation, output_activation):

        super(GeneralMLP, self).__init__()

        self.num_hidden_layers = len(hidden_layers)
        self.hidden_layer_activation = hidden_layer_activation
        self.output_activation = output_activation

        self.layer_list = []

        self.layer_list.append(nn.Linear(input_size, int(hidden_layers[0])))
        for layer_num in range(1, self.num_hidden_layers):
            self.layer_list.append((nn.Linear(int(hidden_layers[layer_num - 1]), int(hidden_layers[layer_num]))))
        self.layer_list.append(nn.Linear(int(hidden_layers[self.num_hidden_layers - 1]), output_size))

    def forward(self, x):

        hidden_layer_activation_fn = get_activation(self.hidden_layer_activation)
        output_activation_fn = get_activation(self.output_activation)

        for layer_num in range(self.num_hidden_layers):
            x = hidden_layer_activation_fn(self.layer_list[layer_num](x))

        x = output_activation_fn(self.layer_list[self.num_hidden_layers](x))

        return x


if __name__ == "__main__":

    test_model = GeneralMLP(5, 6, [5, 4, 7], 'relu', 'softmax')
    test_input = rn.rand(5)
    test_output = test_model(torch.from_numpy(test_input).float())
    print(test_output)