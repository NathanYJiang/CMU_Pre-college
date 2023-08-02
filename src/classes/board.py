from utils.hexCoords import *
import random

class Board:
    def __init__(self):
        self.coords = set()
        self.centers = dict()
        self.midpoints = set()
        self.buildings = dict()

        # port coordinates (fixed points)
        self.ports = {
            (3, 2.5): None, 
            (7, 2.5): None, 
            (10, 1.5): None, 
            (12, -0.5): None, 
            (10, -2.5): None, 
            (7, -3.5): None, 
            (3, -3.5): None, 
            (1, -1.5): None, 
            (1, 0.5): None
        }

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

                # coords for settlements/cities
                self.coords.add((px, py))
                self.buildings[(px, py)] = None

                # center calculations for tiles/numbers
                if (((px % 2 == 1 and py % 2 == 1) 
                    or (px % 2 == 0 and py % 2 == 0)) 
                    and px + py > 0 and px - py < 11 and py > -3):
                    self.centers[(px, py - 0.5)] = None
        
        # midpoint calculations for roads
        for (px1, py1) in self.coords:
            for (px2, py2) in self.coords:
                px = (px1 + px2)/2
                py = (py1 + py2)/2
                if (distance(px1, py1, px2, py2) == 1 
                    and (px, py) not in self.centers):
                    self.midpoints.add(((px1 + px2)/2, (py1 + py2)/2))
                    self.buildings[(px, py)] = None
        
        # board setup (tiles/numbers)
        # tiles (19 with desert)
        self.tiles = (['desert'] + ['wheat'] * 4 + ['sheep'] * 4 + ['wood'] * 4 
                     + ['brick'] * 3 + ['ore'] * 3)

        # numbers (18 because no number on desert)
        self.numbers = [2]
        for i in range(3, 7):
            self.numbers += [i] * 2
        for i in range(8, 12):
            self.numbers += [i] * 2
        self.numbers += [12]

        for (px, py) in self.centers:
            tile = random.choice(self.tiles)
            self.tiles.remove(tile)
            if tile == 'desert':
                self.centers[(px, py)] = (tile, -1)
                continue

            number = random.choice(self.numbers)
            self.numbers.remove(number)

            self.centers[(px, py)] = (tile, number)

        for (px, py) in self.centers:
            print(self.centers[(px, py)][0], self.centers[(px, py)][1])

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
        