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

    def save_net(self, travel, gen, kills):
        placeholder = ""
        self.assess_fitness(travel, kills)
        if self.fitness<10:
            placeholder = "0"
        f_name = v.gen_dir+str(gen)+"/" + str(datetime.now()) + '_fit:' +placeholder + str(self.fitness)+"_gen:"  + str(gen)
        if self.fitness > 0:
            with open(f_name, 'wb') as net:
                p.dump(self, net)
            net.close()

    # fitness based on how far the object travelled and if the object killed anything
    # TODO sprites should pass their own fitness function to abstract the net
    def assess_fitness(self, travel, kills):
        self.fitness = ((.8) * travel) / ((v.squares / v.block_scale)*(v.squares / v.block_scale) - 30)
        if kills >-1:
            self.fitness += .2 * kills
        self.fitness = int(self.fitness * 80 + 20)
        print("Travelled " + str(travel)  + " squares")
        print("travel fitness: "+ str(((.8) * travel) / ((v.squares / v.block_scale)*(v.squares / v.block_scale))*80 +20 ))

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
            self.layers[i] = self.layers[i].mate(partner.layers[i])
        return self


    def print(self):
        for l in self.layers:
            l.print()

        print("")