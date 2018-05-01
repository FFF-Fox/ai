import numpy as np

class MultilayerPerceptron:
    def __init__(self, layers, activations):
        self.params = {}

        # store the input layer dimensions
        self.n = layers[0]

        # store the number of neuron layers
        self.L = len(layers)-1
        self.layers = layers[1:]

        # vectorize activations
        self.sigmoid = np.vectorize(self.sigmoid)
        self.sigmoid_der = np.vectorize(self.sigmoid_der)
        self.relu = np.vectorize(self.relu)
        self.relu_der = np.vectorize(self.relu_der)

        # construct network
        for i in range(self.L):
            self.params['W'+str(i)] = np.random.rand(layers[i],layers[i+1])
            self.params['b'+str(i)] = np.random.rand(layers[i+1],1)

            if activations[i] == 'sigmoid':
                self.params['act'+str(i)] = self.sigmoid
                self.params['der'+str(i)] = self.sigmoid_der
            elif activations[i] == 'relu':
                self.params['act'+str(i)] = self.relu
                self.params['der'+str(i)] = self.relu_der

    def train(self, X, y, method="stochastic", learning_rate=0.1, epochs=200, error_threshold=1e-3):
        if method == "stochastic":
            self.train_stochastic(X, y, r=learning_rate, epochs=epochs, err=error_threshold)

    def forward_pass(self, X):
        m = X.shape[0]
        for l in range(self.L):
            k = self.layers[l]

            # calculate linear unit output and store it for later...
            if l == 0:
                self.params['u'+str(l)] = (np.dot(self.params['W'+str(l)].T,X.T).reshape(k,m) + self.params['b'+str(l)]).reshape(k,m)
            else:
                self.params['u'+str(l)] = (np.dot(self.params['W'+str(l)].T,self.params['y'+str(l-1)]).reshape(k,m) + self.params['b'+str(l)]).reshape(k,m)

            self.params['y'+str(l)] = self.params['act'+str(l)]( self.params['u'+str(l)] ).reshape(k,m)

    def train_stochastic(self, X, y, r, epochs, err):
        (m,n) = X.shape

        for epoch in range(epochs):
            error = 0
            for i in range(m):
                self.forward_pass(X[i].reshape(1,n))

                e = y[i] - self.params['y'+str(self.L-1)]
                if epoch % 10 == 0:
                    error += e**2
                for l in range(self.L-1, -1, -1):
                    k = self.layers[l]
                    if l == self.L-1:
                        self.params['delta'+str(l)] = e * self.params['der'+str(l)]( self.params['u'+str(l)] )
                    else:
                        self.params['delta'+str(l)] = self.params['der'+str(l)]( self.params['u'+str(l)] ).reshape(k,1) * np.dot(self.params['W'+str(l+1)], self.params['delta'+str(l+1)]).reshape(k,1)

                    if l == 0:
                        self.params['dW'+str(l)] = np.dot(X[i].reshape(n,1),self.params['delta'+str(l)].T).reshape(self.params['W'+str(l)].shape)
                    else:
                        self.params['dW'+str(l)] = np.dot(self.params['y'+str(l-1)],self.params['delta'+str(l)].T).reshape(self.params['W'+str(l)].shape)


                # update the weights
                for l in range(self.L):
                    self.params['W'+str(l)] += r * self.params['dW'+str(l)]
                    self.params['b'+str(l)] += r * self.params['delta'+str(l)]

            if epoch % 10 == 0:
                print('epoch',epoch,'error',error/m)

    def predict(self, X):
        self.forward_pass(X)

        return self.params['y'+str(self.L-1)]

    def sigmoid(self, z):
        return 1 / (1 + np.exp(-z))

    def sigmoid_der(self, z):
        return self.sigmoid(z)*(1-self.sigmoid(z))

    def relu(self, z):
        if z > 0:
            return z
        else:
            return 0

    def relu_der(self, z):
        if z > 0:
            return 1
        else:
            return 0

if __name__ == '__main__':
    mlp = MultilayerPerceptron([2,3,3,1],['relu','relu','sigmoid'])

    print(mlp.params)

    print([i for i in range(4,-1,-2)])
