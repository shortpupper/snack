from curses import wrapper
import curses
from random import randrange as rand, choice

class keys:
 class unix:
  down = 258
  up = 259
  left = 260
  right = 261

"""

so make it so that it could clear the screen or get rid of the last pos

"""


def main(stdscr):
 doesDebug = False
 my, mx = stdscr.getmaxyx()
 wallSizeY, wallSizeX = my, mx
 py, px = int(wallSizeY/2), int(wallSizeX/2) #also starting pos
 ogpy, ogpx = py, px
 pos = []
 wallTiles = []
 k,l = 6, 6
 extraApples = 0
 apples = [(k, l), (3, 7), (5, 9)]
 length = 5
 wall = True
 wallTileCar = "░▒▓█"[1]
 oglenght = length
 canPlaceAtpplesInSnack = False
 lastArrowKey = None # 0: down, 1: up, 2: left, 3: right
 curses.init_pair(10, curses.COLOR_RED, curses.COLOR_BLACK)
 curses.init_pair(11, curses.COLOR_YELLOW, curses.COLOR_WHITE)
 stdscr.clear()
 kko = 0
 tst = 1
 doesdie = True
 autoSnack = True
 def closestAtpple():
  if len(apples) > 0:
   pass
  return (0, 0)
  pass
 def makeWall():
  #var for the position of the wall
  wallYX = []
  #makes the bottom wall
  for i in range(wallSizeX-1):
   stdscr.addstr(wallSizeY-1, i, wallTileCar)
   wallYX += [(wallSizeY-1, i)]
  #makes the top wall
  for i in range(wallSizeX-1):
   stdscr.addstr(0, i, wallTileCar)
   wallYX += [(0, i)]
  #makes the left wall
  for i in range(wallSizeY-1):
   stdscr.addstr(i, wallSizeX-1, wallTileCar)
   wallYX += [(i, wallSizeX-1)]
  #makes the right wall
  for i in range(wallSizeY):
   stdscr.addstr(i, 0, wallTileCar)
   wallYX += [(i, 0)]
  return wallYX
 def hardCollide():
  y = []
  if (py-1, px) in pos: y.append(0)
  if (py+1, px) in pos: y.append(1)
  if (py, px+1) in pos: y.append(2)
  if (py, px-1) in pos: y.append(3)
  return y
 def doIcollideXYList(psx, psy, pos):
  if (psy, psx) in pos: return True
  return False
 def doesSnackHitWall():
  r = [x for x in pos if x in wallTiles]
  if len(r) >= 1: return True
  return False
 def doesSnackHitSnake():
  li = len(list(dict.fromkeys(pos)))
  lo = len(pos)
  if li < lo: return True
  return False
 for x in range(extraApples):
  if not canPlaceAtpplesInSnack:
   while True:
    k, l = rand(1, wallSizeY-1), rand(1, wallSizeX-1)
    if (k, l) not in pos: 
     apples.append((k, l))
     break
  else: 
   k, l = rand(1, wallSizeY-1), rand(1, wallSizeX-1)
   apples.append((k, l))
 if wall: wallTiles = makeWall()
 while True:
  stdscr.addstr(py, px, "%")
  stdscr.addstr(5, 5, str(kko)) if doesDebug else None
  if len(pos) > 0: stdscr.addstr(pos[-1][0], pos[-1][1], "+")#π
  pos.append((py, px))# if tst != 1 or len(pos) <= 1 else None
  if doesSnackHitWall(): kko = 1
  if doesSnackHitSnake() and doesdie: kko = 1
  if len(pos) > length:
   ok = pos[0]
   stdscr.addstr(ok[0], ok[1], " ")
   pos.pop(0)
  #if (pos[-1][0], pos[-1][1]) == apples[0]: # if fail
  if (pos[-1][0], pos[-1][1]) in apples:
   length += 1
   apples.pop(apples.index((pos[-1][0], pos[-1][1])))
   if not canPlaceAtpplesInSnack:
    while True:
     k, l = rand(1, wallSizeY-1), rand(1, wallSizeX-1)
     if (k, l) not in pos: 
      apples.append((k, l))
      break
   else: 
    k, l = rand(1, wallSizeY-1), rand(1, wallSizeX-1)
    apples.append((k, l))
   #for e in range(5):#len(apples)
    #k, l = rand(1, my-1), rand(1, mx-1)
    #apples.append((k, l))
  for x in apples:
   stdscr.addstr(x[0], x[1], "@", curses.color_pair(10))
  stdscr.addstr(k, l, "@", curses.color_pair(10))
  #stdscr.addstr(my-4, 2, str([str(x).replace("0", "up").replace("1", "down").replace("2", "right").replace("3", "left") for x in hardCollide()])+" "*10)
  if doesDebug:
   stdscr.addstr(my-4, 2, str([x for x in range(4) if x not in hardCollide()]))
   stdscr.addstr(my-5, 2, str([str(x).replace("0", "up").replace("1", "down").replace("2", "right").replace("3", "left") for x in range(4) if x not in hardCollide()]))
   stdscr.addstr(my-6, 2, str(wallTiles[:4]))
  if autoSnack: curses.halfdelay(1)
  c = stdscr.getch()
  # y, x, string
  if doesDebug:
   stdscr.addstr(my-1, 2, str(c))
   stdscr.addstr(my-2, 2, str(hardCollide()))
   stdscr.addstr(my-3, 2, str([str(x).replace("0", "up").replace("1", "down").replace("2", "right").replace("3", "left") for x in hardCollide()])+" "*10)
  #stdscr.addstr(my-3, 2, str(pos))
  #stdscr.addstr(my-4, 2, str(0 if (py, px) in pos else 1))
  #stdscr.addstr(my-1, 8, str(apples))
  if c == ord('p'): print("s")
  elif c == keys.unix.down and kko == 0: #down
   py += 1
   lastArrowKey = 0
  elif c == keys.unix.up and kko == 0: #up
   py -= 1
   lastArrowKey = 1
  elif c == keys.unix.left and kko == 0:# left
   px -= 1
   lastArrowKey = 2
  elif c == keys.unix.right and kko == 0:#right
   px += 1
   lastArrowKey = 3
  elif c == ord('|'): break
  elif c == ord('p'):
   k, l = rand(1, wallSizeY-1), rand(1, wallSizeX-1)
   apples.append((k, l))
  else:
   if kko == 0 and c != ord("b"):
    r = [x for x in range(4) if x not in hardCollide()] #x != lastArrowKey and
    r = choice(r) if r != [] else ValueError
    #stdscr.addstr(my-5, 8, str(r))
    if r == 0: #up
     py -= 1
     lastArrowKey = 0
    elif r == 1: #down
     py += 1
     lastArrowKey = 1
    elif r == 2: #left
     px += 1
     lastArrowKey = 2
    elif r == 3: #right
     px -= 1
     lastArrowKey = 3
   elif c == ord("b"):stdscr.addstr(wallSizeY-4, 4, str(0 if (py, px) in pos else 1))
  #if kko == 1 and c == 259:
  # c2 = stdscr.getch()
  # if c2 == 260:
  #  print("Window")
  if c == 10 or autoSnack and kko == 1:
   stdscr.clear()
   if wall: wallTiles = makeWall()
   kko = 0
   pos = []
   length = oglenght
   py, px = ogpy, ogpx
  if kko == 1:stdscr.addstr(int(wallSizeY/2), int(wallSizeX/2), str("You Died"))
  stdscr.refresh()
 stdscr.getkey()
wrapper(main)


def main2(stdscr):
 curses.init_pair(10, curses.COLOR_RED, curses.COLOR_BLACK)
 stdscr.clear()
 curses.mousemask(1)
 i = 0
 #curses.color_pair(10)
 while True:
  curses.halfdelay(10)
  c = stdscr.getch()
  if c == curses.KEY_MOUSE:
   m = curses.getmouse()
   stdscr.addstr(6, 6, str(m))
   stdscr.addstr(m[2], m[1], "h",  curses.color_pair(10))
  i += 1
  stdscr.addstr(1, 2, str(i))
  stdscr.refresh()
 stdscr.getkey()
#wrapper(main2)




"""
def testSpeed():
 from time import perf_counter as times
 b = times()
 print(f"1, '{times()}', {b}")
 i = 1
 if i:
  print(f"5, '{times()}', {times()-b}")
 elif not o:
  print(f"3, '{times()}', {times()-b}")
 b = times()
 o = True
 if o:
  print(f"2, '{times()}', {times()-b}")
 print(f"4, '{times()}', {b}")
 elif not i:
  print(f"6, '{times()}', {times()-b}")
 print(f"7, '{times()}', {times()-b}")
testSpeed()
  for x in pos:
   for g in pos:
    if x == g:
     kko = 2
"""
