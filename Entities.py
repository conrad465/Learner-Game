import pygame
import Components
import Systems as s
import vars as v
v.init()

def initgrid(grid):
    global dgrid
    dgrid = grid
    print(dgrid)


def getclosest(pos):
    fx,  fy = pos
    cord = (int(fx/(v.cell_size * v.block_scale)),int(fy/(v.cell_size * v.block_scale)))
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
    def __init__(self,pid,x,y):
        self.image = pygame.Surface([v.player_scale * v.cell_size, v.player_scale * v.cell_size])
        self.image.fill(pygame.Color(255,255,255,255))
        self.dir = 1
        Entity.__init__(self, pid,x,y)
        self.velocity = Components.Velocity(0, 0, pid)
        self.components.append(self.velocity)
        self.bullets = 10

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
                self.velocity.y = 0
            if rect.collidepoint(self.rect.midleft) and self.velocity.x <0:
                self.velocity.x = 0
                self.rect.x += v.player_speed
            if rect.collidepoint(self.rect.midright) and self.velocity.x >0:
                self.velocity.x = 0
                self.rect.x -= v.player_speed

    def update(self):
        dgrid[self.row][self.col] = 0
        self.rect.y += self.velocity.y
        self.rect.x += self.velocity.x
        self.velocity.grav_on =True
        self.col, self.row = getclosest((self.rect.x,self.rect.y))
        dgrid[self.col][self.row] = self.pid
        if self.bullets <= v.shoot_req: self.bullets+=1

    def jump(self):
        if self.velocity.y ==0 :
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
        self.rect.x += self.velocity.x
        if self.colliding:
            self.kill()




