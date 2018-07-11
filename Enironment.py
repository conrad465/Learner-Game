import pygame
import numpy
import Entities as e
import vars as v
import numpy as np
import pickle
import copy
import os
from shutil import copy2, rmtree
global brain1
global brain2
global p1
global p2
global gen; gen = 6
window = pygame.display.set_mode((v.size,v.size))
elist = list()
dgrid = numpy.zeros((int(v.squares/v.block_scale),int(v.squares/v.block_scale)), dtype=int)


def save_players():
    p1.save(gen)
    p2.save(gen)


def mother_nature():
    global brain1
    global brain2
    global gen
    child = "a"
    while True:
        if not os.path.exists("generations/" + str(gen)):
            os.makedirs("generations/" + str(gen))
        if gen != 1:
            [p1, p2] = get_parents(gen,7)
            with open("generations/" + str(gen-1) + "/" + p1,'rb') as f1:
                copy2("generations/" + str(gen-1) + "/" + p1, "generations/" + str(gen) + "/")
                p1 = pickle.load(f1)

            with open("generations/" + str(gen-1) + "/" + p2,'rb') as f2:
                copy2("generations/" + str(gen-1) + "/" + p2, "generations/" + str(gen) + "/")
                p2 = pickle.load(f2)

            child = p1.mate(p2)

            rmtree("generations/" + str(gen-1))
        for i in range(v.gen_size):
            if child != "a":
                brain1 = copy.deepcopy(child).mutate()
                brain2 = copy.deepcopy(child).mutate()
            setup()
        gen += 1



def step():
    timer = 0
    while timer < v.env_timeout:
        timer +=1
        pygame.time.delay(10)
        pygame.display.update()
        window.fill((0, 0, 0))
        e.group.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_UP:
            #         p2.jump()
            #     if event.key == pygame.K_RIGHT:
            #         p2.right()
            #     if event.key == pygame.K_LEFT:
            #         p2.left()
            #     if event.key == pygame.K_SPACE:
            #         p2.shoot()
        p2.decide()
        p1.decide()

        for i in e.group:
            window.blit(i.image, i.rect)
        pygame.display.update()
    save_players()

def addsprites():
    global p1
    global p2
    if gen != 1:
        p1 = e.Player(1,100, 200, brain1)
        p2 = e.Player(2,400,500,brain2)
    else:
        p1 = e.Player(1,100,200)
        p2 = e.Player(2,400,500)

    e.group.add_sprite([p1, p2])


def loadlevel():
    global pnum
    global dgrid
    filename = "maps/gridfile2018-06-23 11:07:29.768659.txt"
    with open(filename,'r') as level_file:
        for line in level_file:
            line.replace('\n','')
            loc = line.split(" ")
            col = int(loc[0])
            row = int(loc[1])
            dgrid[row][col] = 1
            b = e.Block(pnum, col * v.cell_size * v.block_scale, row * v.cell_size * v.block_scale)
            e.group.add(b)
            pnum +=1
    dgrid = np.pad(dgrid, pad_width=v.padding, mode='constant', constant_values=-1)
    e.initgrid(dgrid)


def setup():
    e.group.empty()
    global pnum
    pnum = 0
    loadlevel()
    addsprites()
    pygame.init()
    step()


def get_parents(gen, num):
    gen = gen - 1
    path = os.path.dirname(os.path.abspath(__file__))
    first = ["",0]
    second = ["",0]
    for file in os.listdir(path + "/generations/" + str(gen)):
        index = file.index("fit:")  + 4
        fitness =  int(file[index:index +2])
        if fitness > first[1]:
            second[1] = first[1]
            second[0] = first[0]
            first[1] = fitness
            first[0] = file
        elif fitness > second[1]:
            second[1] = fitness
            second[0] = file
    print("Best from last generation were:\n " + first[0] +"\n" + second[0] )
    return(first[0], second[0])



mother_nature()#setup()


