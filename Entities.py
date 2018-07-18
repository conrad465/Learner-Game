import pygame
import Components
import Systems as s
import vars as v
import Net
from numpy import ix_, zeros
from itertools import chain
v.init()
global player_locs
player_locs = {}


def initgrid(grid):
    global dgrid
    dgrid = grid


def getclosest(pos):
    fx,  fy = pos
    cord = (int(fy/(v.cell_size * v.block_scale))+v.padding,int(fx/(v.cell_size * v.block_scale))+v.padding)
    return cord


class MGroup(pygame.sprite.Group):
    def __init__(self):
        pygame.sprite.Group.__init__(self)
        self.gSystem = s.Gravity()

    def add_sprite(self,entity):
        if type(entity) != list:
            self.add(entity)
            self.gSystem.add(entity)
        else:
            for e in entity:
                self.add(e)
                self.gSystem.add(e)

    def update(self):
        self.gSystem.update()
        for e in self:
            e.update()
            if type(e) == Player or type(e) == Bullet:
                colliding = pygame.sprite.spritecollide(e, self, False)
                for c in colliding:
                    if c is not e:
                        e.collide(c)

group = MGroup()


class Entity(pygame.sprite.Sprite):
    def __init__(self, pid, x, y):
        global player_locs
        pygame.sprite.Sprite.__init__(self)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.row, self.col = getclosest((x,y))
        self.pid = pid
        self.components = list()

    def update(self):
        raise NotImplementedError


class Block(Entity):
    def __init__(self,pid,x,y):
        self.image = pygame.Surface([v.block_scale * v.cell_size, v.block_scale * v.cell_size])
        self.image.fill(pygame.Color(0,50,50,255))
        Entity.__init__(self, pid,x,y)

    def update(self):
        a=1


class Player(Entity):
    def __init__(self, pid, x, y, brain=0):
        self.image = pygame.Surface([v.player_scale * v.cell_size, v.player_scale * v.cell_size])
        self.image.fill(pygame.Color(255, 255, 255, 255))
        self.dir = 1
        Entity.__init__(self, pid, x, y)
        self.velocity = Components.Velocity(0, 0, pid)
        self.components.append(self.velocity)
        self.bullets = 10
        self.actions = [self.shoot, self.left, self.right, self.jump]
        self.locs = set()
        if brain != 0:
            self.net = brain
        else:
            self.net = Net.Net([60], 40, len(self.actions))

        player_locs.update({self.pid: (self.col, self.row)})

    def decide(self):
        global dgrid
        global player_locs
        row_range = list(range(self.row - v.vision, self.row + v.vision + 1))
        col_range = list(range(self.col - v.vision, self.col + v.vision + 1))

        pgrid = dgrid[ix_(col_range,row_range)]
        for key in player_locs:
            if key != self.pid:
                enemy_loc = player_locs[key]
        features = list(chain.from_iterable(pgrid)) + list(enemy_loc) + [self.row, self.col] + [self.dir]
        features = features + list(zeros(40 - len(features)))

        self.actions[self.net.decide(features)]()

    def collide(self,object):
        if isinstance(object, Bullet):
            if object.pid != self.pid:
                self.kill()
        else:
            rect = object.rect
            if rect.collidepoint(self.rect.midbottom):
                self.velocity.y = 0
                self.velocity.grav_on = False
                dif = self.rect.midbottom[1] - rect.midtop[1]
                self.rect.y -=(dif-1)
            if rect.collidepoint(self.rect.midtop):
                self.velocity.y = -1
            if rect.collidepoint(self.rect.midleft) and self.velocity.x <0:
                self.velocity.x = 0
                self.rect.x += v.player_speed
            if rect.collidepoint(self.rect.midright) and self.velocity.x >0:
                self.velocity.x = 0
                self.rect.x -= v.player_speed

    def update(self):
        global player_locs
        dgrid[self.col][self.row] = 0
        self.rect.y += self.velocity.y
        self.rect.x += self.velocity.x
        self.velocity.grav_on = True
        self.col, self.row = getclosest((self.rect.x,self.rect.y))
        self.locs.add((self.col,self.row))
        player_locs.update({self.pid:(self.col , self.row)})
        dgrid[self.col][self.row] = self.pid
        if self.bullets <= v.shoot_req: self.bullets+=1

    def save(self, gen):
        self.net.save_net(len(self.locs), gen)

    def jump(self):
        if self.velocity.grav_on == 0:
            self.velocity.y = v.jump_vel

    def right(self):
        self.velocity.x = v.player_speed
        self.dir = 1

    def left(self):
        self.velocity.x = -1 * v.player_speed
        self.dir = -1

    def shoot(self):
        if self.bullets > v.shoot_req:
            b = Bullet(self.pid, self.rect.center, self.dir)
            group.add(b)
            self.bullets -= v.shoot_req


class Bullet(Entity):
    def __init__(self, pid, loc, dir):
        self.colliding = False
        self.image = pygame.Surface([v.bullet_scale * v.cell_size, v.bullet_scale * v.cell_size])
        self.image.fill(pygame.Color(80, 50, 156, 255))
        self.velocity = Components.Velocity(dir*v.bullet_speed,0,pid)
        Entity.__init__(self, pid, loc[0], loc[1])

    def collide(self, object):
        if object.pid != self.pid:
            self.colliding = True

    def update(self):
        dgrid[self.col][self.row] = 0

        self.rect.x += self.velocity.x
        if self.colliding:
            self.kill()

        self.col, self.row = getclosest((self.rect.x,self.rect.y))
        dgrid[self.col][self.row] = self.pid


