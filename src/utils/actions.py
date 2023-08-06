from cmu_graphics import *

def action(button, app):
    app.gameState = button.label

    if button.label == 'trade':
        print('im not gonna do this yet')
    elif button.label == 'dv':
        print('im not gonna do this yet either')
    elif button.label == 'road':
        buildRoad(button, app)

    

