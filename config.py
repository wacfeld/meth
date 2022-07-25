import lexer

def list_expr():
    return lexer.Expression('LIST')

def sum_expr():
    e = lexer.Expression('sum')
    e.terms=[list_expr(), list_expr(), list_expr()]
    lexer.insert_expr(e)

# def blank_str():
#     return '\\square'
blank_str = '\\square'

def DATA_str(expr):
    return expr.data

def LIST_str(expr):
    # if empty, return blank
    if not expr.terms:
        return blank_str
        
    return ' '.join(e.getstr() for e in expr.terms)

def lim_str(expr):
    appr = expr.terms[0]
    val = expr.terms[1]

    return '\\lim_{%s} %s' % (appr, val)

def sum_str(expr):
    bot = expr.terms[0].getstr()
    top = expr.terms[1].getstr()
    val = expr.terms[2].getstr()

    return '\\sum_{%s}^{%s} %s' % (bot, top, val)

getstrs = { 'lim':lim_str, 'sum':sum_str, 'DATA':DATA_str, 'LIST':LIST_str, }

# tokens corresponding to op names
op_tokens = { 'lim':5 , 'sum':sum_expr , }
