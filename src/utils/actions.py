from cmu_graphics import *

def action(button, app):
    if app.gameState == 'player turn':
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
            app.gameState = 'end'
    else:
        pass



    

