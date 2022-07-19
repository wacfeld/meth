from curses import *
import curses

stdscr = initscr()
noecho()
raw()
stdscr.keypad(True)

while(True):
    # char = str(stdscr.getch())
    char = stdscr.getkey()
    stdscr.move(0,0)
    stdscr.addstr('                   ')
    stdscr.move(0,0)
    stdscr.addstr(char)


endwin()
