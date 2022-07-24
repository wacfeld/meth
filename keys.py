from curses import *
import curses

stdscr = initscr()
noecho()
raw()
stdscr.keypad(True)

while(True):
    key = stdscr.getch()
    if key ==  3: # 
        break
    char = str(key)
    stdscr.addstr(char)
    stdscr.addstr('\n')


endwin()
