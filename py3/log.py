import os
from time import strftime, gmtime
class Log(object):
    def __init__(self, lf):
        self.logF = lf
    def setLogFile(self, file):
        self.logFile = file
    def log(self,text, newline = True, tpeoflg = 'o', prefix = ''):
        logFile = self.logF
        '''
        This function logs the text you give in a file, with a "ERROR|", "NOTICE|", or custom prefix.
        __________
        Arguments
        __________
        text : string - the text you want to log    
        newline: boolean - if you want this log to be seperated with a newline, set this to true. 
        Example(newline = true):
        NOTICE| test
        test| This is great!!
        Example:(newline = false)
        NOTICE| testtest| This is great!!
        tpeoflg : boolean - Type of log you want. Options: 'e' = error, 'n' = notice, 'd' = debug, 'o' = none 'c' = customprefix
        customPrefix : boolean - if this is true, the prefix you give in the next argument will be added with
        a "| ". Automatically defaults to false
        prefix : string - the prefix you want to give. Automatically defaults to ''
        logFile : string - the filename, with extension, you want to save the message to. Automatically defaults
        to 'log.log'.
        factoriesToggle: overrides the filename to "LOG.FACTORIES" Automatically defaults to false.
        '''
        time = strftime("%m-%d-%Y %H:%M:%S|", gmtime())
        if newline == True:
            packup = os.linesep
            if tpeoflg == 'e':
                log = open(logFile, 'a')
                logtxt = time + "ERROR| " + text
                log.write(logtxt)
                log.write(packup)
                log.close()
            elif tpeoflg == 'n':
                log = open(logFile, 'a')
                logtxt = time + "NOTICE| " + text
                log.write(logtxt)
                log.write(packup)
                log.close()
            elif tpeoflg == 'd':
                log = open(logFile, 'a')
                logtxt = time + "DEBUG| " + text
                log.write(logtxt)
                log.write(packup)
                log.close()
            elif tpeoflg == 'o':
                log = open(logFile, 'a')
                logtxt = time + ' ' + text
                log.write(logtxt)
                log.write(packup)
                log.close()
            elif tpeoflg == 'p':
                log = open(logFile, 'a')
                logtxt = time + prefix + "| " + text
                log.write(logtxt)
                log.write(packup)
                log.close()
            else:
                #This code below, in this else block, is for handling letters other than e, n, d, o.
                log = open(logFile, 'a')
                logtxt = time + "ERROR| " + " Wrong parameter passed: " + tpeoflg + " from e, n, d, o. Will default to notice."
                log.write(logtxt)
                log.write(packup)
                logttxt = time + "NOTICE|" + text
                log.write(logttxt)
                log.write(packup)
                log.close()                              
        else:
            if tpeoflg == 'e':
                log = open(logFile, 'a')
                log.write(logtxt)
                log.close()
            elif tpeoflg == 'n':
                log = open(logFile, 'a')
                logtxt = time + "NOTICE| " + text
                log.write(logtxt)
                log.close()
            elif tpeoflg == 'd':
                log.open(logFile, 'a')
                logtxt = time + "DEBUG|" + text
                log.write(logtxt)
                log.close()
            else:
                log = open(logFile, 'a')
                logtxt = time + prefix + "| " + text
                log.write(logtxt)
                log.close()

class Chat(object):
    def __init__(self, chatFile):
        self.chatF = chatFile

    def startChat(self):
        log = Log("log.log")
        UNDIES = "_" * 10
        ender = os.linesep
        chatFile = self.chatF
        chat = open(chatFile, 'a')
        time = strftime("%m-%d-%Y %H:%M:%S")
        chat.write(UNDIES + time + UNDIES + ender)
        chat.close()
        log.log("Chat successfully started", True, 'n')
        print(time + "|" + "Chat successfully started")
    
    def endChat(self):
        """
        Ends chat.
        A possible use is when the program is exiting.
        Parameters - none
        """
        log = Log("log.log")
        ender = os.linesep
        UNDIES = "_" * 10 #Essentially multiplies "_" 10 times. UNDIES == "__________"
        chatFile = self.chatF
        time = strftime("%m-%d-%Y %H:%M:%S")
        chat = open(chatFile, 'a')
        chat.write(UNDIES * 4)
        chat.write(ender)
        chat.close()
        log.log("Chat successfully ended", True, 'n')
        print(time + "|" + "Chat successfully ended")
    
    def chat(self, pName, message):
        log = Log("log.log")
        ender = os.linesep
        person = pName + " |"
        time = strftime("%m-%d-%Y %H:%M:%S|")
        chat = open(self.chatF, 'a')
        formattedChat = time + person + message
        chat.write(formattedChat)
        chat.write(ender)
        chat.close()
        log.log("Chat successfully ended", True, 'n')
        print(time + "|" + "Wrote message to chat with person name " + pName + " with message '" + message + "'")