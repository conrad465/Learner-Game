import numpy as np
import random
import vars as v
v.init()
#players should assess their own fitness
class Layer:

    def __init__(self, nodes, past):
        self.weights = 2 * np.random.sample((nodes, past)) - 1
        self.bias = random.uniform(-1,1)
        self.vals = np.zeros((nodes, past))

    def calc(self, inputs):
        rows = len(self.weights)
        input_mat = np.matrix(np.tile(inputs, (rows,1)))
        res = np.sum(np.multiply(self.weights, input_mat), axis = 1) + self.bias
        self.vals = self.sigmoid(np.array(res).flatten())
        return self.vals

    def sigmoid(self, row):
        return 1 / (1 + np.exp(-1 * row))

    def mutate(self):
        for r in range(len(self.weights)):
            for c in range(len(self.weights[0])):
                rand = random.uniform(0,1)
                if rand < v.mutate_range:
                    rand = random.uniform(.9, 1.1)
                    self.weights[r][c] *= rand

        rand = random.uniform(0,1)
        offset = self.bias / 2 + 1
        if rand > .6:
            self.bias += offset
        elif rand <.4:
            self.bias -= offset

    def mate(self, new_gene):
        child = Layer(len(self.weights), len(self.weights[0]))
        for r in range(len(self.weights)):
            for c in range(len(self.weights[0])):
                rand = random.uniform(0,1)
                if rand > .5:
                    child.weights[r][c] = self.weights[r][c]
                else:
                    child.weights[r][c] = new_gene.weights[r][c]
        rand = random.uniform(0, 1)
        if rand > .5:
            child.bias = self.bias
        else:
            child.bias = new_gene.bias
        return child

    def clone(self):
        child = Layer(len(self.weights), len(self.weights[0]))
        for r in range(len(self.weights)):
            for c in range(len(self.weights[0])):
                child.weights[r][c] = self.weights[r][c]
        child.bias = self.bias
        return child

    def print(self):
        print(self.weights)