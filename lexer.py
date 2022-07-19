import config
import main

class Expression:
    def __init__(self, op, parent=None, terms=[], data=None):
        self.op = op
        self.terms = terms
        self.data = data
        self.parent = parent

    def getstr(self):
        f = config.getstrs[self.op]
        return f(self)

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def data_type(s):
    # 3.14
    if is_number(s):
        return "number"
    
    # Aardvark
    elif s.isalpha():
        return "alpha"

    #  
    elif s.isspace():
        return "space"

    # *#!~
    else:
        return "special"


# take in string, turn into data expr, append to nearest list expr
def append_data(s):
    # navigate upward to nearest list expression
    while main.curexpr.op != 'LIST':
        main.curexpr.op = main.curexpr.parent # the root expression is a list, so this should never encounter None
        
    # append data
    dat = Expression('DATA', parent=main.curexpr, data=s)
    main.curexpr.terms.append(dat)

    # focus new data
    main.curexpr = dat
    

def lex(buf, cur):
    # backspace
    if key == 'KEY_BACKSPACE':
        charbuf = charbuf[:-1] # remove character from buffer; does nothing to empty buffer
        return charbuf

    # if new buffer is valid op
    if buf + cur in config.ops:
        # execute corresponding function
        f = config.ops[buf + cur]
        f()
        
        # clear buffer
        return ''

    # buf is one contiguous piece of data (all letters, all numbers, etc.)
    # cur determines what to do next

    # newline, space, tab, which AT THE MOMENT do the exact same thing
    # manually separate data pieces
    # TODO ^^^
    elif cur.isspace():
        # special case - do nothing
        if buf == '':
            pass

        # create new data expression, append to current list
        else:
            append_data(buf)

        # buffer is now empty
        return ''
            
    # data type changes - separate
    # e.x. '123' followed by 'a'
    elif data_type(buf) != data_type(cur):
        # break off first piece
        append_data(buf)

        # leave second piece in buffer
        return cur

    # 
    elif cur in config.ops:
        # process data
        append_data(buf)
        
        # execute corresponding function
        f = config.ops[cur]
        f()

        # clear buffer
        return ''

    # otherwise do nothing
    else:
        return buf + cur
