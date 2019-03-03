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
        STONE = main.STONE
        GRASS = main.GRASS
        SAND = main.SAND
        BRICK = main.BRICK
        self.saveDict = { str(main.GRASS):'GRASS', str(main.SAND):'SAND', str(main.BRICK):'BRICK', str(main.STONE):'STONE' }
        model = main.Model()