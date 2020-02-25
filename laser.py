import curses
from board import Board
from coord import Direction
import time



p1Moves = {
    'w': Direction.UP,
    'a': Direction.LEFT,
    's': Direction.DOWN,
    'd': Direction.RIGHT
}
p2Moves = {
    'i': Direction.UP,
    'j': Direction.LEFT,
    'k': Direction.DOWN,
    'l': Direction.RIGHT
}
fire = {
    ' ': 1,
    '\n': 2
}
drop = {
    'e': 1,
    'o': 2
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
        
        if char in p1Moves:
            board.move(1,p1Moves[char])
        elif char in p2Moves:
            board.move(2,p2Moves[char])
        elif char in fire:
            board.fire(fire[char])
        elif char in drop:
            board.drop(drop[char])
        elif char == 'q':
            return



if __name__ == '__main__':
    curses.wrapper(main)
