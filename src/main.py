from classes.board import Board
from utils.hexCoords import getHexCoords
from cmu_graphics import *

def onAppStart(app):
    app.s = 70
    app.startX = 0
    app.startY = 300
    restart(app)


def restart(app):
    app.board = Board()


def redrawAll(app):
    app.board.draw(app)
    app.board.drawSettlement(*getHexCoords(app, 8, 1), 'red')
    app.board.drawCity(*getHexCoords(app, 8, 2), 'blue')
    print(len(app.board.centers))
    for x, y in app.board.midpoints:
        drawCircle(*getHexCoords(app, x, y), 5, fill='magenta')


runApp(width=1200, height=700)