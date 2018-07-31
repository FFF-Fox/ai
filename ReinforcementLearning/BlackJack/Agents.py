import numpy as np

class FVMC(object):

    def __init__(self):
        # The default policy to be evaluated is sticking only on 20 or 21
        K = 200
        self.policy = ['hit' for i in range(K)]
        self.policy[-40:] = ['stick' for i in range(40)]

        self.V = np.zeros(K)
        self.Returns = [[] for s in range(K)]

    def update_values(self, episode_states, episode_rewards):
        """ Update the V(s) values after an episode finishes """
        for s in set(episode_states):
                i = episode_states.index(s)    # index of the first visit of state s
                R = sum(episode_rewards[i:])  # total return starting from first visit of s
                self.Returns[s].append(R)
                self.V[s] = np.mean(self.Returns[s])

    def train(self, env, total_episodes):
        """ Estimate the value of the states that the agent experiences. 
            1. Generate episode using the policy
            2. For each state appeared in the episode keep the return following the first
               occurence and average the Returns of each state visited in this episode. """
        for _ in range(total_episodes):
            episode_states = []     # the states that will be visited in the current episode
            episode_rewards = []    # the rewards of the episode

            env.init_episode()
            while not env.episode_finished:
                state = env.current_state_id()
                action = self.policy[state]
                reward = env.player_action(action)
                episode_rewards.append(reward)
                episode_states.append(state)

            self.update_values(episode_states, episode_rewards)

class TD0(object):

    def __init__(self):
        # The default policy to be evaluated is sticking only on 20 or 21
        K = 200
        self.policy = ['hit' for i in range(K)]
        self.policy[-40:] = ['stick' for i in range(40)]

        self.V = np.zeros(K)

    def train(self, env, total_episodes, a, discount_rate):
        """ Estimate the value of the states that the agent experiences. 
            1. Generate episode using the policy
            2. For each state visited, take action acording to policy.
            3. Observe the reward and the next state.
            4. Update the value of the state. """
        for _ in range(total_episodes):
            env.init_episode()
            state = env.current_state_id()
            while not env.episode_finished:
                action = self.policy[state]
                reward = env.player_action(action)
                if not env.episode_finished:
                    next_state = env.current_state_id()
                    dV = a * (reward + discount_rate * self.V[next_state] - self.V[state])
                    self.V[state] += dV
                    state = next_state
                else:
                    dV = a * (reward - self.V[state])
                    self.V[state] += dV

class TD_lamda(object):

    def __init__(self):
        # The default policy to be evaluated is sticking only on 20 or 21
        K = 200
        self.policy = ['hit' for i in range(K)]
        self.policy[-40:] = ['stick' for i in range(40)]

        self.V = np.zeros(K)
        # Replacing traces
        self.e = np.zeros(K)

    def train(self, env, total_episodes, lamda, a, discount_rate):
        """ Estimate the value of the states that the agent experiences. 
            1. Generate episode using the policy
            2. For each state visited, take action acording to policy.
            3. Observe the reward and the next state.
            4. Update the value of all states experienced in the episode. """
        for _ in range(total_episodes):
            self.e = np.zeros(self.e.size)
            env.init_episode()
            state = env.current_state_id()
            while not env.episode_finished:
                action = self.policy[state]
                reward = env.player_action(action)
                self.e[state] = 1
                if not env.episode_finished:
                    next_state = env.current_state_id()
                    dV = reward + discount_rate * self.V[next_state] - self.V[state]
                    state = next_state
                else:
                    dV = reward - self.V[state]
                self.V += a * dV * self.e
                self.e *= discount_rate * lamda


if __name__ == "__main__":
    from environment.Env import Env

    def state_id(d, s, a):
        return (s - 12) * 20 + (d - 1) * 2 + a

    def state_string(id):
        s = id // 20 + 12
        id %= 20
        d = id // 2 + 1
        a = id % 2

        if d == 1:
            d = 'A'
        else:
            d = str(d)
        
        s = str(s)
        a = str(a)

        return d + ' ' + s + ' ' + a

    env = Env()
    agent = TD0()
    
    V = np.zeros()

    