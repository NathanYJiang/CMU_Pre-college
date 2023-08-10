from cmu_graphics import *
from utils.hexCoords import getHexCoords
from utils.messages import updateMessages

def setStatus(button, app):
    if button.label == 'trade':
        app.gameState = 'trade'
        updateMessages(app, 'Pick a resource to trade away')
        
    elif button.label == 'knight':
        if (app.curPlayer.cards['grain'] >= 1
            and app.curPlayer.cards['wool'] >= 1
            and app.curPlayer.cards['ore'] >= 1):
            # enough resources
            app.gameState = 'knight robber'
            updateMessages(app, f'Player {app.curPlayerID+1} moving robber')
        else:
            # not enough resources
            updateMessages(app, 'Not enough resources to buy a knight')

    elif button.label == 'road':
        if (app.curPlayer.cards['lumber'] >= 1 
            and app.curPlayer.cards['brick'] >= 1):
            # enough resources
            app.gameState = 'build road'
            updateMessages(app, f'Player {app.curPlayerID+1} placing road')
        else:
            # not enough resources
            updateMessages(app, 'Not enough resources to build a road')

    elif button.label == 'settlement':
        if (app.curPlayer.cards['lumber'] >= 1
            and app.curPlayer.cards['brick'] >= 1
            and app.curPlayer.cards['wool'] >= 1
            and app.curPlayer.cards['grain'] >= 1):
            # enough resources
            app.gameState = 'build settlement'
            updateMessages(app, f'Player {app.curPlayerID+1} placing settlement')
        else:
            # not enough resources
            updateMessages(app, 'Not enough resources to build a settlement')

    elif button.label == 'city':
        if (app.curPlayer.cards['grain'] >= 2 
            and app.curPlayer.cards['ore'] >= 3):
            # enough resources
            app.gameState = 'build city'
            updateMessages(app, f'Player {app.curPlayerID+1} placing city')
        else:
            # not enough resources
            updateMessages(app, 'Not enough resources to build a city')

    else:
        app.gameState = 'end turn'


def buildSettlement(app, mouseX, mouseY, free=False):
    for (px, py) in app.board.coords:
        if (distance(mouseX, mouseY, *getHexCoords(app, px, py)) <= 12
            and app.board.buildings[(px, py)] == None):
            if free:
                # next stage in start phase
                app.stage += 1
            else:
                app.curPlayer.cards['lumber'] -= 1
                app.curPlayer.cards['brick'] -= 1
                app.curPlayer.cards['wool'] -= 1
                app.curPlayer.cards['grain'] -= 1
            
            app.board.buildings[(px, py)] = (1, app.curPlayer.color)
            updateMessages(app, f'Player {app.curPlayerID+1} built a settlement')
            app.curPlayer.vp += 1

            app.gameState = 'player turn'
            return
    
    # not a valid placement
    updateMessages(app, 'Not a valid placement')


def buildCity(app, mouseX, mouseY):
    # go through coords and check if enough resources to place a city
    for (px, py) in app.board.coords:
        if (distance(mouseX, mouseY, *getHexCoords(app, px, py)) <= 12
            and app.board.buildings[(px, py)] == (1, app.curPlayer.color)):
            app.curPlayer.cards['grain'] -= 2 
            app.curPlayer.cards['ore'] -= 3

            app.board.buildings[(px, py)] = (2, app.curPlayer.color)
            updateMessages(app, f'Player {app.curPlayerID+1} built a city')
            app.curPlayer.vp += 1

            app.gameState = 'player turn'
            return
    
    # not a valid placement
    updateMessages(app, 'Not a valid placement')


def buildRoad(app, mouseX, mouseY, free=False):
    # go through coords and check if enough resources to place a city
    for (px, py) in app.board.midpoints:
        if (distance(mouseX, mouseY, *getHexCoords(app, px, py)) <= 12
            and app.board.buildings[(px, py)] == None):
            if free:
                # enough resources
                app.stage += 1
            else:
                app.curPlayer.cards['lumber'] -= 1
                app.curPlayer.cards['brick'] -= 1

            app.board.buildings[(px, py)] = ('r', app.curPlayer.color)
            updateMessages(app, f'Player {app.curPlayerID+1} built a road')

            app.gameState = 'player turn'
            return
    
    # not a valid placement
    updateMessages(app, 'Not a valid placement')


def moveRobber(app, mouseX, mouseY, knight=False):
    for (px, py) in app.board.centers:
        if (distance(mouseX, mouseY, *getHexCoords(app, px, py)) <= 18 
            and app.robberCoords != (px, py)):
            if knight:
                app.curPlayer.cards['grain'] -= 1
                app.curPlayer.cards['wool'] -= 1
                app.curPlayer.cards['ore'] -= 1

            app.robberCoords = (px, py)

            app.gameState = 'player turn'
            return

    # not a valid placement
    updateMessages(app, 'Not a valid placement')

def trade(app, mouseX, mouseY):
    for resButton in app.resButtons:
        if resButton.onClick(app, mouseX, mouseY):
            if app.curPlayer.cards[resButton.label] >= 3:
                # enough resources
                app.curPlayer.cards[resButton.label] -= 3
                updateMessages(app, 'Pick a resource to receive')
                app.gameState = 'pick resource'
            else:
                # not enough resources
                updateMessages(app, 'Not enough of that resource to trade')
                app.gameState = 'player turn'

            return

    # not a valid placement
    updateMessages(app, 'Not a valid resource')

def pickResource(app, mouseX, mouseY):
    for resButton in app.resButtons:
        if resButton.onClick(app, mouseX, mouseY):
            app.curPlayer.cards[resButton.label] += 1
            updateMessages(app, f'Player {app.curPlayerID+1} completed a trade')
            app.gameState = 'player turn'
            return

    # not a valid placement
    updateMessages(app, 'Not a valid resource')