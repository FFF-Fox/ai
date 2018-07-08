import numpy as np

class First_Visit_MC(object):
    States = []
    for s in range(12, 22):
        for d in range(1, 11):
            for a in [False, True]:
                state = ''
                if d == 1:
                    state += 'A'
                else:
                    state += str(d)
                
                state += ' ' + str(s) + ' ' + str(a)
                States.append(state)
    K = len(States)

    def __init__(self):
        # The default policy to be evaluated is sticking only on 20 or 21
        self.policy = ['hit' for i in range(self.K)]
        self.policy[-40:] = ['stick' for i in range(40)]

        self.V = np.zeros(self.K)
        self.Returns = [[] for s in range(self.K)]

    def update_values(self, episode_states, episode_rewards):
        """ Update the V(s) values after an episode finishes """
        for s in set(episode_states):
                i = episode_states.index(s)    # index of the first visit of state s
                m = len(episode_states) - i
                R = sum(episode_rewards[-m:])  # total return starting from first visit of s
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
                s = env.get_state()
                state = self.States.index(s)
                action = self.policy[state]
                reward = env.player_action(action)
                episode_rewards.append(reward)
                episode_states.append(state)

            self.update_values(episode_states, episode_rewards)


if __name__ == "__main__":
    from environment.Env import Env

    env = Env()
    agent = First_Visit_MC()

    agent.train(env, 5 * 10**5)
    for i in range(200):
        print('state: ',First_Visit_MC.States[i])
        print('V(s): ', agent.V[i])