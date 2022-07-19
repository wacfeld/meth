ops = { 'lim' , 'sum' , '*' }

getstrs = { 'lim':lim_expr, 'sum':sum_expr, 'DATA':DATA_str, 'LIST':LIST_str}

def DATA_str(expr):
    return expr.data

def LIST_str(expr):
    return ' '.join(e.getstr for e in expr.terms)

def lim_str(expr):
    appr = expr.terms[0]
    val = expr.terms[1]

    return '\\lim_{%s} %s' % (appr, val)

def sum_str(expr):
    bot = expr.terms[0].getstr()
    top = expr.terms[1].getstr()
    val = expr.terms[2].getstr()

    return '\\sum_{%s}^{%s} %s' % (bot, top, val)

# def plus_str(expr):
#     return ' + '.join(e.getstr() for e in expr.terms)
