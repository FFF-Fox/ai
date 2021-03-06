import argparse

from environment.Env import Env
from Agents import TD0

# Argument handling.
parser = argparse.ArgumentParser()
parser.add_argument('-p', '--print_values', help='print the state value V(s) of each state',
                    action='store_true')
parser.add_argument('-e', '--episodes', help='total number of episodes used in training', type=int)
parser.add_argument('-a', '--alpha', help='the weight used in updating V(s)', type=float)
parser.add_argument('-d', '--discount_rate', help='the discount rate used in updating V(s)', type=float)
parser.add_argument('-f', '--filename', help='save the state, value pairs in a file', type=str)

args = parser.parse_args()

# Initialize the environment and the agent.
env = Env()
agent = TD0()

# Specify the total number of episodes.
if args.episodes:
    total_episodes = args.episodes
else:
    total_episodes = 10**4

# The agent estimates the state value function.
if args.alpha:
    alpha = args.alpha
else:
    alpha = 0.1

if args.discount_rate:
    discount_rate = args.discount_rate
else:
    discount_rate = 1.0

agent.train(env, total_episodes, alpha, discount_rate)

# Print V(s) to the console.
if args.print_values:
    print("state description: dealer's face-up card, player's points, player has a useable ace")
    for i in range(200):
        print('V('+ TD0.States[i] + '): ', agent.V[i])

# Write the results in a file. The results are written in the form
# of state, value pairs.
if args.filename:
    filename = args.filename
else:
    filename = 'results.dat'
with open(filename, 'w') as f:
    for i in range(200):
        f.write(TD0.States[i] + ',' + str(agent.V[i]) + '\n')