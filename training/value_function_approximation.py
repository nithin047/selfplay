"""
Classes and associated methods that implement value function approximation using an ANN
"""
import torch
from torch import optim
from model.define_model import initialize_ml_model

class ValueFunctionWithApproximation(object):
    def __call__(self, s) -> float:
        """
        return the value of given state; \hat{v}(s)

        input:
            state
        output:
            value of the given state
        """
        raise NotImplementedError()

    def update(self, alpha, G, s_tau):
        """
        Relevant sections of S&B:
        9.1 -- summary of general value function update steps
        Implementing the general update rule (e.g., equation 9.15 or the box immediately prior, in S&B)
        w <- w + \alpha[G- \hat{v}(s_tau;w)] \nabla \hat{v}(s_tau;w)

        input:
            alpha: learning rate
            G: update target
            s_tau: target state for updating (note that update will affect some other states)
        output:
            None
        """
        raise NotImplementedError()

class ValueFunctionWithNN(ValueFunctionWithApproximation):
    def __init__(self, cfg):
        """
        cfg: config_dict
        """
        self.model_cfg = cfg['model']
        self.gameplay_cfg = cfg['gameplay']
        self.model_choice = self.gameplay_cfg['model_choice']

        if self.model_choice == 'random':
            self.model = initialize_ml_model(self.model_cfg)
        else:
            raise ValueError(f'Undefined model choice {self.model_choice} for gameplay provided!')

        self.model = self.model.float()

        # TODO: call this from optimizer_utils
        self.optimizer = optim.Adam(self.model.parameters(), lr=1e-3)

    def __call__(self, s):
        # TODO: implement zero value for terminal states
        s = torch.from_numpy(s)
        value = self.model(s.float())
        return float(value.data.numpy()[0])

    def update(self, alpha, G, s_tau):
        """
        Relevant sections of S&B:
        9.1 -- summary of general value function update steps
        Implementing the general update rule (e.g., equation 9.15 or the box immediately prior, in S&B)
        w <- w + \alpha[G- \hat{v}(s_tau;w)] \nabla \hat{v}(s_tau;w)

        input:
            alpha: learning rate
            G: update target
            s_tau: target state for updating (note that update will affect some other states)
        output:
            None
        """

        self.optimizer.zero_grad()
        s_tau = torch.from_numpy(s_tau)
        value = self.model(s_tau.float())
        v_hat = float(value.data.numpy()[0])
        loss = - alpha * (G - v_hat) * value
        loss.backward()
        self.optimizer.step()

        return None



