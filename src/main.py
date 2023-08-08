from classes.board import Board
from utils.hexCoords import getHexCoords
from cmu_graphics import *
from utils.images import getImages
from classes.player import Player
from classes.button import Button
import random
from utils.messages import updateMessages
from utils.actions import buildRoad, buildSettlement, buildCity, moveRobber


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
    # new game
    app.gameOver = False

    # number of players (fixed at 2 rn)
    app.numPlayers = 2
    app.players = []
    for i in range(app.numPlayers):
        app.players.append(Player(app, i))
    
    # make a new board and get all the images
    app.board = Board()
    getImages(app)
    
    # buttons
    app.buttons = []
    sx, sy = 420, 735

    # missing trade and dv
    labels = ['road', 'settlement', 'city', 'end']
    for i in range(len(labels)): 
        label = labels[i]
        app.buttons.append(Button(sx + 80*i, sy, label))

    # messages
    app.messages = ['Welcome to Settlers of Ketan']

    # initial dice
    app.dice1 = random.randint(1, 6)
    app.dice2 = random.randint(1, 6)

    # pick random player
    app.curPlayerID = random.randint(0, app.numPlayers-1)
    nextPlayer(app)

    # start game
    app.gameState = 'start game'


def nextPlayer(app):
    app.curPlayerID += 1
    app.curPlayerID %= app.numPlayers
    app.curPlayer = app.players[app.curPlayerID]


def nextTurn(app):
    # new player turn
    nextPlayer(app)
    updateMessages(app, f"Player {app.curPlayerID+1}'s turn")

    # roll the dice
    app.dice1 = random.randint(1, 6)
    app.dice2 = random.randint(1, 6)
    app.roll = app.dice1 + app.dice2

    # rolled a robber!
    if app.roll == 7:
        updateMessages(app, f'Player {app.curPlayerID+1} rolled 7')
        app.gameState = 'move robber'
    else:
        updateMessages(app, f'Player {app.curPlayerID+1} rolled {app.roll}')
        # give players resources
        for player in app.players:
            player.getResources(app)
        
        app.gameState = 'player turn'


def redrawAll(app):
    # draw board
    app.board.draw(app)

    # draw dice
    drawImage(app.dice[app.dice1], 670, 610)
    drawImage(app.dice[app.dice2], 755, 610)

    # draw player icon
    drawImage(app.icons[app.curPlayerID], 60, 60, align='center')

    # draw player resources
    drawRect(30, 670, 360, 150, fill=app.curPlayer.color, border='black')
    for i in range(5):
        resource = app.resources[i]
        drawImage(app.resImages[resource], 45 + 70*i, 685)
        drawLabel(app.curPlayer.cards[resource], 70 + 70*i, 790, size=36, 
                  font='monospace')
    
    # draw buttons
    for button in app.buttons:
        button.draw(app)
    
    # draw messages
    for i in range(len(app.messages)):
        drawLabel(app.messages[i], 1100, 50 + 25*i, size=16)
    
    # draw circles for placement
    if app.gameState[:5] == 'build':
        if app.gameState[6:] == 'road':
            for (px, py) in app.board.midpoints:
                drawCircle(*getHexCoords(app, px, py), 12, fill='yellow', 
                           opacity=60)
        else:
            for (px, py) in app.board.coords:
                drawCircle(*getHexCoords(app, px, py), 12, fill='yellow', 
                           opacity=60)
    elif app.gameState == 'move robber':
        for (px, py) in app.board.centers:
            drawCircle(*getHexCoords(app, px, py), 18, fill='yellow', 
                       opacity=60)


def onMousePress(app, mouseX, mouseY):
    # no actions allowed if the game is over
    if app.gameOver: return

    # starting action
    if app.gameState == 'start game':
        # initial settlements
        buildSettlement(app, mouseX, mouseY, True)
        buildRoad(app, mouseX, mouseY, True)
        nextPlayer(app)
        buildSettlement(app, mouseX, mouseY, True)
        buildRoad(app, mouseX, mouseY, True)
        buildSettlement(app, mouseX, mouseY, True)
        buildRoad(app, mouseX, mouseY, True)
        nextPlayer(app)
        buildSettlement(app, mouseX, mouseY, True)
        buildRoad(app, mouseX, mouseY, True)

    # on player turn, check actions of all buttons
    if app.gameState == 'player turn':
        for button in app.buttons:
            if button.onClick(mouseX, mouseY): 
                break

        if app.gameState == 'end turn':
            nextTurn(app)

    # player has acted, so check what they want to do
    else:
        if app.gameState == 'build road':
            buildRoad(app, mouseX, mouseY)
        elif app.gameState == 'build settlement':
            buildSettlement(app, mouseX, mouseY)
        elif app.gameState == 'build city':
            buildCity(app, mouseX, mouseY)
        elif app.gameState == 'move robber':
            moveRobber(app, mouseX, mouseY)
        
        if app.curPlayer.vp >= 10:
            updateMessages(app, f'Player {app.curPlayerID+1} wins with ' + 
                           f'{app.curPlayer.vp} points!')
            nextPlayer(app)
            updateMessages(app, f'Player {app.curPlayerID+1} got second place' + 
                           f' with {app.curPlayer.vp} points')
            updateMessages(app, 'Press n for a new game')
            app.gameOver = True


def onKeyPress(app, key):
    if app.gameOver:
        if key == 'n':
            restart(app)
    elif app.gameState not in ['move robber', 'new game'] and key == 'escape':
        app.gameState = 'player turn'


runApp(width=1350, height=850)
