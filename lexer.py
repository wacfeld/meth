import config

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


# take in string, turn into data expr, insert to right of nearest list subexpr
def insert_data(s):
    import main
    
    # create data expr
    dat = Expression('DATA', data=s)

    # current expr is a list: insert on far right end
    if main.curexpr.op == 'LIST':
        main.curexpr.terms.append(dat)
        dat.parent = main.curexpr

    # navigate upward to nearest list expression
    else:
        prevexpr = None
        while main.curexpr.op != 'LIST':
            prevexpr = main.curexpr
            main.curexpr = main.curexpr.parent # the root expression is a list, so this must terminate
        
        # insert to right of prevexpr
        ind = main.curexpr.terms.index(prevexpr) + 1
        main.curexpr.terms.insert(ind, dat)
        dat.parent = main.curexpr
        
    # focus new data
    main.curexpr = dat
    

def lex(buf, cur):
    # if new buffer is valid op
    if buf + cur in config.op_tokens:
        # execute corresponding function
        f = config.op_tokens[buf + cur]
        f()
        
        # clear buffer
        return ''
    
    # buf is one contiguous piece of data (all letters, all numbers, etc.)
    # cur determines what to do next

    # newline, space, tab, which AT THE MOMENT do the exact same thing
    # manually separate data pieces
    # TODO ^^^
    elif cur.isspace():
        # blank buffer - do nothing
        if buf == '':
            pass

        # create new data expression, append to current list
        else:
            insert_data(buf)

        # buffer is now empty
        return ''
            
    # data type changes - separate
    # e.x. '123' followed by 'a'
    elif data_type(buf) != data_type(cur) and buf != '':
        # break off first piece
        insert_data(buf)

        # leave second piece in buffer
        return cur

    # data followed by single-character op, e.x. a_ for subscripting
    elif cur in config.op_tokens:
        # process data
        insert_data(buf)
        
        # execute corresponding function
        f = config.op_tokens[cur]
        f()

        # clear buffer
        return ''

    # otherwise do nothing, return new buffer
    else:
        return buf + cur
