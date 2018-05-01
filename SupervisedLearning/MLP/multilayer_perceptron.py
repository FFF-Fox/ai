import numpy as np

class MultilayerPerceptron:
    def __init__(self, layers, activations):
        self.params = {}

        # store the input layer dimensions
        self.n = layers[0]

        # store the number of neuron layers
        self.L = len(layers)-1

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


    def sigmoid(self, z):
        return 1 / (1 + np.exp(-z))

    def sigmoid_der(self, z):
        return sigmoid(z)*(1-sigmoid(z))

    def relu(self, z):
        return np.maximum([0,z])

    def relu_der(self, z):
        if z > 0:
            return 1
        else:
            return 0

if __name__ == '__main__':
    mlp = MultilayerPerceptron([2,3,3,1],['relu','relu','sigmoid'])

    print(mlp.params)
