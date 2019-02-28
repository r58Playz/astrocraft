import main
import saveModule
class fs(object):
    #Block constants
    STONE = main.STONE
    GRASS = main.GRASS
    SAND = main.SAND
    BRICK = main.BRICK
    model = main.Model()
    def __init__(self):
        print("Initialised api")

if __name__ == "__main__":
    api = fs()
    api.makeFlatWorldSave()