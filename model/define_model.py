from model.mlp import GeneralMLP


def initialize_ml_model(model_cfg):

    model_type = model_cfg['model_type'].lower()
    input_size = model_cfg['input_size']
    output_size = model_cfg['output_size']
    hidden_layers = model_cfg['hidden_layers']
    hidden_layer_activation = model_cfg['hidden_layer_activation'].lower()
    output_activation = model_cfg['output_activation'].lower()

    if model_type == 'mlp':
        return GeneralMLP(input_size, output_size, hidden_layers, hidden_layer_activation, output_activation)

    else:
        raise ValueError(f'Undefined model type {model_type} provided!')




