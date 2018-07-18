import Layer as l
from datetime import datetime
import pickle as p
import numpy as np
import vars as v
v.init()


class Net:
    # Layers is a list of node numbers for each hidden layer in the grid
    # param @in_num is indicates the length of the input array
    # decisions is a list of potential actions
    def __init__(self, layers, in_num, decisions):
        self.fitness = 0
        self.layers = list()

        layers = iter(layers)
        start_layer = next(layers)
        self.layers.append(l.Layer(start_layer, in_num))
        prev_nodes = start_layer
        for node_num in layers:
            self.layers.append(l.Layer(node_num, prev_nodes))
            prev_nodes = node_num
        self.layers.append(l.Layer(decisions, prev_nodes))

    def save_net(self, travel, gen,kill = 0, alive = 0):
        self.assess_fitness(travel)
        f_name = v.gen_dir+str(gen)+"/" + str(datetime.now()) + '_fit:' + str(self.fitness) +"_gen:"  + '1'
        with open(f_name, 'wb') as net:
            p.dump(self, net)
        net.close()

    def assess_fitness(self, travel, kills = 0, alive = 0):
        self.fitness = int((((1.0) * travel) /  ((v.squares / v.block_scale)*(v.squares / v.block_scale)))* 90 + 10)
        print("Travelled " + str(travel)  + " squares")
        # TODO make fitness more robust

    def decide(self, input):
        layers = iter(self.layers)
        start_layer = next(layers)
        out = start_layer.calc(input)
        for layer in layers:
            out = layer.calc(out)
        return np.argmax(out)


    def mutate(self):
        for layer in self.layers:
            layer.mutate()
        return self

    def mate(self, partner):
        for i in range(len(self.layers)):
            self.layers[i].mate(partner.layers[i])
        return self