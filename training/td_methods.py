"""
Implementations of TD-learning methods for backgammon
"""
import numpy as np
from tqdm import trange

# TODO: remove dependency on environment
# TODO: resolve absence of Policy class -- use afterstates!
# TODO: make specific to backgammon use case and to self-play
def semi_gradient_n_step_td(env,
                            gamma:float,
                            pi:Policy,
                            n:int,
                            alpha:float,
                            V:ValueFunctionWithApproximation,
                            num_episode:int):
    """
    implement n-step semi gradient TD for estimating v
    implementation is according to algorithm described just prior to eq. 9.15 in S&B
    input:
        env: target environment
        gamma: discounting factor
        pi: target evaluation policy
        n: n-step
        alpha: learning rate
        V: value function
        num_episode: episodes to iterate
    output:
        None
    """
    for _ in trange(num_episode):

        R = []
        S = []
        state, r, done = env.reset(), 0., False
        S.append(state)
        T = np.Inf
        t = 0

        while t <= T+n-2:

            if t<T:

                state = S[t]
                a = pi.action(state)
                next_state, r, done, info = env.step(a)
                R.append(r)
                S.append(next_state)
                if done:
                    T = t+1
            tau = t - n + 1
            if tau >= 0:
                G = 0
                for ii in range(tau+1, min(tau+n, T) + 1):
                    G = G + gamma**(ii - tau - 1) * R[ii-1]
                if tau+n<T:
                    G = G + gamma**n * V(S[tau+n])
                V.update(alpha, G, S[tau])

            t = t+1