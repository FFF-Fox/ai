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

    
if __name__=="__main__":
    # fvmc = First_Visit_MC()
    S = First_Visit_MC()
    for i in range(200):
        print(First_Visit_MC.States[i], S.policy[i])

    print(S.V)