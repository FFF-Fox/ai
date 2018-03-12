import numpy as np

class Perceptron:
    def __init__(self):
        self.w = None
        self.b = None
        self.step = np.vectorize(self.step)

    def init_params(self, n):
        """ Initialization of the model parameters. Initializes weights and bias at random using a normal distribution. """
        self.w = np.random.normal(size=n)
        self.b = np.random.normal(size=1)

    def linear_unit(self, X):
        """ Computes the dot product of X and the weights of the perceptron. """
        return np.dot(X,self.w) + self.b

    def step(self, z):
        if z < 0.5:
            return 0.0
        else:
            return 1.0

    def forward_prop(self, X):
        """ Forward propagation step. Given an input X computes the perceptron's output. """
        z = self.linear_unit(X)
        y_hat = self.step(z)
        return y_hat

    def back_prop(self, y_hat, y, X):
        """ Backward propagation step (batch). Update the weights of the perceptron based on the error of the model's output. """
        d = y - y_hat
        dw = np.dot(d.T,X)
        self.w = self.w + dw
        self.b = self.b + np.sum(d)

    def mse(self, y_hat, y):
        """ Computes the mean square error. """
        mse = ((y_hat - y) ** 2).mean()
        return mse

if __name__ == '__main__':
    from sklearn.datasets import make_moons
    np.random.seed(10)
    m = 3 # number of training examples
    n = 2
    X, y = make_moons(m, noise=0.1)

    p = Perceptron()

    p.init_params(n)
    assert(p.w.shape == (n,))
    assert(p.b.shape == (1,))

    assert(np.abs(p.linear_unit(X[0])[0] - -0.398003670538) < 1.0e-12)
    assert((p.linear_unit(X) == np.dot(X,p.w) + p.b).all())

    y_hat = p.forward_prop(X)
    assert((y_hat == [0, 0, 1]).all())

    for i in range(10):
        y_hat = p.forward_prop(X)
        p.back_prop(y_hat, y, X)
        print(p.w,p.b)
        print(p.mse(y_hat,y))

    # y_hat = p.forward_prop(X[0])
    # print(p.w,p.b)
    # p.back_prop(y_hat, y[0], X[0])
    # print(p.w,p.b)
