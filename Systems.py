import vars as v
import Components
v.init()


class Gravity():
    def __init__(self):
        self.vlist = list()

    def update(self):
        for vel in self.vlist:
            if vel.grav_on:
                vel.y += v.gravity

    def add(self,entity):
        for c in entity.components:
            if type(c) == Components.Velocity:
                self.vlist.append(c)
