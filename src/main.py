from classes.board import Board
from utils.hexCoords import getHexCoords
from cmu_graphics import *
from utils.images import getImages
from classes.player import Player
from classes.button import Button
import random


def onAppStart(app):
    app.s = 70
    app.startX = 0
    app.startY = 300
    app.colors = [rgb(237, 1, 1), rgb(15, 152, 245), rgb(246, 247, 239), 
                  rgb(246, 139, 46)]
    app.resources = ['lumber', 'brick', 'wool', 'grain', 'ore']
    app.tileToRes = {
        'forest': 'lumber',
        'hill': 'brick',
        'pasture': 'wool',
        'field': 'grain',
        'mountain': 'ore'
    }

    restart(app)


def restart(app):
    # number of players (fixed at 2 rn)
    app.numPlayers = 2
    app.players = []
    for i in range(app.numPlayers):
        app.players.append(Player(app, i))
    
    # make a new board and get all the images
    app.board = Board()
    getImages(app)

    #TEST
    app.board.buildings[(8, 1)] = (1, app.players[0].color)
    
    # buttons
    app.buttons = []
    sx, sy = 550, 750
    for i in range(6):
        label = ['trade', 'dv', 'road', 'settlement', 'city', 'end'][i]
        app.buttons.append(Button(sx + 80*i, sy, label))
    
    app.curPlayerID = random.randint(0, app.numPlayers-1)
    onTurn(app)

def onTurn(app):
    # new player turn
    app.curPlayerID += 1
    app.curPlayerID %= app.numPlayers

    # roll the dice (move to dice button later)
    app.dice1 = random.randint(1, 6)
    app.dice2 = random.randint(1, 6)
    app.roll = app.dice1 + app.dice2

def redrawAll(app):
    curPlayer = app.players[app.curPlayerID]

    # draw board
    app.board.draw(app)

    # draw dice
    drawImage(app.dice[app.dice1], 650, 600)
    drawImage(app.dice[app.dice2], 735, 600)

    # random settlement/city test
    app.board.drawSettlement(*getHexCoords(app, 8, 1), fill=app.colors[0])
    app.board.drawCity(*getHexCoords(app, 8, 2), fill=app.colors[1])

    # random playericon test
    drawImage(app.icons[app.curPlayerID], 50, 50, align='center')

    # draw player resources
    for i in range(5):
        resource = app.resources[i]
        drawImage(app.resImages[resource], 70 + 70*i, 700)
        drawLabel(curPlayer.cards[resource], 95 + 70*i, 805, size=36, 
                  font='monospace')
    
    curPlayer.getResources(app)

    for button in app.buttons:
        button.draw(app)

def onMousePress(app, mouseX, mouseY):
    onTurn(app)


runApp(width=1400, height=850)