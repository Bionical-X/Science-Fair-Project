#imports
import numpy as np

#Nots on nueronic networks
# A nueran network:
# input layer
# hidden layers
# output layers

# At its smallest unit the nueron network is made up of nuerons
# Each nueron takes in inputs from previous layers
# each nueron comes with its own associated weight set
# and each nueron has its own unique bias
# the dot product of inputs and weights then gets added with bias for output
inputs = [1, 2, 3, 2.5]
weights = [0.2, 0.8, -0.5, 1.0]
bias = 2

output = inputs[0]*weights[0] + inputs[1]*weights[1]+ inputs[2]*weights[2] + inputs[3]*weights[3] + bias
print(output)

#So for example lets say we were finding the output layer given 4 inputs from a hidden layer of nuerons
inputs = [1,2,3,2.5]
weights1 = [0.2, 0.8, -0.5, 1.0]
weights2 = [0.5, -0.91, 0.26, -0.5]
weights3 = [-0.26, -0.27, 0.17, 0.87]
bias1 = 2
bias2 = 3
bias3 = 0.5

# In this output layer we acutally have 3 outputs nuerons
# note np.dot is just a function for dot product of 2 arrays
output1 = np.dot(inputs,weights1) + bias1
output2 = np.dot(inputs, weights2) + bias2
output3 = np.dot(inputs, weights3) + bias3
outputLayer = [output1, ou#It should be noted that the relationship for output and weights/inputs/bias is linear
# outputs = inputs*weights + bias
# weights are the slope
# bias is the translation
# this is base knowledge that will be useful in the adjusting of networks
# Activation point will be covered in another note pack







#Now to write the more standardized way to neuron layers
# Note: in numpy when using dot function if a matrix is fed in then it will do matrix multiplication
inputs = [1, 2, 3, 2.5] #shape/size of 4 x 1
weights = [[0.2, 0.8, -0.5, 1.0], #Shape/size of 3x4
           [0.5, -0.91, 0.26, -0.5],
           [-0.26, -0.27, 0.17, 0.87]]
biases = [2,3,0.5]

#if np.dot(inputs,weights) were used there would be an error
# a 4x1 can't be matrix multiplied with a 3x4 in that order
# while a 3x4 can be multiplied by a 4x1 to form a new 3x1 maxtrix
layer_outputs = np.dot(weights, inputs) + biases


