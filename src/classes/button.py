from cmu_graphics import *
from utils.actions import setStatus


class Button:
    def __init__(self, x, y, label, res=False):
        self.x = x
        self.y = y
        self.res = res
        if res:
            self.width = 50
            self.height = 73
        else:
            self.width = 70
            self.height = 70
        self.label = label

    def draw(self, app):
        drawRect(self.x, self.y, self.width, self.height, 
                 fill='white', border='black')
        
        x, y = self.x + self.width/2, self.y + self.height/2
        drawLabel(self.label, x, y-18)
        if self.label == 'road':
            drawLine(x-25, y+10, x+25, y+10, fill=app.curPlayer.color, lineWidth=10)
        elif self.label == 'settlement':
            app.board.drawSettlement(x, y+12, app.curPlayer.color)
        elif self.label == 'city':
            app.board.drawCity(x, y+14, app.curPlayer.color)
        elif self.label == 'end':
            drawImage(app.endturn, x+2, y+9, align='center')
        elif self.label == 'knight':
            drawImage(app.smallRobber, x, y+10, align='center')

    def onClick(self, mouseX, mouseY):
        # not clicked, so return
        if not ((self.x <= mouseX <= self.x + self.width) 
                and (self.y <= mouseY <= self.y + self.height)): return False
        
        if not self.res:
            setStatus(self, app)
            
        return True
    