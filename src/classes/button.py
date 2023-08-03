class Button:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def isClicked(self, mouseX, mouseY):
        return ((self.x <= mouseX <= self.x + self.width) 
            and (self.y <= mouseY <= self.y + self.height))
    
    def onClick(self):
        pass