import lexer

texpre = '''\\documentclass{article}
\\usepackage[active,tightpage]{preview}
\\renewcommand{\\PreviewBorder}{1in}

\\usepackage{standalone}
\\usepackage{amsmath}

\\usepackage{xcolor}
\\newcommand{\\mathcolorbox}[2]{\\colorbox{#1}{$\\displaystyle #2$}}
\\newcommand{\\hlfancy}[2]{\\sethlcolor{#1}\\hl{#2}}

\\usepackage{mathtools}
\\usepackage{amssymb}

\\begin{document}
\\begin{preview}
\n'''

texpost = '''\n
\\end{preview}
\\end{document}'''

eqnpre = '\\begin{equation*}\n'
eqnpost = '\n\\end{equation*}\n'

def color_fg(s):
    return '\\textcolor{green}{' + s + '}'

def color_bg(s):
    return '\\mathcolorbox{green}{' + s + '}'

def create_doc(body):
    return texpre + body + texpost

def create_eqn(eqn):
    return eqnpre + eqn + eqnpost

def list_expr():
    return lexer.Expression('LIST')

# like tab on input boxes on websites
def tab_fore():
    # if list focused, 
    # TODO
    pass

# like shift-tab on input boxes on websites
def tab_back():
    pass
    # TODO

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
