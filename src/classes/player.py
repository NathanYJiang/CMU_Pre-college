from math import floor


class Player:
    def __init__(self, app, index):
        self.number = index + 1
        self.color = app.colors[index]
        self.cards = dict()
        self.vp = 0
        for resource in app.resources:
            self.cards[resource] = 4
    
    def getResources(self, app):
        for (px, py) in app.board.centers:
            # robber is blocking this hex
            if (px, py) == app.robberCoords: continue

            # distribute resources to surrounding settlements/cities
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
