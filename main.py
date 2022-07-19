from curses import *
import curses

import config
import lexer

stdscr = initscr()
noecho()
raw()
stdscr.keypad(True)


# buffer where characters are read, displayed, processed
charbuf = ''

# root expression, which is a list of terms
root = lexer.Expression('LIST')

# current expression, used to navigate/edit
curexpr = root

stdscr.move(curses.LINES-1, 0)

# read characters into minibuffer
while(True):
    key = stdscr.getkey()

    charbuf = lexer.lex(charbuf, key) # send buffer + new character to lexer

    stdscr.move(curses.LINES-1, 0)
    stdscr.clrtoeol()
    stdscr.addstr(charbuf)

endwin()
