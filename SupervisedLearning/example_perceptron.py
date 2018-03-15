if __name__ == '__main__':
    from sklearn.datasets import make_moons
    from Perceptron.perceptron import *

    m = 300 # number of training examples
    X, y = make_moons(m, noise=0.1)
    n = X.shape[1]

    clf = Perceptron('step')
    clf.init_params(n)
    clf.train(X,y,epochs=200,rate=0.1, init=False)

    clf.plot_decision_boundary(X,y,"After 100 epochs of training")
