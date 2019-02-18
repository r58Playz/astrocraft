from main import * # we need the blocktypes from the main program
import json
import os
from time import gmtime, strftime

class saveLoad(object):
    def __init__(self):
        # "tarnslate" the block texture tuples into readable words for saving
        saveLoad.coordDictSave = { str(main.GRASS):'GRASS', str(main.SAND):'SAND', str(main.BRICK):'BRICK', str(main.STONE):'STONE' }
        # "tarnslate" the words back into tuples for loading
        saveLoad.coordDictLoad = { 'GRASS':main.GRASS, 'SAND':main.SAND, 'BRICK':main.BRICK, 'STONE':main.STONE }
        
        saveLoad.saveGameFile = 'SAVE.FACTORIES'
        
    def printStuff(self, txt):
        toLog = strftime("%d-%m-%Y %H:%M:%S|", gmtime()) + str(txt) 
        log = open('LOG.FACTORIES','w')
        log.write(toLog)
        log.close()
    def hasSaveGame(self):
        if os.path.exists(saveLoad.saveGameFile):
            return True
        else:
            return False
    
    def loadWorld(self, model, saveFile):
        saveLoad.printStuff('start loading...') 
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
                model.add_block( tuple(json.loads(coords)), saveLoad.coordDictLoad[blockType], False )
        
        saveLoad.printStuff('loading completed')
        
    def saveWorld(self, model, saveFile):
        saveLoad.printStuff('start saving...')
        fh = open(saveFile, 'w')
        
        # build a string to save it in one action
        worldString = ''
        
        for block in model.world:
            # convert the block coords into json
            # convert with the translation dictionary the block type into a readable word
            worldString += json.dumps(block) + '=>' + saveLoad.coordDictSave[ str(model.world[block]) ] + '\n'

        fh.write(worldString)
        fh.close()
        saveLoad.printStuff('saving completed')
