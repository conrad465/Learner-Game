import numpy as np
import Layer as l
from datetime import datetime
import pickle as p
import vars as v
v.init()


class Net:
    def __init__(self, layers, in_num, out):
        self.fitness = 0
        self.layers = list()
        self.out = out

        layers = iter(layers)
        start_layer = next(layers)
        self.layers.append(l.Layer(start_layer, in_num))
        prev_nodes = start_layer
        for node_num in layers:
            self.layers.append(l.Layer(node_num, prev_nodes))
            prev_nodes = node_num
        self.layers.append(l.Layer(len(out), prev_nodes))

    def save_net(self):
        f_name = v.gen_dir + str(datetime.now()) + '_fit:' + str(self.fitness) +"_gen:"  + '1'
        with open(f_name, 'wb') as net:
            p.dump(self, net)
        net.close()

    def assess_fitness(self, travel, kills = 0, alive = 0):
        self.fitness = ((1.0) * len(travel)) /  (v.squares / v.block_size)
        # TODO make fitness more robust

    def calculate(self, input):
        layers = iter(self.layers)
        start_layer = next(layers)
        out = start_layer.calc(input)
        for layer in layers:
            out = layer.calc(out)
        return out

    def mutate(self):
        for layer in self.layers:
            layer.mutate()