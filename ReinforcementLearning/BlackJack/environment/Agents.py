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
        self.policy = ['hit' for i in range(self.K)]
        self.policy[-40:] = ['stick' for i in range(40)]

        self.V = np.zeros(self.K)
        self.returns = [[] for s in range(self.K)]

    def train(self, env, total_episodes):
        """ Estimate the value of the states that the agent experiences. 
            1. Generate episode using the policy
            2. For each state appeared in the episode keep the return following the first
               occurence and average the returns of each state visited in this episode. """
        for episode in range(total_episodes):
            episode_states = []    # the states that will be visited in the current episode
            episode_rewards = []    # the rewards of the episode

            env.init_episode()
            while not env.episode_finished:
                s = env.get_state()
                # print(self.States.index(s))
                state = self.States.index(s)
                action = self.policy[state]
                reward = env.player_action(action)
                episode_rewards.append(reward)
                episode_states.append(state)

            for s in set(episode_states):
                k = episode_states.index(s)    # find the first visit of state s
                m = len(episode_states) - k
                R = sum(episode_rewards[-m:])
                self.returns[s].append(R)
                self.V[s] = np.mean(self.returns[s])
                


if __name__=="__main__":
    from Env import Env

    env = Env()
    agent = First_Visit_MC()

    agent.train(env, 5 * 10**5)
    for i in range(200):
        print('state: ',First_Visit_MC.States[i])
        print('V(s): ', agent.V[i])