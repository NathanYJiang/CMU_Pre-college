from cmu_graphics import *
from utils.actions import action

class Button:
    def __init__(self, x, y, label):
        self.x = x
        self.y = y
        self.width = 70
        self.height = 70
        self.label = label

    def draw(self, app):
        drawRect(self.x, self.y, self.width, self.height, 
                 fill='white', border='black')
        drawLabel(self.label, self.x+self.width/2, self.y+self.height/2)

    def buttonPressed(self, mouseX, mouseY):
        # not clicked, so return
        if not ((self.x <= mouseX <= self.x + self.width) 
            and (self.y <= mouseY <= self.y + self.height)): return
        
        action(self, app)
        

        

    
