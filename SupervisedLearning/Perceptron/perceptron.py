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

    def back_prop(self, y_hat, y, X, rate):
        """ Backward propagation step (batch). Update the weights of the perceptron based on the error of the model's output. """
        d = y - y_hat
        dw = np.dot(d.T,X)
        self.w = self.w + rate * dw
        self.b = self.b + rate * np.sum(d)

    def mse(self, y_hat, y):
        """ Computes the mean square error. """
        mse = np.square(y_hat - y).mean()
        return mse

    def train(self, X, y, epochs, threshold=0, rate=1):
        """ Given the training dataset and the number of epochs, the perceptron is trained to minimize its error. """
        (m,n) = X.shape
        self.init_params(n)

        for epoch in range(epochs):
            y_hat = self.forward_prop(X)
            self.back_prop(y_hat, y, X, rate)
            mse = self.mse(y_hat,y)

            if epoch % 5 == 0:
                print("MSE:",mse)

            if mse < threshold:
                break

    def predict(self, X):
        y_hat = self.forward_prop(X)
        return y_hat

    def plot_decision_boundary(self, X, y, title, h=0.01):
        """Plot the decision boundary
        Originally found on stack overflow ( https://stackoverflow.com/questions/19054923/plot-decision-boundary-matplotlib ). Made some changes.
        """

        if X.shape[1] > 3:
            print ( "Cannot plot more than 2 dimensions. Please use only for binary classification on 2 dimensional data." )
            return

        x_min, x_max = X[:,0].min() - 1, X[:,0].max() + 1
        y_min, y_max = X[:,1].min() - 1, X[:,1].max() + 1
        xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                             np.arange(y_min, y_max, h))

        Zx = np.c_[xx.ravel(), yy.ravel()]

        # here "model" is the model's prediction (classification) function
        Z = self.predict( Zx )

        # Put the result into a color plot
        Z = Z.reshape(xx.shape)
        plt.contourf(xx, yy, Z, cmap="coolwarm")
        # plt.axis('off')

        # Plot the training points
        plt.scatter(X[:,0], X[:,1], marker='.', c=y,  cmap="coolwarm")

        plt.title(title, fontsize=16)
        plt.xlabel("x1", fontsize=14)
        plt.ylabel("x2", fontsize=14)
        plt.show()


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

    p.train(X,y,30)



    m = 30 # number of training examples
    X, y = make_moons(m, noise=0.1)
    p.train(X,y,100,rate=0.1)
    # print(p.predict([1,1]))
    # print(p.predict([1,0]))

    import matplotlib.pyplot as plt
    p.plot_decision_boundary(X,y,"After 100 epochs of training")

    # y_hat = p.forward_prop(X[0])
    # print(p.w,p.b)
    # p.back_prop(y_hat, y[0], X[0])
    # print(p.w,p.b)
