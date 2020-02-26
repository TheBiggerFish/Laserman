from coord import Coord,Direction

class Player():
    def __init__(self,pos,facing):
        self.pos = pos
        self.facing = facing
        self.mirrors = 3
        self.lives = 3
        self.firing = 0
        self.firingLine = {}

    def __str__(self):
        if self.facing == Direction.UP:
            return '^'
        elif self.facing == Direction.RIGHT:
            return '>'
        elif self.facing == Direction.DOWN:
            return 'v'
        elif self.facing == Direction.LEFT:
            return '<'
        else:
            return 'X'

    def at(self,pos):
        return self.pos == pos

    def fired(self):
        if self.firing > 0:
            self.firing -= 1
            if self.firing == 0:
                self.firingLine.clear()


    
