from coord import Coord,Direction

class Player():
    def __init__(self,pos,facing):
        self.pos = pos
        self.facing = facing
        self.mirror = 3
        self.lives = 3
        self.firing = 0

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

    
