from cmu_graphics import *
from utils.hexCoords import getHexCoords
from utils.messages import updateMessages


def setStatus(button, app):
    if button.label == 'trade':
        print('im not gonna do this yet')
    elif button.label == 'dv':
        print('im not gonna do this yet either')
    elif button.label == 'road':
        app.gameState = 'build road'
    elif button.label == 'settlement':
        app.gameState = 'build settlement'
    elif button.label == 'city':
        app.gameState = 'build city'
    else:
        app.gameState = 'end turn'


def buildSettlement(app, mouseX, mouseY):
    # go through coords and check if enough resources to place a settlement
    for (px, py) in app.board.coords:
        if (distance(mouseX, mouseY, *getHexCoords(app, px, py)) <= 12
            and app.board.buildings[(px, py)] == None):
            resourcesNeeded = ['lumber', 'brick', 'wool', 'grain']

            # learned the all function from https://docs.python.org/3/library/functions.html#all
            if all(app.curPlayer.cards[r] >= 1 for r in resourcesNeeded):
                # enough resources
                for r in resourcesNeeded:
                    app.curPlayer.cards[r] -= 1
                
                app.board.buildings[(px, py)] = (1, app.curPlayer.color)
                updateMessages(app, f'Player {app.curPlayerID+1} built a settlement')
                return
            else:
                # not enough resources
                updateMessages(app, 'Not enough resources')
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
                return
            else:
                # not enough resources
                updateMessages(app, 'Not enough resources')
                return
    
    # not a valid placement
    updateMessages(app, 'Not a valid placement')

def buildRoad(app, mouseX, mouseY):
    # go through coords and check if enough resources to place a city
    for (px, py) in app.board.midpoints:
        if (distance(mouseX, mouseY, *getHexCoords(app, px, py)) <= 12
            and app.board.buildings[(px, py)] == None):
            if (app.curPlayer.cards['lumber'] >= 1
                and app.curPlayer.cards['brick'] >= 1):
                # enough resources
                app.curPlayer.cards['lumber'] -= 1
                app.curPlayer.cards['brick'] -= 1

                app.board.buildings[(px, py)] = ('r', app.curPlayer.color)
                updateMessages(app, f'Player {app.curPlayerID+1} built a road')
                return
            else:
                # not enough resources
                updateMessages(app, 'Not enough resources')
                return
    
    # not a valid placement
    updateMessages(app, 'Not a valid placement')
    