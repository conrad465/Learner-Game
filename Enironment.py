import pygame
import numpy
import Entities as e
import vars as v
import numpy as np
import pickle
import random
import os
import Net
from shutil import copy2, rmtree
global brain1
global brain2
global p1
global p2
global gen; gen = 419
global entity_index

global players; players = list()
global brains; brains = list()
window = pygame.display.set_mode((v.size,v.size))
elist = list()
game_grid = numpy.zeros((int(v.squares / v.block_scale), int(v.squares / v.block_scale)), dtype=int)


# saves the current generation members
def save_players():
    for player in players:
        player.save(gen)
    # p1.save(gen)
    # p2.save(gen)


# called to shuffle genes from parents
def shuffle_genes(parent_name1, parent_name2):
    with open("generations/" + str(gen - 1) + "/" + parent_name1, 'rb') as parent_file1:
        with open("generations/" + str(gen - 1) + "/" + parent_name2, 'rb') as parent_file2:
            parent1 = pickle.load(parent_file1)
            parent2 = pickle.load(parent_file2)
            if random.random() > .7:
                brain = parent1
            elif random.random() > .7:
                brain = parent2
            else:
                brain = parent1.mate(parent2)
                print("mating")

            if random.random() > .3:
                print("mutating")
                brain = brain.mutate()
            return brain


# TODO create function to load specific gneerations


# called to create and assess a generation from the genes of a previous one
def run_new_generation():
    parents = get_parents(gen, v.generation_carryover)
    # for i in range(v.next_gen):
    #     copy2("generations/" + str(gen - 1) + "/" + parents[i], "generations/" + str(gen) + "/")

    for i in range(v.gen_size):
        brains.clear()
        players.clear()
        for i in range(v.player_num):
            parent_index1 = random.randint(0, len(parents)-1)
            parent_index2 = random.randint(0, len(parents)-1)
            print("Picking " + parents[parent_index1])
            print("Picking " + parents[parent_index2])
            brains.append(shuffle_genes(parents[parent_index1], parents[parent_index2]))
        setup()
    run_new_species(3)
    rmtree("generations/" + str(gen - 1))


# called to create and assess the first generation of a learning species randomly
def run_new_species(num):

    for i in range(num):
        brains.clear()
        players.clear()
        for j in range(v.player_num):
            brains.append(Net.Net([20], v.inputs, 4))
        setup()


# managing function that handles generational evolution
def mother_nature():
    global gen
    while True:

        print(brains)
        if not os.path.exists("generations/" + str(gen)):
            os.makedirs("generations/" + str(gen))
        if gen != 1:
            run_new_generation()
        else:
            run_new_species(v.generation_carryover)
        gen += 1


# Performs necessary rendering and calls members of a generation to act
# for one round of evolution
def step():
    timer = 0
    while timer < v.env_timeout:
        timer += 1
        pygame.display.update()
        window.fill((0, 0, 0))
        e.group.update()
        events = pygame.event.get()

        for p in range(len(players)):
            if p!=-1:
                players[p].decide()
            else:
                players[p].decide(events)
        if check_win():
            timer += v.env_timeout

        for i in e.group:
            window.blit(i.image, i.rect)
        pygame.display.update()
    save_players()


# initialize members of a round of evolution
def add_sprites():
    #TODO Add algorithm to drop in open spaces in any map
    for i in range(v.player_num):
        [row, col] = get_space()
        # print(row)
        # print(col)
        players.append(e.Player(i+2, row, col, brains[i]))


    e.group.add_sprite(players)


# loads the map from a pre-made map file and initializes the game grid
def load_map():
    # TODO add gui to allow easy pickings
    # TODO use pickle with grid
    global entity_index
    global game_grid
    filename = "maps/gridfile2018-06-23 11:07:29.768659.txt"
    with open(filename, 'r') as level_file:
        for line in level_file:
            (col, row) = tuple(map(int, line.replace('\n', '').split(" ")))
            game_grid[row][col] = 1
            block = e.Block(entity_index, col * v.block_size, row * v.block_size)
            e.group.add(block)
            entity_index += 1

    game_grid = np.pad(game_grid, pad_width=v.padding, mode='constant', constant_values=-1)
    e.initgrid(game_grid)


# calls all helper functions to create an instance of a round of evolution
def setup():
    global entity_index
    e.group.empty()
    entity_index = 0
    load_map()
    add_sprites()
    pygame.init()
    step()


# returns the top num most fit individuals from the generation before curr_gen as file names
def get_parents(curr_gen, num):
    old_gen = curr_gen - 1
    path = os.path.dirname(os.path.abspath(__file__))
    parents = list()
    average_fitness = 0
    gen_dir = path + "/generations/" + str(old_gen)
    for file in os.listdir(gen_dir):
        # parses stored generation members with naming convention ["date time"_fit:## gen:#]
        index = file.index("fit:") + 4
        fitness = int(file[index:index + 2])
        average_fitness+=fitness
        parents.append((file, fitness))
    average_fitness/=1.0*len(os.listdir(gen_dir))
    with open("/Users/conradmitchell/PycharmProjects/Learner-Game/gen.csv", "a") as growth:
        growth.write(str(old_gen) + "," + str(average_fitness)+",\n")
    parents = sorted(parents, key=lambda x: x[1], reverse=True)
    parents = parents[0:num]
    print("Best from last generation were:\n " + parents[0][0] + "\n" + parents[1][0])
    return [item[0] for item in parents]


# checks if either player has killed each other
def check_win():
    a = players

    for player in players:
        if player.fit < 0:
            players[(-1*player.fit) -2].fit += 1
            player.fit = 0
            #return True
    return False


def get_space():
    while True:
        r = random.randint(0, len(game_grid) - 2)
        c = random.randint(0, len(game_grid) - 1)
        if game_grid[r][c] == 0 and game_grid[r+1][c] == 1:
            return [c*v.block_size, r*v.block_size]

mother_nature()