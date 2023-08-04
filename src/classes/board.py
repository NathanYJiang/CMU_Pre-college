from utils.hexCoords import getHexCoords, isHalf
from cmu_graphics import *
from math import floor, ceil
import random


class Board:
    def __init__(self):
        self.coords = set()
        self.centers = dict()
        self.midpoints = set()
        self.buildings = dict()
        self.tileToResource = {
            'forest': 'lumber',
            'hill': 'brick',
            'pasture': 'wool',
            'field': 'grain',
            'mountain': 'ore'
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
        self.tiles = (['desert'] + ['field'] * 4 + ['pasture'] * 4 + 
                      ['forest'] * 4 + ['hill'] * 3 + ['mountain'] * 3)

        # numbers (18 because no number on desert)
        self.numbers = [2]
        for i in range(3, 7):
            self.numbers += [i] * 2
        for i in range(8, 12):
            self.numbers += [i] * 2
        self.numbers += [12]

        # add a tile and number to each hexagon of the board
        for (px, py) in self.centers:
            tile = random.choice(self.tiles)
            self.tiles.remove(tile)
            if tile == 'desert':
                self.centers[(px, py)] = (tile, -1)
                self.robber = (px, py)
                continue

            number = random.choice(self.numbers)
            self.numbers.remove(number)

            self.centers[(px, py)] = (tile, number)

    def draw(self, app):
        # draw the surrounding water
        drawRect(0, 0, app.width, app.height, fill='lightBlue')

        self.drawTiles(app)
        self.drawGrid(app)
        self.drawBuildings(app)
    
    def drawTiles(self, app):
        for px, py in self.centers:
            (x, y) = getHexCoords(app, px, py)
            drawCircle(x, y, 5, fill='magenta')
            (tile, number) = self.centers[(px, py)]
            drawImage(app.tiles[tile], x, y, align='center')
            if number == -1:
                continue
            drawImage(app.tokens[number], x, y, align='center')
    
    def drawBuildings(self, app):
        for (px, py) in self.buildings:
            if self.buildings[(px, py)] != None:
                building, color = self.buildings[(px, py)]
                if building == 's':
                    self.drawSettlement(*getHexCoords(app, px, py), 
                                             fill=color)
                elif building == 'c':
                    self.drawCity(*getHexCoords(app, px, py), fill=color)
                else:
                    self.drawRoad(app, px, py, color)

    def drawGrid(self, app):
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
        # (not really necessary, just a safety check)
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
    
    def drawRoad(self, app, px, py, color):
        drawLine(*getHexCoords(app, floor(px), floor(py)), 
                 *getHexCoords(app, ceil(px), ceil(py)), 
                 fill=color, lineWidth=10)
        