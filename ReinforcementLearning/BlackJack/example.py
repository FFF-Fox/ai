import argparse

from environment.Env import Env
from environment.Agents import First_Visit_MC

# Argument handling.
parser = argparse.ArgumentParser()
parser.add_argument('-p', '--print_values', help='print the state value V(s) of each state',
                    action='store_true')
parser.add_argument('-e', '--episodes', help='total number of episodes used in training', type=int)
parser.add_argument('-f', '--filename', help='save the state, value pairs in a file', type=str)

args = parser.parse_args()

env = Env()
agent = First_Visit_MC()
if args.episodes:
    total_episodes = args.episodes
else:
    total_episodes = 10**4
agent.train(env, total_episodes)

if args.print_values:
    print("state description: dealer's face-up card, player's points, player has a useable ace")
    for i in range(200):
        print('V('+ First_Visit_MC.States[i] + '): ', agent.V[i])

if args.filename:
    with open(args.filename, 'w') as f:
        for i in range(200):
            f.write(First_Visit_MC.States[i] + ',' + str(agent.V[i]) + '\n')