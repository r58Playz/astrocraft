from main import * # we need the blocktypes from the main program
import json
import os
from time import gmtime, strftime
from resources.log import Log

class saveModule(object):
    def __init__(self):
        # "tarnslate" the block texture tuples into readable words for saving
        self.coordDictSave = { str(main.GRASS):'GRASS', str(main.SAND):'SAND', str(main.BRICK):'BRICK', str(main.STONE):'STONE' }
        # "tarnslate" the words back into tuples for loading
        self.coordDictLoad = { 'GRASS':main.GRASS, 'SAND':main.SAND, 'BRICK':main.BRICK, 'STONE':main.STONE }
        
        self.saveGameFile = 'SAVE.FACTORIES'
        
    def printStuff(self, txt):
        log=Log("LOG.FACTORIES")
        log.log(txt, True, 'n')
    def hasSaveGame(self):
        if os.path.exists(self.saveGameFile):
            return True
        else:
            return False
    
    def loadWorld(self, model, saveFile):
        self.printStuff('start loading...')
        fh = open(saveFile, 'r')
        worldMod = fh.read()
        fh.close()
        
        worldMod = worldMod.split('\n')
        
        for blockLine in worldMod:
            # remove the last empty line
            if blockLine != '':
                coords, blockType = blockLine.split('=>')
                # convert the json list into tuple; json ONLY get lists but we need tuples
                # translate the readable word back into the texture coords
                model.add_block( tuple(json.loads(coords)), self.coordDictLoad[blockType], False )
        
        self.printStuff('loading completed')
        
    def saveWorld(self, model, saveFile):
        self.printStuff('start saving...')
        fh = open(saveFile, 'w')
        fh.write('')
        fh.close()
        fh = open(saveFile, 'a')
        
        for block in model.world:
            # convert the block coords into json
            # convert with the translation dictionary the block type into a readable word
            blockString = json.dumps(block) + '=>' + self.coordDictSave[ str(model.world[block]) ] + '\n'
            fh.write(blockString)

        fh.close()
        self.printStuff('saving completed')
