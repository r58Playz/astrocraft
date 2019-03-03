from apires import apiRes as apiRes
class FactoriesAPI(object):
    def __init__(self):
        print("Initialised api")
        self.apires = apiRes()
    
    def makeFlatWorld(self):
        print("This is going to make a flat world with grass as the first layer, and stone as the bottom layer.")
        filename = raw_input("File name to save to with pathway from base folder(not needed) and extension: ")
        save = open(filename, 'w')
        save.write(self.apires.flatWorld)
        save.close()
        print("Done")
    
    def makeHillyWorldwithHouse(self):
        print("This is going to make a hilly world with a house.")
        filename = raw_input("File name to save to with pathway from base folder(not needed) and extension: ")
        save = open(filename, 'w')
        save.write(self.apires.houseandhillsWorld)
        save.close()
        print("Done")

if __name__ == "__main__":
    api = FactoriesAPI()
    api.makeHillyWorldwithHouse()