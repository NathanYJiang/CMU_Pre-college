from math import floor, ceil

class Player:
    def __init__(self, app, number):
        self.color = app.colors[number - 1]
        self.cards = dict()
        for resource in app.resources:
            self.cards[resource] = 0
    
    def getResources(self, app, px, py):
        if app.board.buildings(px, py)

        
    def makeBuilding(self, app, px, py, building):
        app.board.buildings[(px, py)] = (building, self.color)
