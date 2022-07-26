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

def del_expr():
    ce = lexer.curexpr

    # parent is list
    if ce.parent and ce.parent.op == 'LIST':
        p = ce.parent
        
        # get index
        idx = p.terms.index(ce)
        
        # delete from list
        del p.terms[idx]

        if not p.terms:
            lexer.curexpr = p

        else:
            # refocus
            idx = min(idx, len(p.terms)-1)
            lexer.curexpr = p.terms[idx]
    
    # otherwise, this is a list
    else:
        assert ce.op == 'LIST'

        # clear list
        ce.terms = []
        
        # focus does not change
        

def nav_fore():
    ce = lexer.curexpr
    if ce.parent and ce.parent.terms:
        idx = ce.parent.terms.index(ce)
        idx += 1
        idx %= len(ce.parent.terms)
        lexer.curexpr = ce.parent.terms[idx]

def nav_back():
    ce = lexer.curexpr
    if ce.parent and ce.parent.terms:
        idx = ce.parent.terms.index(ce)
        idx -= 1
        idx %= len(ce.parent.terms)
        lexer.curexpr = ce.parent.terms[idx]

def nav_up():
    if lexer.curexpr.parent:
        lexer.curexpr = lexer.curexpr.parent

def nav_down():
    if lexer.curexpr.terms:
        lexer.curexpr = lexer.curexpr.terms[0]

# # like tab on input boxes on websites
# def tab_fore():
#     oldcur = lexer.curexpr
    
#     # if not focused on list, navigate up to list
#     while lexer.curexpr.op != 'LIST':
#         lexer.curexpr = lexer.curexpr.parent

#     # if list is root, do nothing
#     if lexer.curexpr == lexer.root or not lexer.curexpr.parent:
#         lexer.curexpr = oldcur
#         return
    
#     # navigate up until not last term
#     while lexer.curexpr.parent.terms[-1] == lexer.curexpr:
#         lexer.curexpr = lexer.curexpr.parent
        
#         if not lexer.curexpr.parent:
#             lexer.curexpr = oldcur
#             return
        
#     # move forward one term
#     idx = lexer.curexpr.parent.terms.index(lexer.curexpr)
#     lexer.curexpr = lexer.curexpr.parent.terms[idx+1]


# # like shift-tab on input boxes on websites
# def tab_back():
#     oldcur = lexer.curexpr
    
#     # if not focused on list, navigate up to list
#     while lexer.curexpr.op != 'LIST':
#         lexer.curexpr = lexer.curexpr.parent

#     # if list is root, revert
#     if not lexer.curexpr.parent:
#         lexer.curexpr = oldcur
#         return
    
#     # navigate up until not first term
#     while lexer.curexpr.parent.terms[0] == lexer.curexpr:
#         lexer.curexpr = lexer.curexpr.parent
        
#         if not lexer.curexpr.parent:
#             lexer.curexpr = oldcur
#             return
    
#     # move backward one term
#     idx = lexer.curexpr.parent.terms.index(lexer.curexpr)
#     lexer.curexpr = lexer.curexpr.parent.terms[idx-1]

def sum_expr():
    # create sum expr
    e = lexer.Expression('sum', terms=[list_expr(), list_expr(), list_expr()])

    # insert
    lexer.insert_expr(e)

    # focus bottom term
    lexer.curexpr = e.terms[0]

def lim_expr():
    # create lim expr
    e = lexer.Expression('lim', terms=[list_expr(), list_expr()])

    # insert
    lexer.insert_expr(e)

    # focus approaches term
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
    appr = expr.terms[0].getstr()
    val = expr.terms[1].getstr()

    return '\\lim_{%s} %s' % (appr, val)

def sum_str(expr):
    bot = expr.terms[0].getstr()
    top = expr.terms[1].getstr()
    val = expr.terms[2].getstr()

    return '\\sum_{%s}^{%s} %s' % (bot, top, val)

getstrs = { 'lim':lim_str, 'sum':sum_str, 'DATA':DATA_str, 'LIST':LIST_str, }

# tokens corresponding to op names
op_tokens = { 'lim':lim_expr , 'sum':sum_expr , }
