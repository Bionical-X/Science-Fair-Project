import numpy as np

# This is considered a batch of inputs
# if we run multiple samples at the same time we are more likely
# to produce acurate results 
inputs = [[1,2,3,2.5], #3s4
          [2.0,5.0,-1.0,2.0],
          [-1.5,2.7,3.3,-0.8]]

weights = [[0.2,0.8,-0.5,1.0], # 3x4
           [0.5,-0.91,0.26,-0.5],
           [-0.26,-0.27,0.17,0.87]]
biases = [2,3,0.5]


#Since both matrices are the same weight
#We need to transpose one changing its shape to 4x3
#luckily numpy has a transpose function
outputs = np.dot(inputs, np.array(weights).T)+biases
print(outputs)

#Now lets say we add an extra layer

weights2 = [[0.1,-0.14,0.5], # 3x4
           [-0.5,0.12,-0.33],
           [-0.44,0.73,-0.13]]
biases2 = [-1,2,-0.5]

#outputs become layer1_outputs
layer1_outputs = outputs

layer2_outputs = np.dot(layer1_outputs, np.array(weights2).T) + biases2
print(layer2_outputs)

#But as expected this method would become non-sustanible
#Since if we want to add more layers or change layers
# we would need to change or add more lines of code
# Thus to standardize this we will use object oritented coding
# Just for the purposes of this demo we will use a random set seed to demonstrate weights


class Layer_Dense:
    def __init__(self, n_inputs, n_neurons):
        self.weights = 0.10*np.random.randn(n_inputs, n_neurons) # the 0.10 was added to keep range of values in the interval (-1,1)
        self.biases = np.zeros((1, n_neurons)) #the first input in np.zeros determines the shape of the matrix thus we passed in a touple

        
    def forward(self, inputs):
        self.output = np.dot(inputs, self.weights) + self.biases

layer1 = Layer_Dense(4,5)
layer2 = Layer_Dense(5,2)

layer1.forward(inputs)
#print(layer1.output)
layer2.forward(layer1.output)
#print(layer2.output)





    
