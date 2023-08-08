from cmu_graphics import *
from utils.hexCoords import getHexCoords
from utils.messages import updateMessages


def setStatus(button, app):
    # if button.label == 'trade':
    #     print('im not gonna do this yet')
    # elif button.label == 'dv':
    #     print('im not gonna do this yet either')
    if button.label == 'road':
        app.gameState = 'build road'
    elif button.label == 'settlement':
        app.gameState = 'build settlement'
    elif button.label == 'city':
        app.gameState = 'build city'
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
            else:
                # not enough resources
                updateMessages(app, 'Not enough resources')
            
            app.gameState = 'player turn'
            return
    
    # not a valid placement
    updateMessages(app, 'Not a valid placement')

    # free means just started, so repeat the placement
    if free:
        app.stage -= 1


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
                updateMessages(app, 'Not enough resources')
            
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
            else:
                # not enough resources
                updateMessages(app, 'Not enough resources')
            
            app.gameState = 'player turn'
            return
    
    # not a valid placement
    updateMessages(app, 'Not a valid placement')

    # free means just started, so repeat the placement
    if free:
        app.stage -= 1


def moveRobber(app, mouseX, mouseY):
    for (px, py) in app.board.centers:
        if (distance(mouseX, mouseY, *getHexCoords(app, px, py)) <= 18 
            and app.robberCoords != (px, py)):
            app.robberCoords = (px, py)
            app.gameState = 'player turn'
            return

    # not a valid placement
    updateMessages(app, 'Not a valid placement')
