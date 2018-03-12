import numpy as np

class Perceptron:
    def __init__(self):
        self.w = None
        self.b = None

    def init_params(self, n):
        """ Initialization of the model parameters. Initializes weights and bias at random using a normal distribution. """
        self.w = np.random.normal(size=n)
        self.b = np.random.normal(size=1)



if __name__ == '__main__':
    p = Perceptron()

    p.init_params(3)
    assert(p.w.shape == (3,))
    assert(p.b.shape == (1,))
