import pygame
import datetime
import vars as v
v.init()

window = pygame.display.set_mode((v.size,v.size))
window.fill((0,0,0))
group = pygame.sprite.Group()
grid_library = {}
cords = set()

def getclosest(pos):
    fx,  fy = pos
    cord = (int(fx / (v.cell_size * v.block_scale)), int(fy / (v.cell_size * v.block_scale)))
    return cord


def addblock(pos):
    coord = getclosest(pos)
    cords.add(coord)
    print(cords)
    x,y = coord
    a = pygame.draw.rect(window, (255, 255,255,), (coord[0] * v.cell_size * v.block_scale, coord[1] * v.cell_size * v.block_scale, v.cell_size * v.block_scale, v.block_scale * v.cell_size))


def drawlines():
  for row in range(int(v.size / v.cell_size)):
      pygame.draw.line(window, (255,255,255), (0, row * v.cell_size * v.block_scale), (v.block_scale * v.size, v.block_scale * row * v.cell_size))
      pygame.draw.line(window, (255, 255, 255), (v.block_scale * row * v.cell_size, 0), (v.block_scale * v.cell_size * row, v.size))


def savegrid():
 with open("gridfile"+str(datetime.datetime.now())+".txt" , 'w') as gfile:
     for row in cords:
        gfile.write(str(row[0])+' ' + str(row[1])+ '\n')


def step():
    t = False
    while True:
        pygame.time.delay(10)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                t = True
                while t:
                    addblock(pygame.mouse.get_pos())
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONUP:
                            t = False
                    pygame.display.update()
            if event.type == pygame.KEYDOWN:
                savegrid()
                exit()
            pygame.display.update()
pygame.init()
drawlines()
step()