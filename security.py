import re

class NumCodeMessageSecurity(object):
    def __init__(self):
        #TODO check for config, if there get settings else configure
        print("")
        self.numcode_encryptkey = {"A":1,"B":2,"C":3,"D":4,"E":5,"F":6,"G":7,"H":8,"I":9,"J":10,"K":11,"L":12,"M":13,"N":14,"O":15,"P":16,"Q":17,"R":18,"S":19,"T":20,"U":21,"V":22,"W":23,"X":24,"Y":25,"Z":26}
        self.regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
    
    def encrypt(self, message):
        messagearr = list(message)
        encryptedarr = []
        encryptedstr = ""
        for letter in messagearr:
            ltr = letter
            try:
                ltr = int(ltr)
                encryptedarr.append(str(ltr))
            except:
                # check for special characters
                if self.regex.search(ltr) != None:
                    encryptedarr.append(ltr)
                else:
                    if ltr != " ":
                        ltr = ltr.upper()
                        numofltr = self.numcode_encryptkey[ltr]
                        strnumofltr = str(numofltr)
                        encryptedarr.append(strnumofltr)
                    else:
                        encryptedarr.append(ltr)
        for i in encryptedarr:
            encryptedstr = encryptedstr + encryptedarr[i]
            encryptedstr = encryptedstr + " "
        
        return encryptedstr
