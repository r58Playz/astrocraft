from apiRESOURCES import apiRes as apiRes
class FactoriesAPI(object):
    def __init__(self):
        print("Initialised api")
        self.apires = apiRes()
    
    def loadWorldFromArray(self, array):
        """Loads world from array.
        
        Arguments:
            array {List} -- [description]
        """