from math import floor

class Player:
    def __init__(self, app, index):
        self.number = index + 1
        self.color = app.colors[index]
        self.cards = dict()
        for resource in app.resources:
            self.cards[resource] = 0
    
    def getResources(self, app):
        for (px, py) in app.board.centers:
            tile, number = app.board.centers[(px, py)]
            if number == app.roll:
                for dx in range(-1, 2):
                    for dy in range(0, 2):
                        if app.board.buildings[(px + dx, floor(py) + dy)] == None:
                            continue

                        building, color = app.board.buildings[(px + dx, 
                                                               floor(py) + dy)]
                        if color == self.color:
                            self.cards[app.tileToRes[tile]] += building

    def makeBuilding(self, app, px, py, building):
        app.board.buildings[(px, py)] = (building, self.color)
