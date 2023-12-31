from classes.board import Board
from utils.hexCoords import getHexCoords
from cmu_graphics import *
from utils.images import getImages
from classes.player import Player
from classes.button import Button
import random
from utils.messages import updateMessages
from utils.actions import (buildRoad, buildSettlement, buildCity, moveRobber, 
                           trade, pickResource)


def onAppStart(app):
    # fixed variables
    app.s = 70
    app.startX = 0
    app.startY = 300
    app.screen = 'start'
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

    # number of players (fixed at 2)
    app.numPlayers = 2
    app.players = []
    for i in range(app.numPlayers):
        app.players.append(Player(app, i))

    # get all images
    getImages(app)

    # buttons
    # action buttons
    app.buttons = []
    sx, sy = 430, 735
    labels = ['trade', 'knight', 'road', 'settlement', 'city', 'end']
    for i in range(len(labels)): 
        app.buttons.append(Button(sx + 80*i, sy, 70, 70, labels[i]))

    # resource buttons
    app.resButtons = []
    for i in range(5):
        app.resButtons.append(Button(45 + 70*i, 685, 50, 73, app.resources[i], 
                                     True))
    
    # make a new board and get all the images
    app.board = Board()

    # messages
    app.messages = ['Welcome to Settlers of Ketan']

    # initial dice
    app.dice1 = random.randint(1, 6)
    app.dice2 = random.randint(1, 6)

    # pick random player
    app.curPlayerID = random.randint(0, app.numPlayers-1)
    nextPlayer(app)
    updateMessages(app, f'Player {app.curPlayerID+1} placing settlement')

    # start game
    app.gameState = 'start game'
    app.stage = 1


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

    # rolled a robber
    if app.roll == 7:
        updateMessages(app, f'Player {app.curPlayerID+1} rolled 7')
        app.gameState = 'move robber'
        updateMessages(app, f'Player {app.curPlayerID+1} moving robber')
    else:
        updateMessages(app, f'Player {app.curPlayerID+1} rolled {app.roll}')
        # give players resources
        for player in app.players:
            player.getResources(app)
        
        app.gameState = 'player turn'


def redrawAll(app):
    if app.screen == 'start':
        drawImage(app.setting, 0, 0)
        drawImage(app.logo, app.width//2, 190, align='center')
        drawLabel('Created by Nathan Jiang', app.width//2, 285, align='center', 
                  size=28, font='monospace', italic=True)
        drawLabel('Click to start', app.width//2, 500, align='center', size=48, 
                  font='monospace', bold=True)
    elif app.screen == 'game':
        # draw board
        app.board.draw(app)

        # draw dice
        drawImage(app.dice[app.dice1], 670, 610)
        drawImage(app.dice[app.dice2], 755, 610)

        # draw player icon and vp counter
        drawImage(app.icons[app.curPlayerID], 60, 60, align='center')
        drawLabel(app.curPlayer.vp, 60, 110, align='center', size=36, 
                font='monospace')

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
        
        # draw building costs
        drawImage(app.buildCost[app.curPlayerID], 1100, 620, align='center')
        
        # draw circles for placement
        if app.gameState == 'start game':
            if app.stage % 2 == 1:
                drawBuildingPlaces(app)
            else:
                drawRoadPlaces(app)
        elif app.gameState[:5] == 'build':
            if app.gameState[6:] == 'road':
                drawRoadPlaces(app)
            else:
                drawBuildingPlaces(app)
        elif app.gameState in ['move robber', 'knight robber']:
            drawRobberPlaces(app)


def drawRoadPlaces(app):
    for (px, py) in app.board.midpoints:
        drawCircle(*getHexCoords(app, px, py), 12, fill='yellow', 
                   opacity=60)


def drawBuildingPlaces(app):
    for (px, py) in app.board.coords:
        drawCircle(*getHexCoords(app, px, py), 12, fill='yellow', 
                   opacity=60)


def drawRobberPlaces(app):
    for (px, py) in app.board.centers:
        drawCircle(*getHexCoords(app, px, py), 18, fill='yellow', 
                   opacity=60)


def onMousePress(app, mouseX, mouseY):
    if app.screen == 'start':
        app.screen = 'game'
        restart(app)

    # no actions allowed if the game is over
    elif app.screen == 'game':
        if app.gameOver:
            return

        # starting action
        elif app.gameState == 'start game':
            if app.stage == 1:
                app.gameState = 'build settlement'
                buildSettlement(app, mouseX, mouseY, True)
            elif app.stage == 2:
                app.gameState = 'build road'
                buildRoad(app, mouseX, mouseY, True)
                if app.stage == 3:
                    nextPlayer(app)
            elif app.stage == 3:
                app.gameState = 'build settlement'
                buildSettlement(app, mouseX, mouseY, True)
            elif app.stage == 4:
                app.gameState = 'build road'
                buildRoad(app, mouseX, mouseY, True)
            elif app.stage == 5:
                app.gameState = 'build settlement'
                buildSettlement(app, mouseX, mouseY, True)
            elif app.stage == 6:
                app.gameState = 'build road'
                buildRoad(app, mouseX, mouseY, True)
                if app.stage == 7:
                    nextPlayer(app)
            elif app.stage == 7:
                app.gameState = 'build settlement'
                buildSettlement(app, mouseX, mouseY, True)
            elif app.stage == 8:
                app.gameState = 'build road'
                buildRoad(app, mouseX, mouseY, True)

                # if starting phase is over
                if app.stage >= 9:
                    nextPlayer(app)
                    nextTurn(app)
                    app.gameState = 'player turn'

                    # exit start game state
                    return
            
            if app.gameState == 'player turn':
                message = f'Player {app.curPlayerID+1} placing '
                if app.stage % 2 == 0:
                    updateMessages(app, message + 'road')
                else:
                    updateMessages(app, message + 'settlement')

            app.gameState = 'start game'

        # on player turn, check actions of all buttons
        elif app.gameState == 'player turn':
            for button in app.buttons:
                if button.onClick(app, mouseX, mouseY): 
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
            elif app.gameState == 'knight robber':
                moveRobber(app, mouseX, mouseY, True)
            elif app.gameState == 'trade':
                trade(app, mouseX, mouseY)
            elif app.gameState == 'pick resource':
                pickResource(app, mouseX, mouseY)
            
            if app.curPlayer.vp >= 10:
                updateMessages(app, f'Player {app.curPlayerID+1} wins with ' 
                               + f'{app.curPlayer.vp} points!')
                otherPlayerID = (app.curPlayerID + 1) % app.numPlayers
                updateMessages(app, f'Player {otherPlayerID+1} got second place' 
                               + f' with {app.players[otherPlayerID].vp} points')
                updateMessages(app, 'Press n for a new game or h to return ' 
                               + 'to the home screen')
                app.gameOver = True


def onKeyPress(app, key):
    if app.gameOver:
        if key == 'n':
            restart(app)
        elif key == 'h':
            app.screen = 'start'
    elif (app.gameState != 'move robber'
          and app.gameState != 'start game'
          and app.gameState != 'pick resource'
          and key == 'escape'):
        app.gameState = 'player turn'
    elif key == 'r':
        for resource in app.resources:
            app.curPlayer.cards[resource] += 1


runApp(width=1350, height=850)
