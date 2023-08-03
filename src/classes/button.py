class Button:
    def __init__(self, x, y, length, height):
        self.x = x
        self.y = y
        self.length = length
        self.height = height

    def isClicked(self, mouseX, mouseY):
        return ((self.x <= mouseX <= self.x + self.length) 
            and (self.y <= mouseY <= self.y + self.height))
    