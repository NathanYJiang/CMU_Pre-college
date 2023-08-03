from PIL import Image
from cmu_graphics import CMUImage


# credit for number tokens goes to: https://catanworldexplorers.fandom.com/wiki/Settlement
# credit for dice images goes to: https://game-icons.net/1x1/delapouite/dice-six-faces-one.html
# credit for other images goes to: https://github.com/BryantCabrera/Settlers-of-Catan/tree/master/resources/imgs
def getImages(app):
    # tokens
    app.tokens = dict()
    for i in range(2, 13):
        # 7 is the robber!
        if i == 7: continue
        token = Image.open(f'images/token{i}.webp')
        token.thumbnail((50, 50))
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
        dice.thumbnail((70, 70))
        app.dice[i] = CMUImage(dice)
    
    # player icon
    app.icons = dict()
    for i in range(1, app.numPlayers + 1):
        icon = Image.open(f'images/p{i}icon.png')
        icon.thumbnail((60, 60))
        app.icons[i] = CMUImage(icon)


