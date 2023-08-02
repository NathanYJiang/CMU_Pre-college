from PIL import Image, ImageOps
from cmu_graphics import CMUImage

# credit for number tokens goes to: https://catanworldexplorers.fandom.com/wiki/Settlement
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
    # border code modified from https://stackoverflow.com/questions/11142851/adding-borders-to-an-image-using-python 
    app.dice = dict()
    for i in range(1, 7):
        dice = Image.open(f'images/dice-{i}.png')
        diceWithBorder = ImageOps.expand(dice, border=10, fill='black')
        diceWithBorder.thumbnail((70, 70))
        app.dice[i] = CMUImage(diceWithBorder)


