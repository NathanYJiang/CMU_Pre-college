from classes.board import Board
from utils.hexCoords import getHexCoords
from cmu_graphics import *
from utils.images import getImages
import random


def onAppStart(app):
    app.s = 70
    app.startX = 0
    app.startY = 300
    app.colors = [rgb(237, 1, 1), rgb(15, 152, 245), rgb(246, 247, 239), 
                  rgb(246, 139, 46)]
    restart(app)


def restart(app):
    app.numPlayers = 2
    app.board = Board()
    
    getImages(app)


def redrawAll(app):
    app.board.draw(app)
    dice1 = random.randint(1, 6)
    dice2 = random.randint(1, 6)
    drawImage(app.dice[dice1], 630, 590)
    drawImage(app.dice[dice2], 710, 590)
    roll = dice1 + dice2

    # random settlement/city
    app.board.drawSettlement(*getHexCoords(app, 8, 1), fill=app.colors[0])
    app.board.drawCity(*getHexCoords(app, 8, 2), fill=app.colors[1])

    # random playericon
    drawImage(app.icons[1], 50, 50, align='center')


runApp(width=1400, height=850)