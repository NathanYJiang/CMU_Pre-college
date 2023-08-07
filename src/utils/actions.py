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
                for r in resourcesNeeded:
                    app.curPlayer.cards[r] -= 1
                
                app.board.buildings[(px, py)] = (1, app.curPlayer.color)
                break
            else:
                updateMessages(app, 'Not enough resources')
    
    # return to player turn
    app.gameState = 'player turn'

def buildCity(app, mouseX, mouseY):
    # go through coords and check if enough resources to place a city
    for (px, py) in app.board.coords:
        if (distance(mouseX, mouseY, *getHexCoords(app, px, py)) <= 12
            and app.board.buildings[(px, py)] == (1, app.curPlayer.color)):
            if (app.curPlayer.resources['grain'] >= 2 
                and app.curPlayer.resources['ore'] >= 3):
                app.curPlayer.resources['grain'] -= 2 
                app.curPlayer.resources['ore'] -= 3
    
    # return to player turn
    app.gameState = 'player turn'

def buildRoad(app, mouseX, mouseY):
    # go through coords and check if enough resources to place a city
    for (px, py) in app.board.midpoints:
        if (distance(mouseX, mouseY, *getHexCoords(app, px, py)) <= 12
            and app.board.buildings[(px, py)] == None):
            if (app.curPlayer.resources['lumber'] >= 1
                and app.curPlayer.resources['brick'] >= 1):
                app.curPlayer.resources['lumber'] -= 1
                app.curPlayer.resources['brick'] -= 1
    
    # return to player turn
    app.gameState = 'player turn'
        


    

