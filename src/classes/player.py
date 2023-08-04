class Player:
    def __init__(self, app, number):
        self.color = app.colors[number - 1]
        self.cards = dict()
        
