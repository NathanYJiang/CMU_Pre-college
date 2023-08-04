class Button:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def onClick(self, mouseX, mouseY):
        # not clicked, so return
        if not ((self.x <= mouseX <= self.x + self.width) 
            and (self.y <= mouseY <= self.y + self.height)): return
        
        
    
