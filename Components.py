class Component():
    def __init__(self, pnum):
        self.pid = pnum


class Velocity(Component):
    def __init__(self,x, y, pid):
        Component.__init__(self,pid)
        self.x = x
        self.y = y
        self.grav_on = True


