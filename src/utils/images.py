import os
import pathlib
from cmu_graphics import CMUImage
from PIL import Image, ImageFilter

# credit for number tokens goes to: https://catanworldexplorers.fandom.com/wiki/Settlement
# credit for dice images goes to: https://game-icons.net/1x1/delapouite/dice-six-faces-one.html
# credit for end turn image goes to: https://www.pngmart.com/image/tag/fast-forward
# credit for trade icon goes to: https://www.flaticon.com/free-icon/swap_3466554
# credit for background goes to: https://catanuniverse.com/en/media/
# credit for other images goes to: https://github.com/BryantCabrera/Settlers-of-Catan/tree/master/resources/imgs
# used https://tinypng.com/ to minimize images
# PIL sharpen learned from: https://pythonexamples.org/python-pillow-image-sharpen/

# from Ray's cmu_graphics demo
def getImagePath(imageName):
    return os.path.join(pathlib.Path(__file__).parent, f"../images/{imageName}")

def getImages(app):
    # tokens
    app.tokens = dict()
    for i in range(2, 13):
        # 7 is the robber!
        if i == 7: continue
        
        token = Image.open(getImagePath(f'token{i}.webp'))
        app.tokens[i] = processImage(token, (50, 50))
    
    # tiles
    app.tiles = dict()
    for resource in ['desert', 'field', 'pasture', 'forest', 'hill', 'mountain']:
        tile = Image.open(getImagePath(f'{resource}.png'))
        app.tiles[resource] = processImage(tile, (140, 140))
    
    # dice
    app.dice = dict()
    for i in range(1, 7):
        dice = Image.open(getImagePath(f'dice{i}.png'))
        app.dice[i] = processImage(dice, (75, 75))
    
    # player icon
    app.icons = []
    for i in range(app.numPlayers):
        icon = Image.open(getImagePath(f'p{i+1}icon.png'))
        app.icons.append(processImage(icon, (60, 60)))

    # resources
    app.resImages = dict()
    for resource in app.resources:
        resImage = Image.open(getImagePath(f'resources--{resource}.png'))
        app.resImages[resource] = processImage(resImage, (50, 80))
    
    # robber and small robber (for button icon)
    robber = Image.open(getImagePath('robber.png'))
    app.robber = processImage(robber, (40, 40))
    app.smallRobber = processImage(robber, (30, 30))

    # end turn
    endturn = Image.open(getImagePath('endturn.png'))
    app.endturn = processImage(endturn, (30, 30))

    # building costs
    app.buildCost = []
    for i in range(len(app.players)):
        buildCost = Image.open(getImagePath(f'p{i+1}BuildingCosts.png'))
        app.buildCost.append(processImage(buildCost, (350, 350)))

    # trade
    trade = Image.open(getImagePath('trade.png'))
    app.trade = processImage(trade, (40, 40))

    # start screen
    # logo
    logo = Image.open(getImagePath('ketanlogo.png'))
    app.logo = processImage(logo, (1200, 120))

    # background
    setting = Image.open(getImagePath('ketanbackground.png'))
    app.setting = processImage(setting, (2000, 850))


def processImage(image, size):
    # converts, resizes, and then sharpens an image
    image = image.convert('RGBA')
    image.thumbnail(size)
    image = image.filter(ImageFilter.SHARPEN)
    return CMUImage(image)