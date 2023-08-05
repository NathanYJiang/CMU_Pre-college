from cmu_graphics import CMUImage
from PIL import Image, ImageFilter, ImageEnhance


# credit for number tokens goes to: https://catanworldexplorers.fandom.com/wiki/Settlement
# credit for dice images goes to: https://game-icons.net/1x1/delapouite/dice-six-faces-one.html
# credit for other images goes to: https://github.com/BryantCabrera/Settlers-of-Catan/tree/master/resources/imgs
# PIL sharpen learned from: https://pythonexamples.org/python-pillow-image-sharpen/
# used https://tinypng.com/ to minimize images

def getImages(app):
    # tokens
    app.tokens = dict()
    for i in range(2, 13):
        # 7 is the robber!
        if i == 7: continue
        token = Image.open(f'images/token{i}.webp')
        token.thumbnail((50, 50))
        token = token.filter(ImageFilter.SHARPEN)
        app.tokens[i] = CMUImage(token)
    
    # tiles
    app.tiles = dict()
    for resource in ['desert', 'field', 'pasture', 'forest', 'hill', 'mountain']:
        tile = Image.open(f'images/{resource}.png')
        tile.thumbnail((140, 140))
        app.tiles[resource] = CMUImage(tile)
    
    # dice
    app.dice = dict()
    for i in range(1, 7):
        dice = Image.open(f'images/dice{i}.png')
        dice.thumbnail((75, 75))
        app.dice[i] = CMUImage(dice)
    
    # player icon
    app.icons = []
    for i in range(app.numPlayers):
        icon = Image.open(f'images/p{i+1}icon.png')
        icon.thumbnail((60, 60))
        app.icons.append(CMUImage(icon))

    # resources
    app.resImages = dict()
    for resource in app.resources:
        resImage = Image.open(f'images/resources--{resource}.png')
        resImage.thumbnail((50, 80))
        #resImage = resImage.filter(ImageFilter.SHARPEN)
        app.resImages[resource] = CMUImage(resImage)


