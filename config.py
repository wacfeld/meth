import lexer

texpre = '''\\documentclass{minimal}
\\usepackage{standalone}
\\usepackage{amsmath}

\\usepackage{xcolor}
\\newcommand{\\mathcolorbox}[2]{\\colorbox{#1}{$\\displaystyle #2$}}

\\usepackage{mathtools}
\\usepackage{amssymb}

\\begin{document}\n'''

texpost = '\n\\end{document}'

eqnpre = '\\begin{equation*}\n'
eqnpost = '\n\\end{equation*}\n'

def highlight(s):
    return '\\mathcolorbox{red}{' + s + '}'

def create_doc(body):
    return texpre + body + texpost

def create_eqn(eqn):
    return eqnpre + eqn + eqnpost

def list_expr():
    return lexer.Expression('LIST')

def sum_expr():
    # create sum expr
    e = lexer.Expression('sum')
    e.terms=[list_expr(), list_expr(), list_expr()]

    # insert
    lexer.insert_expr(e)

    # focus bottom term
    lexer.curexpr = e.terms[0]

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
