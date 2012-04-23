import copy
import pygame as pg
import time
import random

from Queue import Queue
from pygame.locals import *

DIMENSION = 6*5*5*2*2
APPLES = 1
DOTSIZE = 5 * DIMENSION / 60
size = X, Y = DIMENSION - DOTSIZE, DIMENSION - DOTSIZE
DOTS = (X / DOTSIZE -1) * ( Y / DOTSIZE - 1)
black = 0, 0, 0
pg.init()
screen = pg.display.set_mode(size)


def xp():
    return random.randint(1, X / DOTSIZE - 1) * DOTSIZE
def yp():
    return random.randint(1, Y / DOTSIZE - 1) * DOTSIZE

def inbounds(item):
    if item[0] in [0, X]:
        return False
    if item[1] in [0, Y]:
        return False
    return True

class AppleClass:
    def __init__(self):
        self.location = [xp(), yp()]
    def respawn(self, takenlist):
        spawn = [xp(), yp()]
        while spawn in takenlist:
            spawn = [xp(), yp()]
        self.location = spawn

applelist = [AppleClass() for j in range(APPLES)]

class SnakeClass:
    def __init__(self):
        self.body = [[300,300]]
        self.current = [0,DOTSIZE]
        self.maximized = False

    def move(self, index, value, apples=[]):
        first = copy.copy(self.body[0])
        first[index] += value
        if not inbounds(first) or first in self.body:
            return False
        inApple = False
        for apple in apples:
            if apple.location == first:
                inApple = True
                self.body = [first] + self.body
                if len(self.body) == DOTS -1:
                    self.maximized = True
                apple.respawn(self.body)
                break
        if not inApple:
            self.body = [first] + self.body[:-1]
        self.current = [index, value]
        return True

def gameover(reason):
    myfont = pg.font.SysFont("Comic Sans MS", 30)
    label1 = myfont.render(reason, 1, pg.Color("blue"))
    label2 = myfont.render("Space to play again", 1, pg.Color("blue"))
    label3 = myfont.render("ESC to exit", 1, pg.Color("blue"))
    screen.blit(label1, (210, 220))
    screen.blit(label2, (170, 270))
    screen.blit(label3, (205, 320))
    pg.display.flip()

snake = SnakeClass()

pg.display.set_caption("Snake")
direction = [0, DOTSIZE]
GAMEOVER = False
TIC = True
q = Queue()
pg.time.set_timer(USEREVENT+1, 120)
RUN = True
head = None
al = None
while RUN:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            RUN = False
        elif event.type == MOUSEBUTTONDOWN:
            pass
        elif event.type == USEREVENT+1:
            TIC = True
        elif (event.type == KEYDOWN):
            if (event.key == K_ESCAPE):
                RUN = False
            elif (event.key == K_SPACE):
                if GAMEOVER:
                    GAMEOVER = False
                    snake.__init__()
                    direction = [0, DOTSIZE]
            elif (event.key == K_RIGHT):
                q.put([0, DOTSIZE])
            elif (event.key == K_LEFT):
                q.put([0, (-1) * DOTSIZE])
            elif (event.key == K_UP):
                q.put([1, (-1) * DOTSIZE])
            elif (event.key == K_DOWN):
                q.put([1, DOTSIZE])

    if not GAMEOVER:
        screen.fill(black)
        pg.draw.rect(screen, pg.Color("white"),(0,0,X,Y), DOTSIZE)
        for apple in applelist:
            al = copy.copy(apple.location)
            al[1] -= 7
            pg.draw.circle(screen, pg.Color("red"), apple.location, DOTSIZE / 2)
            pg.draw.circle(screen, pg.Color("green"), al, DOTSIZE / 6)
        for bodypart in snake.body:
            pg.draw.circle(screen, pg.Color("yellow"), bodypart, DOTSIZE / 2)
        head = copy.copy(snake.body[0])
        head[0] -= 5
        pg.draw.circle(screen, pg.Color("red"), head, DOTSIZE / 8)
        head[0] += 10
        pg.draw.circle(screen, pg.Color("red"), head, DOTSIZE / 8)
        if TIC:
            if not q.empty():
                direction = q.get()
            if direction == [snake.current[0], snake.current[1]*(-1)]:
                direction[1] *= (-1)
            if not snake.move(*direction, apples=applelist):
                GAMEOVER = True
                gameover("Game Over")
            TIC = False
        if snake.maximized:
            GAMEOVER = True
            gameover("Congratulations!")
    pg.display.flip()
