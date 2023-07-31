from cmu_graphics import *
import math

def getHexCoords(app, px, py):
    if isWhole(px) and isWhole(py):
        px = int(px)
        py = int(py)
        x = app.startX
        y = app.startY

        # calculations using geometry
        x += px * (app.s * math.sqrt(3) / 2)
        y -= py * (app.s * 3 / 2)

        # if both even or if both odd, shift up
        if (py % 2 == 0 and px % 2 == 0) or (py % 2 == 1 and px % 2 == 1):
            y -= app.s * 1 / 2

        x = rounded(x)
        y = rounded(y)
        return x, y
    else:
        # if x is a .5, then avg the two
        if isHalf(px):
            x1, y1 = getHexCoords(app, math.floor(px), int(py))
            x2, y2 = getHexCoords(app, math.ceil(px), int(py))
            return (x1 + x2) / 2, (y1 + y2) / 2
        # if y is a .5, then avg the two
        if isHalf(py):
            x1, y1 = getHexCoords(app, px, math.floor(py))
            x2, y2 = getHexCoords(app, px, math.ceil(py))
            return (x1 + x2) / 2, (y1 + y2) / 2


# check if x has a 0.5
def isHalf(x):
    return almostEqual(x % 1, 0.5)


# check if x is whole
def isWhole(x):
    return almostEqual(x % 1, 0)