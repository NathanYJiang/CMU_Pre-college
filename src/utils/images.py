from PIL import Image
from cmu_graphics import CMUImage

# credit for number tokens goes to: https://catanworldexplorers.fandom.com/wiki/Settlement
# credit for other images goes to: https://github.com/BryantCabrera/Settlers-of-Catan/tree/master/resources/imgs
def getImage(app):
    # tokens
    app.tokens = []
    for i in range(2, 13):
        # 7 is the robber!
        if i == 7: continue
        tile = Image.open(f'images/token{i}.webp')
        tile.thumbnail((50, 50))
        app.tokens.append(CMUImage(tile))
    
    app.resources = []
    for i in range(2, 13):
        # 7 is the robber!
        if i == 7: continue
        tile = Image.open(f'images/token{i}.webp')
        tile.thumbnail((50, 50))
        app.tokens.append(CMUImage(tile))

