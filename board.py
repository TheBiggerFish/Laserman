from player import Player
from coord import Coord,Direction
from space import Space,Object
import curses

class Board:
    width = 17
    height = 17
    def __init__(self):
        self.p1 = Player(pos=Coord(0,0),facing=Direction.RIGHT)
        self.p2 = Player(pos=Coord(Board.width-1,Board.height-1),facing=Direction.LEFT)
        self.grid = Board.newGrid()

    def __getitem__(self,pos):
        return self.grid[pos.y][pos.x]
    
    def __setitem__(self,pos,item):
        self.grid[pos.y][pos.x] = item 

    @staticmethod
    def newGrid():
        grid = []
        for i in range(Board.width):
            row = []
            for j in range(Board.height):
                if (i % 2 == 1 and j % 2 == 1) and not Board.onBorder(Coord(i,j)):
                    row.append(Space(Object.WALL))
                else:
                    row.append(Space(Object.OPEN))
            grid.append(row)
        return grid

    @staticmethod
    def on(coord):
        if coord.x >= 0 and coord.y >= 0:
            if coord.x < Board.width and coord.y < Board.height:
                return True
        return False

    @staticmethod
    def onBorder(coord):
        if coord.x == 0 or coord.y == 0:
            return True
        if coord.x == Board.width - 1 or coord.y == Board.height - 1:
            return True
        return False

    def spaceOpen(self,pos):
        if Board.on(pos):
            if self[pos].isEmpty():
                if self.playerAt(pos) is None:
                    return True
        return False

    def playerAt(self,pos):
        if self.p1.pos == pos:
            return self.p1
        elif self.p2.pos == pos:
            return self.p2
        else:
            return None

    def getPlayer(self,who):
        if who == 1:
            return self.p1
        elif who == 2:
            return self.p2
        else:
            raise Exception()

    def move(self,who,where):
        player = self.getPlayer(who)
        
        if player.firing == 0:
            if self.spaceOpen(player.pos + Coord.dir(where)):
                player.pos += Coord.dir(where)
            player.facing = where


    def gameOver(self):
        return self.p1.lives == 0 or self.p2.lives == 0

    def fire(self,who):
        player = self.getPlayer(who)
        
        player.firing = 20
        dir = player.facing
        pos = player.pos + dir
        while self.on(pos) and not self[pos].isWall():
            target = self.playerAt(pos)
            if target is not None:
                target.lives -= 1

            if self[pos].isMirror():
                dir = Space.mirrorReflect(dir=dir,type=self[pos].object)

            elif dir == Direction.RIGHT or dir == Direction.LEFT:
                player.firingLine[pos] = '\u2014'

            else:
                player.firingLine[pos] = '|'
            pos = pos + dir

    
    def drop(self,who,which):
        player = self.getPlayer(who)

        if player.mirrors > 0:
            player.mirrors -= 1
            if which == 1:
                self[player.pos] = Space(Object.MIRROR_1)
            elif which == 2:
                self[player.pos] = Space(Object.MIRROR_2)


    def timeStep(self):
        self.p1.fired()
        self.p2.fired()
    
    def drawBoard(self,stdscr):
        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        for row in range(Board.height):
            for col in range(Board.width):
                if self.p1.at(Coord(col,row)):
                    stdscr.addstr(row,col*2,str(self.p1)+' ',curses.color_pair(1))
                elif self.p2.at(Coord(col,row)):
                    stdscr.addstr(row,col*2,str(self.p2)+' ',curses.color_pair(2))
                elif Coord(col,row) in self.p1.firingLine:
                    stdscr.addstr(row,col*2,self.p1.firingLine[Coord(col,row)],curses.color_pair(3))
                elif Coord(col,row) in self.p2.firingLine:
                    stdscr.addstr(row,col*2,self.p2.firingLine[Coord(col,row)],curses.color_pair(3))
                else:
                    stdscr.addstr(row,col*2,str(self.grid[row][col])+' ')
