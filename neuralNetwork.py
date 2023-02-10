import numpy as np


class neuralNetwork:
    #This function is for the creation of hidden layers and outputlayer neurons
    def __init__(self, neurons_list):
        self.layers = []
        for i in neurons_list:
            self.layers.append(Layer_Dense(i))
        
    #This is the function where you pass in inputs
    def  forward(self, inputs):
        #initilizing the activation functions
        activation = Activation_ReLU()
        softMax = Activation_softmax()

        #Go through hidden layers passing in data
        for i in range(len(self.layers)-1):
            self.layers[1].forward(inputs)
            inputs = activation.adjust(self.layers[i].output)

        #adjusting final layer
        self.layers[len(self.layers)].forward(inputs)
        self.outputs = activation(self.layers[len(self.layers).output])

    def getOutput(self):
        return self.outputs


class Layer_Dense: #neuron layer
    def __init__(self, n_neurons):
        self.weights = 0.1 * np.random.randn(n_neurons)
        self.biases = np.zeros((1, n_neurons))
    def forward(self, inputs):
        self.output = np.dot(self.weights, inputs) + self.biases


#This is for the hidden layers
class Activation_ReLU:
    def adjust(self, inputs):
        return np.maximum(0, inputs) #output
    
    
#This is a softmax activation function
#This is mainly for the final output neurons
class Activation_Softmax:
    def adjust(self, inputs):

        exp_values = np.exp(inputs - np.max(inputs,axis=1,keepdims=True))
        probabilities = exp_values / np.sum(exp_values, axis=1, keepdims=True)
        
        return probabilities #output

network = neuralNetwork([3,2])
inputs = [0.1,0.2,0.3]

network.forward(inputs)
print(network.getOutput())
