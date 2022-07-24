from curses import *
import curses

import config
import lexer
from lexer import root
from lexer import curexpr

stdscr = initscr()
noecho()
raw()
stdscr.keypad(True)


# buffer where characters are read, displayed, processed
charbuf = ''

stdscr.move(curses.LINES-1, 0)

# read characters into minibuffer
while(True):
    # key = stdscr.getkey()
    key = stdscr.getch()

    # backspace
    if key == 263:
        charbuf = charbuf[:-1] # remove character from buffer; does nothing to empty buffer

    # 
    if key == 3:
        exit(0)
    
    # escape ()
    # TODO

    # regular character
    else:
        assert chr(key).isprintable()
        key = chr(key)
        charbuf = lexer.lex(charbuf, key) # send buffer + new character to lexer

    # generate latex code
    latex = root.getstr()

    # display latex code
    stdscr.move(0, 0)
    stdscr.clrtoeol()
    stdscr.addstr(latex)

    # display buffer
    stdscr.move(curses.LINES-1, 0)
    stdscr.clrtoeol()
    stdscr.addstr(charbuf)


endwin()
