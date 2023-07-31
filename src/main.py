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


# call the function to draw the points on the hexagon
def redrawAll(app):
    app.board.draw(app)
    app.board.drawSettlement(*getHexCoords(app, 8, 1), 'blue')
    drawCircle(20, 20, 1, fill='red')
    app.board.drawCity(*getHexCoords(app, 8, 2), 'red')
    drawCircle(20, 50, 1, fill='red')

runApp(width=1200, height=700)