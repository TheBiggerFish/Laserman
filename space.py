from enum import Enum
from coord import Direction
class Object(Enum):
    OPEN = 0
    WALL = 1
    ROCK = 2
    MIRROR_1 = 3
    MIRROR_2 = 4
    

class Space:
    def __init__(self,object=Object.OPEN):
        self.object = object

    def __str__(self):
        if self.object == Object.WALL:
            return 'W'
        elif self.object == Object.OPEN:
            return '.'
        elif self.object == Object.MIRROR_1:
            return '\\'
        elif self.object == Object.MIRROR_2:
            return '/'

    def isEmpty(self):
        return self.object == Object.OPEN
    
    def isWall(self):
        return self.object == Object.WALL
    
    def isRock(self):
        return self.object == Object.ROCK

    def isMirror(self):
        return self.object == Object.MIRROR_1 or self.object == Object.MIRROR_2
    
    @staticmethod
    def mirrorReflect(dir, type):
        if type == Object.MIRROR_1:
            if dir == Direction.UP:
                return Direction.LEFT
            elif dir == Direction.RIGHT:
                return Direction.DOWN
            elif dir == Direction.DOWN:
                return Direction.RIGHT
            elif dir == Direction.LEFT:
                return Direction.UP
            else:
                return dir
        elif type == Object.MIRROR_2:            
            if dir == Direction.UP:
                return Direction.RIGHT
            elif dir == Direction.RIGHT:
                return Direction.UP
            elif dir == Direction.DOWN:
                return Direction.LEFT
            elif dir == Direction.LEFT:
                return Direction.DOWN
            else:
                return dir
        else:
            return dir