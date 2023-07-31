from utils.hexCoords import *

class Board:
    def __init__(self):
        self.coords = set()

        # calculate all coords
        for py in range(-3, 3):
            for px in range(1, 12):
                # ignore top left
                if py >= 1 and px == 1: continue
                if py >= 2 and px == 2: continue

                # ignore top right
                if py >= 2 and px == 10: continue
                if py >= 1 and px == 11: continue

                # ignore bottom left
                if py <= -2 and px == 1: continue
                if py <= -3 and px == 2: continue

                # ignore bottom right
                if py <= -3 and px == 10: continue
                if py <= -2 and px == 11: continue

                self.coords.add((px, py))

    def draw(self, app):
        self.drawGrid(app)
        self.drawCells(app)

    def drawCells(self, app):
        for i in range(4, 9, 2):
            pass

    def drawGrid(self, app):
        # draw the surrounding water
        drawRect(0, 0, app.width, app.height, fill='lightBlue')

        # draw the grid
        for (px, py) in self.coords:
            # draw land connecting the hexagons
            # horizontal lines
            if px + py < 11 and px - py < 12:
                self.drawLand(app, px, py, px+1, py)

            # vertical lines
            if px % 2 == 1 and py % 2 == 1 and py < 2:
                self.drawLand(app, px, py, px, py+1)
            
            if px % 2 == 0 and py % 2 == 0 and py < 2:
                self.drawLand(app, px, py, px, py+1)
        
        for (px, py) in self.coords:
            # draw points
            self.drawDot(app, px, py)
    
    def drawLand(self, app, x1, y1, x2, y2):
        # dont allow coords with both x and y as .5
        if (isHalf(x1) and isHalf(y1)) or isHalf(x2) and isHalf(y2):
            return
        
        # make the midpoints red
        coords1 = getHexCoords(app, x1, y1)
        coords2 = getHexCoords(app, x2, y2)
        drawCircle(*coords1, 5, fill='tan')
        drawCircle(*coords2, 5, fill='tan')
        drawLine(*coords1, *coords2, fill='tan', lineWidth=10)

    def drawDot(self, app, x, y):
        # dont allow coords with both x and y as .5
        if isHalf(x) and isHalf(y):
            return

        # make the midpoints red
        fill = 'red' if isHalf(x) or isHalf(y) else 'black'
        coords = getHexCoords(app, x, y)
        drawCircle(*coords, 3, fill=fill)
        drawLabel(f'({x},{y})', coords[0], coords[1] + 8, size=8)

    # used this tool for drawSettlement and drawCity to calculate 
    # what the center of the settlement/city should be
    # https://www.omnicalculator.com/math/centroid

    def drawSettlement(self, x, y, fill):
        # center of the settlement if (x, y) was (0, 0)
        cx, cy = 12, 13.65

        # relative (x, y) to the center
        rx, ry = x - cx, y - cy

        drawPolygon(rx+12, ry, rx, ry+7, rx, ry+24, rx+24, ry+24, 
                    rx+24, ry+7, fill=fill, border='black')

    def drawCity(self, x, y, fill):
        # center of the city if (x, y) was (0, 0)
        cx, cy = 12.682, 18.49

        # relative (x, y) to the center
        rx, ry = x - cx, y - cy

        drawPolygon(rx+8, ry, rx, ry+6, rx, ry+30, rx+30, ry+30, rx+30, ry+16, 
                    rx+16, ry+16, rx+16, ry+6, fill=fill, border='black')
        