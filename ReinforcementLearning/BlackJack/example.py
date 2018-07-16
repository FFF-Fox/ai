from environment.Env import Env
from environment.Agents import First_Visit_MC

env = Env()
agent = First_Visit_MC()

total_episodes = 10**4
filename = 'fvmc.dat'

agent.train(env, total_episodes)

print("state description: dealer's face-up card, player's points, player has a useable ace")
for i in range(200):
    print('V('+ First_Visit_MC.States[i] + '): ', agent.V[i])

with open(filename, 'w') as f:
    for i in range(200):
        f.write(First_Visit_MC.States[i] + ' ' + str(agent.V[i]) + '\n')