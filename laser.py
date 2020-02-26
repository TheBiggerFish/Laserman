import curses
from board import Board
from coord import Direction
import time



moves = {
    'w': (1, Direction.UP),
    'a': (1, Direction.LEFT),
    's': (1, Direction.DOWN),
    'd': (1, Direction.RIGHT),
    
    'i': (2, Direction.UP),
    'j': (2, Direction.LEFT),
    'k': (2, Direction.DOWN),
    'l': (2, Direction.RIGHT)
}
fire = {
    ' ': 1,
    '\n': 2
}
drop = {
    'q': (1,1),
    'e': (1,2),
    'u': (2,1),
    'o': (2,2)
}

def main(stdscr):
    board = Board()
    stdscr.nodelay(True)
    while(not board.gameOver()):
        board.timeStep()
        board.drawBoard(stdscr)
        time.sleep(0.05)
        try:
            char = stdscr.getkey()
        except:
            continue
        
        if char in moves:
            board.move(moves[char][0],moves[char][1])
        elif char in fire:
            board.fire(fire[char])
        elif char in drop:
            board.drop(drop[char][0],drop[char][1])
        elif len(char) == 1 and ord(char) == 27:
            return

    stdscr.nodelay(False)
    stdscr.clear()
    stdscr.addstr(1,1,'Game over')
    stdscr.getkey()



if __name__ == '__main__':
    curses.wrapper(main)
