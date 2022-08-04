#include <ncurses.h>
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/*
  lexer converts characters into tokens
  tokens are added to expression structure via logic
  expression structure is converted into characters
  
  e.g. (= (limit x infinity (/ 1 x)) 0) is an expression
  now if the user were to type in "= lim x infinity sin ( 1 / x )" (or something roughly like that), then firstly:

  = : create skeleton equality, put the existing equality in the LHS, focus the RHS
  lim : create skeleton limit, put in focused area, focus limit variable
  x : put x in focused area, focus limit target
  infinity: put infinity in focused area, focus limit expression
  sin: create skeleton sine, put in focused area, focus interior
  ( : create skeleton parentheses, focus interior
  1 : put 1 in focused area
  / : create skeleton division, put 1 in numerator, focus denominator
  x : put x in focused area, return focus to parentheses
  ) : return focus to sine, return focus to limit, return focus to equality, done
  
  the lexer sees x followed by either a space, closing parenthesis, operator, etc. and recognizes it as a variable, as opposed to part of a keyword
  similar goes for numbers
  
  the expression builder always expects a single subexpression to fill in components
  the exception is for parenthetical expressions, which expect subexpressions until a matching closing parenthesis
  when an expression is completely filled in then focus is returned to the parent
  i.e. focus is a stack
  this stack (tree) can be traversed up and down and sideways via hotkeys
  
  there are two modes, insert mode (types keys and backspace), and visual mode
  there is no normal mode
  
  modes can be toggled with the escape key, or they can be temporarily switched on using alt
  config file determines ALL hotkeys (and tokens, and expression structures associated with tokens)
  
  tokens are lim, sum, sin, oo (infinity), +, etc.
  characters and special characters can't mix, however, to avoid having to put too many spaces
  nevermind that ^ ... for example, just do the whatever 1+ token break thing
  expressions structures are associated with tokens like lim, sum, +, (), etc.
  
  you are allowed to leave an expression incomplete, perhaps by pressing tab
  so for example limit as x approaches 0 from the negative side, we can put a superscript minus sign
 */

int main(int argc, char **argv)
{
  /* assert(argc == 2); */
  /* char *fname = argv[1]; */

  initscr();
  raw();
  noecho();
  keypad(stdscr, TRUE);

  // buffer that holds characters before they are recognized as tokens
  char charbuf[100];

  move(LINES-1, 0);
  int c;
  for(;;)
  {
    c = getch();
    addch(c);
  }
}
