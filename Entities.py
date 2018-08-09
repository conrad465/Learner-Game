import pygame
import Components
import Systems as s
import vars as v
import Net
import math
v.init()
global player_locs
global bullet_locs
player_locs = {}
bullet_locs ={}


def initgrid(grid):
    global dgrid
    global bullet_locs
    bullet_locs.clear()
    dgrid = grid

# returns the closest grid block to the actual x and y position
# allows environment to be mapped to a grid
def getclosest(pos):
    fx,  fy = pos
    fx -= (.50*v.player_size)
    fy -= (.50*v.player_size)
    cords = (int(round(((1.0)*fy)/v.block_size))+v.padding, int(round(((1.0)*fx)/v.block_size))+v.padding)
    return cords

# container for all entities in the game
# manages updating and collisions
class MGroup(pygame.sprite.Group):
    def __init__(self):
        pygame.sprite.Group.__init__(self)
        self.gSystem = s.Gravity()

    def add_sprite(self, entity):
        if type(entity) != list:
            self.add(entity)
            self.gSystem.add(entity)
        else:
            for e in entity:
                self.add(e)
                self.gSystem.add(e)
    # checks collisions for all entities in group
    def update(self):
        self.gSystem.update()
        for entity in self:
            entity.update()
            if type(entity) == Player or type(entity) == Bullet:
                colliding = pygame.sprite.spritecollide(entity, self, False)
                for c in colliding:
                    if c is not entity:
                        entity.collide(c)

group = MGroup()

# Base class for block, sprite, bullet
class Entity(pygame.sprite.Sprite):
    def __init__(self, pid, x, y):
        global player_locs
        pygame.sprite.Sprite.__init__(self)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.row, self.col = getclosest((x, y))
        self.pid = pid
        self.components = list()

    def update(self):
        raise NotImplementedError


class Block(Entity):
    def __init__(self,pid,x,y):
        self.image = pygame.Surface([v.block_scale * v.cell_size, v.block_scale * v.cell_size])
        self.image.fill(pygame.Color(0,50,50,255))
        Entity.__init__(self, pid, x, y)

    # not implemented yet
    def update(self):
        a=1


class Player(Entity):
    def __init__(self, pid, x, y, brain=0):
        self.image = pygame.Surface([v.player_scale * v.cell_size, v.player_scale * v.cell_size])
        self.image.fill(pygame.Color(255, 255, 255, 255))
        self.direction = 1
        Entity.__init__(self, pid, x, y)
        self.velocity = Components.Velocity(0, 0, pid)
        self.components.append(self.velocity)
        self.bullet_timer = 10
        self.actions = [self.shoot, self.left, self.right, self.jump]
        self.locs = set()
        self.fit = 0
        self.slave = False

        if brain != 0:
            self.net = brain
        else:
            self.net = Net.Net([20], v.inputs, len(self.actions))

        player_locs.update({self.pid: (self.row, self.col)})

    # Primary meat of decision -- creates a list of inputs for the neural net
    # looks at blocks around it, bullets nearby, location of enemy
    def decide(self, events = ""):
        if events != "":
            self.obey(events)
            self.slave = True
            return
        global dgrid
        global player_locs
        direction = [self.direction]
        surroundings = get_distances(self.row, self.col)
        enemy_loc = relative_enemy_loc(self.row, self.col, self.pid)
        enemy_in_row = 0
        bullet_in_row = 0
        if enemy_loc[0] == 0:
            if enemy_loc[1] > 0:
                enemy_in_row = 1
            else:
                enemy_in_row =- 1
        incoming = bullet_row(self.row, self.col, self.pid)
        if incoming == 0:
            bullet_in_row = 1;
        features = direction + surroundings + enemy_loc + incoming + [enemy_in_row] + [bullet_in_row]
        self.actions[self.net.decide(features)]()

    def collide(self,object):
        if isinstance(object, Bullet):
            if object.pid != self.pid:
                self.fit = -1*object.pid
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
        self.rect.y += self.velocity.y
        self.rect.x += self.velocity.x
        self.velocity.grav_on = True
        self.row, self.col = getclosest((self.rect.x,self.rect.y))
        self.locs.add((self.row,self.col))
        player_locs.update({self.pid:(self.row , self.col)})
        if self.bullet_timer <= v.shoot_req: self.bullet_timer += 1

    def save(self, gen):
        if not self.slave:
            self.net.save_net( len(self.locs), gen, self.fit,)

    def jump(self):
        if self.velocity.grav_on == 0:
            self.velocity.y = v.jump_vel

    def right(self):
        self.velocity.x = v.player_speed
        self.direction = 1

    def left(self):
        self.velocity.x = -1 * v.player_speed
        self.direction = -1

    def shoot(self):
        if self.bullet_timer > v.shoot_req:
            b = Bullet(self.pid, self.rect.center, self.direction)
            group.add(b)
            self.bullet_timer -= v.shoot_req

    def obey(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.jump()
                if event.key == pygame.K_LEFT:
                    self.left()
                if event.key == pygame.K_RIGHT:
                    self.right()
                if event.key == pygame.K_SPACE:
                    self.shoot()


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
        global bullet_locs
        self.rect.x += self.velocity.x
        if self.colliding:
            self.kill()
            if self.pid in bullet_locs:
                bullet_locs.pop(self.pid)
        else:
            self.row, self.col = getclosest((self.rect.x,self.rect.y))
            bullet_locs.update({self.pid:(self.row,self.col)})

# returns distance from sprite to block in each cardinal location
def get_distances(row, col):
    N=1
    NE=1
    E=1
    SE=1
    S=1
    SW=1
    W=1
    NW=1
    # print("row:" + str(row) + " col:"+str(col))
    if not (row > len(dgrid)-2 or row < 1 or col > len(dgrid)-2 or col < 1):
        while dgrid[row+N][col]!=1:
            N+=1
        while dgrid[row-S][col]!=1:
            S+=1
        while dgrid[row][col+E]!=1:
            E+=1
        while dgrid[row][col-W]!=1:
            W+=1
        while dgrid[row+NE][col+NE]!=1:
            NE+=1
        while dgrid[row+SE][col-SE]!=1:
            SE+=1
        while dgrid[row-SW][col-SW]!=1:
            SW+=1
        while dgrid[row-NW][col+NW]!=1:
            NW+=1
   # print([N,NE,E,SE,S,SW,W,NW])
    return[N,NE,E,SE,S,SW,W,NW]

# gets the relative distance between sprite and closest
def relative_enemy_loc(row, col, pid):
    eloc = get_closest(row, col, pid)
    vert = row-eloc[0]
    horz = col-eloc[1]
    return [vert,horz]

# gets the location of the nearest bullet
def bullet_row(row, col, pid):
    # print(bullet_locs)
    if len(bullet_locs) > 0:
        bloc = get_closest(row, col, pid, bullet_locs)
        if bloc:
            return [row - bloc[0]]
    return[0]


# returns nearest enemy or bullet
def get_closest(row, col, pid, range=player_locs):
    min_dist = 10000
    closest = 0
    for key in range:
        if key != pid:
            eloc = range[key]
            dist = math.sqrt((row-eloc[0]) ** 2 + (col-eloc[1]) ** 2)
            if dist < min_dist:
                min_dist = dist
                closest = key
    if closest == 0:
        return False
    return range[closest]