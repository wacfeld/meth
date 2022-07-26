from curses import *
import curses

import tempfile, os

# import sys

import config
import lexer
from lexer import root
from lexer import curexpr

stdscr = initscr()
noecho()
raw()
stdscr.keypad(True)

# setup temp dir and files
# output file
# outfile = sys.argv[1]
tmpdir = '/dev/shm/'
td = tempfile.TemporaryDirectory(dir=tmpdir)
os.chdir(td.name) # cd to td
fname = '__temp__'
texfname = fname + '.tex'
f = open(texfname, 'w')

# compile latex code
os.system('latex -interaction=batchmode %s > /dev/null &' % fname)
# os.system('xdvi -watchfile 0.01 %s%s.dvi' % (tmpdir, fname))


# buffer where characters are read, displayed, processed
charbuf = ''

stdscr.move(curses.LINES-1, 0)

# read characters into minibuffer
while(True):
    # generate latex code
    latex = config.create_doc(config.create_eqn(root.getstr()))
    # latex = str(root.terms[0]) + '\n' + str(root.terms[0].terms) + '\n' + str(root.terms[0].terms[0].terms) if root.terms else 'hi'

    # display latex code
    stdscr.move(0, 0)
    stdscr.clrtoeol()
    stdscr.addstr(latex)

    # write latex code to outfile
    f.seek(0,0)
    f.write(latex)
    f.truncate()
    f.flush()

    # compile latex code
    os.system('latex -interaction=batchmode %s > /dev/null &' % texfname)

    # move back to bottom
    stdscr.move(curses.LINES-1, 0)

    # key = stdscr.getkey()
    key = stdscr.getch()

    # backspace
    if key == 263:
        charbuf = charbuf[:-1] # remove character from buffer; does nothing to empty buffer

    # 
    elif key == 3:
        exit(0)

    # tab
    elif key == 9:
        # send current text to the lexer
        charbuf = lexer.lex(charbuf, ' ')

        # navigate forward
        config.nav_fore()

    # enter
    elif key == 10:
        # send current text to the lexer
        charbuf = lexer.lex(charbuf, ' ')

        # navigate upward
        config.nav_up()

    # delete
    elif key == 330:
        # send current text to the lexer
        charbuf = lexer.lex(charbuf, ' ')
        
        # navigate downward
        config.nav_down()

    elif key == 353:
        # send current text to the lexer
        charbuf = lexer.lex(charbuf, ' ')

        # navigate backward
        config.nav_back()
    
    # escape ()
    # TODO

    # regular character
    else:
        assert chr(key).isprintable() or chr(key).isspace()
        key = chr(key)
        charbuf = lexer.lex(charbuf, key) # send buffer + new character to lexer

    # display buffer
    stdscr.clrtoeol()
    stdscr.addstr(charbuf)


    # write latex code to outfile
    f.seek(0,0)
    f.write(latex)
    f.flush()
    f.truncate()

    # compile latex code
    os.system('latex -interaction=batchmode %s > /dev/null &' % texfname)


f.close()
endwin()
