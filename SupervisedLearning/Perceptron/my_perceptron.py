import numpy as np
import matplotlib.pyplot as plt

class Perceptron:
    def __init__(self):
        self.w = None
        self.cache = {}

    def _initialization(self, d):
        """Initialization for the weights of the perceptron.
        Input:
            d: An integer denoting the dimensions of the input layer including the
            bias term.
        """
        w = np.zeros( (d,1) )
        assert ( w.shape == (d, 1) )
        return w

    def _linear_unit(self, w, X):
        """The linear unit of the perceptron.
        Inputs:
            w: The weights of the perceptron.
            X: The input.
        Output:
            u: An (m,1) vector containing the dot product of each <w,Xi>.
        """
        u = np.dot(w.T, X)

        assert ( u.shape == (1, X.shape[1]) )
        return u

    def _activation(self, u):
        """Apply the activation function to the output of the linear unit.
        Input:
            u: The output vector of the linear unit.
        Output:
            a: The activation vector with the same size of the linear unit.
        """
        a = np.sign(u)

        assert ( a.shape == u.shape )
        return a

    def _MSE(self, y, y_hat):
        """Evaluates the Mean Square Error."""
        n = y.shape[1]
        error = (1/n) * np.sum( np.square(y - y_hat) )

        assert (error.shape == ())
        return error

    def _compute_cost(self, y, y_hat):
        """Compute the result of the cost function.
        Input:
            y: The real values of the labels.
            y_hat: The output labels of the perceptron in a iteration.
        Outputs:
            J: The cost evaluated from the cost function.
        """
        J = self._MSE(y, y_hat)

        return J

    def _weight_update(self, X, y, u, r):
        """Update the weights of the perceptron.
        Inputs:
            u: The output of the linear unit.
            r: Learning rate.
        """
        dw = np.sum( (y - u) * X , axis=1).reshape(X.shape[0], 1)
        w = self.w + r * dw

        assert ( self.w.shape == w.shape )
        return w

    def _preprocess_X(self, X):
        """Preprocessing of X:
            Resize (m x d) => (d+1, m), where d is the # of dimensions and
            m is the # of the training examples. A column of ones is added
            to help with the computation of biases.
        """
        X_proc = np.array( X )

        m = X_proc.shape[0]
        d = X_proc.shape[1]

        X_proc = X_proc.T.reshape( (d, m) )
        X_proc = np.append(X_proc, np.ones((1, m)), axis=0)

        assert ( X_proc.shape == (d+1,m) )
        return X_proc

    def _preprocess_input(self, X_train, y_train):
        """Method used to preprocess the input given. X is expected to be (m x d).
        y is a one dimensional array.
        Inputs:
            X_train: The training data.
            y_train: The training labels.
        """
        X = self._preprocess_X( X_train )
        y = np.array( y_train )
        y = y.reshape( (1, X.shape[1]) )

        assert ( y.shape == (1,X.shape[1]) )
        return X, y

    def train(self, X_train, y_train, learning_rate=0.001, n_epochs=100, error_threshold=0, verbose=True):
        self.cache["cost"] = []
        self.cache["learning_rate"] = learning_rate
        self.cache["n_epochs"] = n_epochs

        X, y = self._preprocess_input(X_train, y_train)

        self.w = self._initialization( X.shape[0] )
        for i in range(n_epochs):
            u = self._linear_unit(self.w, X)
            y_hat = self._activation(u)
            J = self._compute_cost(y, y_hat)

            if verbose and (i % 10 == 0):
                padding = (len(str(n_epochs)) - len(str(i))) * " "
                print ( "Iteration %s%d, MSE = %.3f" % (padding, i, J) )

            if J < error_threshold:
                break
            else:
                self.w = self._weight_update(X, y, u, learning_rate)
                self.cache["cost"].append(J)

        if verbose: print ( "Finished learning. MSE = %.3f" % J )

    def predict(self, X):
        """Predict the labels for each example in X.
        Input:
            X: The examples for which the algorithm will predict the labels.
        Output:
            y_pred: An array containing the predicted labels.
        """
        X_proc = self._preprocess_X( X )
        u = self._linear_unit(self.w, X_proc)
        y_pred = self._activation(u).T

        return y_pred

    def plot_error(self):
        """Plot the MSE over the number of epochs."""
        plt.plot(range(len(self.cache["cost"])), self.cache["cost"], "firebrick")

        plot_title = "Learning Rate: %s, Epochs: %d" % (self.cache["learning_rate"], self.cache["n_epochs"])
        plt.title(plot_title, fontsize=16)
        plt.xlabel('Epochs', fontsize=14)
        plt.ylabel('MSE', fontsize=14)
        plt.show()

    def plot_classification_results(self, X_in, y_in, msg, h=0.01):
        """Plot the decision boundary
        Originally found on stack overflow ( https://stackoverflow.com/questions/19054923/plot-decision-boundary-matplotlib ). Made some changes.
        """
        X, y = self._preprocess_input(X_in, y_in)

        if X.shape[0] > 3:
            print ( "Cannot plot more than 2 dimensions. Please use only for binary classification on 2 dimensional data." )
            return

        x_min, x_max = X[0, :].min() - 1, X[0, :].max() + 1
        y_min, y_max = X[1, :].min() - 1, X[1, :].max() + 1
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
        plt.scatter(X[0,:], X[1,:], marker='.', c=y[0,:],  cmap="coolwarm")

        plt.title(msg, fontsize=16)
        plt.xlabel("x1", fontsize=14)
        plt.ylabel("x2", fontsize=14)
        plt.show()


def main():
    import math
    import numpy as np
    import matplotlib.pyplot as plt
    from sklearn.datasets import make_moons
    from sklearn.metrics import accuracy_score

    np.random.seed( 420 )

    m = 200 # number of training examples
    X_moon, Y_moon = make_moons(m, noise=0.1)
    def process_Y_moon(x):
        if x == 0:
            return -1
        else:
            return x
    Y_moon = list(map(process_Y_moon, Y_moon))
    c = 1.5    # a constant used for the mean of the normal distributions.
    k = math.floor(m/2)
    X_normal = np.append(np.random.normal(loc=[c,c], size=(k,2)),
                         np.random.normal(loc=[-c,-c], size=(k,2)),
                         axis=0)
    Y_normal = np.append([-1 for i in range(k)], [1 for i in range(k)])


    # --------- Choose dataset and size of training data --------- #
    train_percent = 0.66
    data_X, data_y = np.array( X_moon ), np.array( Y_moon )

    # --------- Shuffling the input --------- #
    perm = np.arange( data_X.shape[0] )
    np.random.shuffle(perm)
    data_X = data_X[perm,:]
    data_y = data_y[perm]

    # --------- Train/Test split --------- #
    tr_ex = math.ceil( train_percent * m )
    X_train = data_X[:tr_ex,:]
    y_train = data_y[:tr_ex]

    X_test = data_X[tr_ex:,:]
    y_test = data_y[tr_ex:]

    # ---------- Initialize the model ----------#

    model = Perceptron()

    # ---------- Train the model ----------#

    model.train(X_train, y_train, learning_rate=0.001, n_epochs=200, error_threshold=0.300)

    # ---------- Plot the error over the iterations ----------#

    model.plot_error()

    # ---------- Plot Classification Results ----------#

    # Train
    model.plot_classification_results(X_train, y_train, msg="Train Dataset")
    y_pred = model.predict(X_train)
    print ( "Train accuracy:", accuracy_score(y_train, y_pred) )

    # Test
    y_pred = model.predict(X_test)
    model.plot_classification_results(X_test, y_test, msg="Test Dataset")
    print ( "Test accuracy:", accuracy_score(y_test, y_pred) )

        
if __name__ == '__main__':
    main()