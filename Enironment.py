import pygame
import numpy
import Entities as e
import vars as v
v.init()


window = pygame.display.set_mode((v.size,v.size))
elist = list()
dgrid = numpy.zeros((int(v.squares/v.block_scale),int(v.squares/v.block_scale)), dtype=int)


def step():
    run = True
    while run:
        pygame.time.delay(10)

        pygame.display.update()
        window.fill((0, 0, 0))
        e.group.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    p2.jump()
                if event.key == pygame.K_RIGHT:
                    p2.right()
                if event.key == pygame.K_LEFT:
                    p2.left()
                if event.key == pygame.K_SPACE:
                    p2.shoot()

        for i in e.group:
            window.blit(i.image, i.rect)
        print(dgrid)
        print('\n')
        pygame.display.update()


def addsprites():
    global p1
    global p2
    global pnum
    p1 = e.Player(2, 300, 50 )
    pnum +=1
    p2 = e.Player(3,50,300)
    pnum+=1
    e.group.add_sprite([p1,p2])


def loadlevel():
    global pnum
    filename = "gridfile2018-06-23 11:07:29.768659.txt"
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
    e.initgrid(dgrid)


def setup():
    global pnum
    pnum = 0
    loadlevel()
    addsprites()
    pygame.init()
    step()





setup()


