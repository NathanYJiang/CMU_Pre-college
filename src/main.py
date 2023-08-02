from classes.board import Board
from utils.hexCoords import getHexCoords
from cmu_graphics import *
from utils.images import getImages

def onAppStart(app):
    app.s = 70
    app.startX = 0
    app.startY = 300
    app.colors = [rgb(237, 1, 1), rgb(15, 152, 245), rgb(246, 247, 239), 
                  rgb(246, 139, 46)]
    restart(app)


def restart(app):
    app.board = Board()
    getImages(app)


def redrawAll(app):
    app.board.draw(app)
    drawImage(app.dice[1], 620, 550)
    drawImage(app.dice[2], 700, 550)

    # random settlement/city
    app.board.drawSettlement(*getHexCoords(app, 8, 1), fill=app.colors[0])
    app.board.drawCity(*getHexCoords(app, 8, 2), fill=app.colors[1])

    # top left circles
    drawCircle(10, 10, 10, fill=app.colors[0])
    drawCircle(10, 30, 10, fill=app.colors[1])
    drawCircle(10, 50, 10, fill=app.colors[2])
    drawCircle(10, 70, 10, fill=app.colors[3])
    


runApp(width=1400, height=850)