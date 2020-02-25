from enum import Enum
class Direction(Enum):
    NONE = 0
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4

class Coord:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def __str__(self):
        return '(' + str(self.x) + ',' + str(self.y) + ')'

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __add__(self,other):
        if type(other) == Coord:
            return Coord(self.x+other.x,self.y+other.y) 
        elif type(other) == Direction:
            return self + Coord.dir(other)
    
    def __hash__(self):
        return self.y*1000000 + self.x
    
    @staticmethod
    def dir(which):
        if which == Direction.UP:
            return Coord(0,-1)
        elif which == Direction.RIGHT:
            return Coord(1,0)
        elif which == Direction.DOWN:
            return Coord(0,1)
        elif which == Direction.LEFT:
            return Coord(-1,0)
        else:
            return Coord(0,0)
    
    