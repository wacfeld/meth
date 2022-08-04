from graphics import *
width = None
height = None

def init(w, h):
    global width, height
    width = w
    height = h
    
    win = GraphWin("meth", w, h) # init window

    # testimg = Image(Point(100,100), "euler/Zeta_Neo-Euler.svg")
    # testimg.draw(win)
