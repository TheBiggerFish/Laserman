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
        self.p1FL = {} #Player 1 firing line
        self.p2FL = {} #Player 2 firing line

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
                if self.p1.pos != Coord(pos.x,pos.y) and self.p2.pos != Coord(pos.x,pos.y):
                    return True
        return False

    def move(self,who,where):
        if who == 1 and self.p1.firing == 0:
            if self.spaceOpen(self.p1.pos + Coord.dir(where)):
                self.p1.pos += Coord.dir(where)
            self.p1.facing = where
        elif who == 2 and self.p2.firing == 0:
            if self.spaceOpen(self.p2.pos + Coord.dir(where)):
                self.p2.pos += Coord.dir(where)
            self.p2.facing = where

    def gameOver(self):
        return self.p1.lives == 0 or self.p2.lives == 0

    def fire(self,who):
        if who == 1:
            self.p1.firing = 20
            dir = self.p1.facing
            pos = self.p1.pos + dir
            while self.on(pos) and not self[pos].isWall():
                if dir == Direction.RIGHT or dir == Direction.LEFT:
                    self.p1FL[pos] = '\u2014 '
                else:
                    self.p1FL[pos] = '|'
                if self[pos].isMirror():
                    del self.p1FL[pos]
                    dir = Space.mirrorReflect(dir=dir,type=self[pos].object)
                pos = pos + dir


        elif who == 2:
            self.p2.firing = 20
            dir = self.p2.facing
            pos = self.p2.pos + dir
            while self.on(pos) and not self[pos].isWall():
                if dir == Direction.RIGHT or dir == Direction.LEFT:
                    self.p2FL[pos] = '\u2014 '
                else:
                    self.p2FL[pos] = '|'
                if self[pos].isMirror():
                    del self.p2FL[pos]
                    dir = Space.mirrorReflect(dir=dir,type=self[pos].object)
                pos = pos + dir
    
    def drop(self,who,which):
        if who == 1 and self.p1.mirror > 0:
            self.p1.mirror -= 1
            if which == 1:
                self[self.p1.pos] = Space(Object.MIRROR_1)
            elif which == 2:
                self[self.p1.pos] = Space(Object.MIRROR_2)
        if who == 2 and self.p2.mirror > 0:
            self.p2.mirror -= 1
            if which == 1:
                self[self.p2.pos] = Space(Object.MIRROR_1)
            elif which == 2:
                self[self.p2.pos] = Space(Object.MIRROR_2)


    def timeStep(self):
        if self.p1.firing > 0:
            self.p1.firing -= 1
            if self.p1.firing == 0:
                self.p1FL.clear()
        if self.p2.firing > 0:
            self.p2.firing -= 1
            if self.p2.firing == 0:
                self.p2FL.clear()
    
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
                elif Coord(col,row) in self.p1FL:
                    stdscr.addstr(row,col*2,self.p1FL[Coord(col,row)],curses.color_pair(3))
                elif Coord(col,row) in self.p2FL:
                    stdscr.addstr(row,col*2,self.p2FL[Coord(col,row)],curses.color_pair(3))
                else:
                    stdscr.addstr(row,col*2,str(self.grid[row][col])+' ')
