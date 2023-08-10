from cmu_graphics import *
from utils.hexCoords import getHexCoords
from utils.messages import updateMessages

def setStatus(button, app):
    if button.label == 'trade':
        app.gameState = 'trade'
        updateMessages(app, 'Pick a resource to trade away')
    elif button.label == 'knight':
        app.gameState = 'knight robber'
        updateMessages(app, f'Player {app.curPlayerID+1} moving robber')
    elif button.label == 'road':
        app.gameState = 'build road'
        updateMessages(app, f'Player {app.curPlayerID+1} placing road')
    elif button.label == 'settlement':
        app.gameState = 'build settlement'
        updateMessages(app, f'Player {app.curPlayerID+1} placing settlement')
    elif button.label == 'city':
        app.gameState = 'build city'
        updateMessages(app, f'Player {app.curPlayerID+1} placing city')
    else:
        app.gameState = 'end turn'


def buildSettlement(app, mouseX, mouseY, free=False):
    # go through coords and check if enough resources to place a settlement
    for (px, py) in app.board.coords:
        if (distance(mouseX, mouseY, *getHexCoords(app, px, py)) <= 12
            and app.board.buildings[(px, py)] == None):
            resourcesNeeded = ['lumber', 'brick', 'wool', 'grain']

            # learned the all function from https://docs.python.org/3/library/functions.html#all
            if free or all(app.curPlayer.cards[r] >= 1 for r in resourcesNeeded):
                # enough resources
                if not free:
                    for r in resourcesNeeded:
                        app.curPlayer.cards[r] -= 1
                
                app.board.buildings[(px, py)] = (1, app.curPlayer.color)
                updateMessages(app, f'Player {app.curPlayerID+1} built a settlement')
                app.curPlayer.vp += 1

                # next stage in starting phase
                if free:
                    app.stage += 1
            else:
                # not enough resources
                updateMessages(app, 'Not enough resources to build a settlement')
            
            app.gameState = 'player turn'
            return
    
    # not a valid placement
    updateMessages(app, 'Not a valid placement')


def buildCity(app, mouseX, mouseY):
    # go through coords and check if enough resources to place a city
    for (px, py) in app.board.coords:
        if (distance(mouseX, mouseY, *getHexCoords(app, px, py)) <= 12
            and app.board.buildings[(px, py)] == (1, app.curPlayer.color)):
            if (app.curPlayer.cards['grain'] >= 2 
                and app.curPlayer.cards['ore'] >= 3):
                # enough resources
                app.curPlayer.cards['grain'] -= 2 
                app.curPlayer.cards['ore'] -= 3

                app.board.buildings[(px, py)] = (2, app.curPlayer.color)
                updateMessages(app, f'Player {app.curPlayerID+1} built a city')
                app.curPlayer.vp += 1
            else:
                # not enough resources
                updateMessages(app, 'Not enough resources to build a city')
            
            app.gameState = 'player turn'
            return
    
    # not a valid placement
    updateMessages(app, 'Not a valid placement')


def buildRoad(app, mouseX, mouseY, free=False):
    # go through coords and check if enough resources to place a city
    for (px, py) in app.board.midpoints:
        if (distance(mouseX, mouseY, *getHexCoords(app, px, py)) <= 12
            and app.board.buildings[(px, py)] == None):
            if (free or (app.curPlayer.cards['lumber'] >= 1
                         and app.curPlayer.cards['brick'] >= 1)):
                # enough resources
                if not free:
                    app.curPlayer.cards['lumber'] -= 1
                    app.curPlayer.cards['brick'] -= 1

                app.board.buildings[(px, py)] = ('r', app.curPlayer.color)
                updateMessages(app, f'Player {app.curPlayerID+1} built a road')

                # next stage in starting phase
                if free:
                    app.stage += 1
            else:
                # not enough resources
                updateMessages(app, 'Not enough resources to build a road')
            
            app.gameState = 'player turn'
            return
    
    # not a valid placement
    updateMessages(app, 'Not a valid placement')


def moveRobber(app, mouseX, mouseY, knight=False):
    for (px, py) in app.board.centers:
        if (distance(mouseX, mouseY, *getHexCoords(app, px, py)) <= 18 
            and app.robberCoords != (px, py)):
            if (not knight or (app.curPlayer.cards['grain'] >= 1
                and app.curPlayer.cards['wool'] >= 1
                and app.curPlayer.cards['ore'] >= 1)):
                # enough resources
                if knight:
                    app.curPlayer.cards['grain'] -= 1
                    app.curPlayer.cards['wool'] -= 1
                    app.curPlayer.cards['ore'] -= 1

                app.robberCoords = (px, py)

                # next stage in starting phase
                if knight:
                    app.curPlayer.knights += 1
            else:
                # not enough resources
                updateMessages(app, 'Not enough resources to buy a knight')
            
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