import numpy as np
import math
import random
import collections

class neuralNetwork:
    def __init__(self, layerOneSize, layerTwoSize, layerThreeSize):
        self.weights1 = np.random.uniform(size=(layerTwoSize,layerOneSize),low=-1,high=1)
        self.biases2 = [0]*layerTwoSize
        self.activations2 = [0]*layerTwoSize
        self.weights2 = np.random.uniform(size=(layerThreeSize,layerTwoSize),low=-1,high=1)
        self.biases3 = [0]*layerThreeSize
        self.activations3 = [0]*layerThreeSize
        self.weightsAdjust1 = np.zeros((layerTwoSize,layerOneSize))
        self.biasesAdjust2 = np.zeros(layerTwoSize)
        self.weightsAdjust2 = np.zeros((layerThreeSize,layerTwoSize))
        self.biasesAdjust3 = np.zeros(layerThreeSize)
        self.activationsAdjust2 = [0]*layerTwoSize
        self.epsilon = 1.0
        #print(self.biases2)
        self.count = 0
        self.memory = collections.deque(maxlen = 2500)

    def sigmoid(self,x):
        for r in range(len(x)):
            x[r] =  1/(1+math.exp(-x[r]))
        return x

    def choose(self, state):
        if random.uniform(0,1)<self.epsilon:
            choice = random.randint(0,len(self.activations3)-1)
            self.epsilon -= 0.001
        else:
            self.activations2 = np.copy(self.ReLU((np.matmul(self.weights1,state)+self.biases2)))
            #print(self.activations2)
            self.activations3 = np.copy(self.sigmoid((np.matmul(self.weights2,self.activations2)+self.biases3)))
            print(self.activations3)
            maximum = 0
            choice = 0
            for n in range(len(self.activations3)):
                if self.activations3[n]>maximum:
                    choice = n
                    maximum = self.activations3[n]
        #print(choice)
        #print(self.biases3)
        self.count += 1
        return choice

    def sig(self,x):
        return math.exp(-x)/math.pow(1+math.exp(-x),2)
        
    def siga(self,x):
        for r in range(len(x)):
            x[r] = math.exp(-x[r])/math.pow(1+math.exp(-x[r]),2)
        return x

    def ReLU(self,x):
        for r in range(len(x)):
            if x[r]<=0:
                x[r]=0
        return x

    def ReLUd(self,x):
        if x<=0:
            return 0
        else:
            return 1

    def ReLUda(self,x):
        for r in range(len(x)):
            if x[r]<=0:
                x[r] = 0
            else:
                x[r] = 1
        return x

    def remember(self, state, choice, reward):
        self.memory.append((state, choice, reward))

    def adjust(self):
        if len(self.memory) >= 1000:
            minibatch = random.sample(self.memory, 1000)
        else:
            minibatch = self.memory
        for (state, choice, reward) in minibatch:
            
            self.biasesAdjust3[choice] += reward*2*(1-self.activations3[choice])*self.sig(
                np.dot(self.weights2[choice],self.activations2)+self.biases3[choice])
            
            self.weightsAdjust2[choice] += np.dot(reward*2.0*(1-self.activations3[choice])*self.sig(
                np.dot(self.weights2[choice],self.activations2)+self.biases3[choice]),self.activations2)
            
            self.biasesAdjust2 += np.multiply(self.ReLUda(np.matmul(self.weights1,state)+self.biases2)*
                np.dot(self.weights2[choice],reward*2*(1-self.activations3[choice])),(
                self.ReLUd(np.dot(self.weights2[choice],self.activations2)+self.biases3[choice])))

            for i in range(len(self.weights1)):
                self.weightsAdjust1[i] += reward*2*(1-self.activations3[choice])*(
                        self.ReLUd(np.dot(self.weights2[choice],self.activations2)+self.biases3[choice]))*(
                        self.weights2[choice][i]*self.ReLUd(np.dot(self.weights1[i],state)+self.biases2[i])*state)
            
    
            #print(self.weightsAdjust2)
        self.optimize()
                
    def optimize(self):
        self.weights1 += 1/self.count * self.weightsAdjust1
        self.weights2 += 1/self.count * self.weightsAdjust2
        self.biases2 += 1/self.count * self.biasesAdjust2
        #self.biases3 += 1/self.count * self.biasesAdjust3
        #print(self.epsilon)
        self.weightsAdjust1.fill(0)
        self.weightsAdjust2.fill(0)
        self.biasesAdjust2.fill(0)
        self.biasesAdjust3.fill(0)
        self.count = 0
        
