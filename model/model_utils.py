import torch
import torch.nn
import torch.nn.functional as F


def get_activation(activation_type):

    if activation_type.lower() == 'relu':
        return F.relu
    elif activation_type.lower() == 'softmax':
        return lambda x: F.softmax(x, dim=0)
    else:
        raise ValueError(f'Undefined activation function {activation_type.lower()} provided!')