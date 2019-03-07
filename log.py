import os
from time import strftime, gmtime
class Log(object):
    def __init__(self, lf):
        """Initializes the log object.
        
        Arguments:
            object {Object} -- Nessesary for code to function.
            lf {String} -- filename to save log to(optionally path to file)
        
        Example:
            file = "log.log" # Means that log.log is in current folder.
            file = "logs/log1.log" # Means that log1.log is in folder logs which is in current folder.
        """

        self.logF = lf
    def setLogFile(self, file):
        """Sets the log file to file.
        
        Arguments:
            file {String} -- filename(optionally pathway to file)
        
        Example:
            file = "log.log" # Means that log.log is in current folder.
            file = "logs/log1.log" # Means that log1.log is in folder logs which is in current folder.
        """

        self.logFile = file
    def log(self,text, newline = True, tpeoflg = 'o', prefix = ''):
        """Logs a message(text) with newline(newline) with type(tpeoflg), or a custom prefix(prefix).
        
        Arguments:
            text {String} -- The text to log
        
        Keyword Arguments:
            newline {Boolean} -- Whether or not to put a new line after the message (default: {True})
            tpeoflg {character} -- The type of the log. (default: {'o'})
            prefix {String} -- The prefix to use if you choose to use a custom prefix. (default: {''})
        
        Choices:
            tpeoflg:
                'e' = error
                'n' = notice
                'd' = debug
                'o' = none
                'p' = prefix
        """

        logFile = self.logF
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
        """Initializes chatfile
        
        Arguments:
            chatFile {String} -- the chatfile to save to
        """
        self.chatF = chatFile

    def startChat(self):
        """Starts the chat.
        """

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
        return 1
    
    def endChat(self):
        """Ends the chat.
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
        return 1
    
    def chat(self, pName, message):
        """Writes to chat file the person name, and message.
        
        Arguments:
            pName {String} -- Name of person who is chatting.
            message {String} -- Message of person who is chattting.
        """

        log = Log("log.log")
        ender = os.linesep
        fmessage = message + "'"
        person = pName + " said '"
        time = strftime("%m-%d-%Y %H:%M:%S|")
        chat = open(self.chatF, 'a')
        formattedChat = time + person + fmessage
        chat.write(formattedChat)
        chat.write(ender)
        chat.close()
        log.log("Wrote message to chat with person name " + pName + "with message '" + message + "'", True, 'n')
        print(time + "|" + "Wrote message to chat with person name " + pName + " with message '" + message + "'")