from classes.board import Board
from utils.hexCoords import getHexCoords
from cmu_graphics import *
from utils.images import getImages
from classes.player import Player
import random


def onAppStart(app):
    app.s = 70
    app.startX = 0
    app.startY = 300
    app.colors = [rgb(237, 1, 1), rgb(15, 152, 245), rgb(246, 247, 239), 
                  rgb(246, 139, 46)]
    app.resources = {'wood', 'brick', 'sheep', 'wheat', 'ore'}
    restart(app)


def restart(app):
    app.numPlayers = 2
    app.players = []
    for i in range(app.numPlayers):
        app.players.append(Player(app, i))

    app.board = Board()
    getImages(app)
    onTurn(app)

def onTurn(app):
    # roll the dice (move to dice button later)
    app.dice1 = random.randint(1, 6)
    app.dice2 = random.randint(1, 6)
    app.roll = app.dice1 + app.dice2

def redrawAll(app):
    # draw board
    app.board.draw(app)

    # draw dice
    drawImage(app.dice[app.dice1], 630, 590)
    drawImage(app.dice[app.dice2], 710, 590)

    # random settlement/city test
    app.board.drawSettlement(*getHexCoords(app, 8, 1), fill=app.colors[0])
    app.board.drawCity(*getHexCoords(app, 8, 2), fill=app.colors[1])

    # random playericon test
    drawImage(app.icons[1], 50, 50, align='center')


runApp(width=1400, height=850)