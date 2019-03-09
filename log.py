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
    def changeChatFile(self, chatFile):
        '''Changes chatfile to chatFile. Creates and tests chatfile if needed.
        
        Arguments:
            chatFile {String} -- Provided file. Provide pathway from this folder to file in this format:
                'foldername/optionalfolder/optionalfolder/file.txt'
        '''
        if os.path.exists(chatFile):
            self.chatF = chatFile
        else:
            # Otherwise makes the file then sets it.
            fle = open(chatFile, 'w')
            # Dummy writing for testing stream
            teststream = """
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla sollicitudin velit massa. Quisque eget augue ultrices, placerat dolor quis, interdum mi. In dignissim metus id rhoncus bibendum. Donec et urna dolor. Vestibulum nibh est, mollis sed massa ut, commodo vulputate nibh. Aenean feugiat malesuada magna, at tincidunt elit. Vivamus dignissim, elit varius venenatis molestie, lacus quam sodales mauris, et viverra massa lorem in velit. Vestibulum ac odio quis sapien viverra interdum quis vel sem. Nulla orci ipsum, molestie ac convallis a, condimentum vitae dui. Aenean sagittis interdum commodo.
Proin quam ante, semper eu consectetur a, vestibulum sit amet felis. Integer nec pharetra dolor. Maecenas quis ante id augue tristique fringilla. Nullam quis dolor vitae tortor aliquet aliquet. Etiam non nunc at quam gravida pharetra. Nulla lobortis, augue sed tempus egestas, justo elit consequat nisi, non ultricies turpis velit nec erat. Maecenas finibus lorem ac vulputate fermentum. Donec eget molestie turpis. Integer rhoncus nisi sem. Quisque bibendum, erat a blandit sodales, enim quam laoreet mi, vitae cursus urna quam vel felis.
Proin eu lacus in sem lacinia pretium a dapibus dui. Vivamus eget varius nunc. Duis lorem ligula, luctus id tempor a, fringilla quis nibh. Aliquam malesuada risus ut mollis gravida. Ut sit amet sollicitudin leo. Cras pulvinar lacus quis enim placerat, quis finibus neque dapibus. Nam lobortis aliquam viverra. Quisque ac posuere mi. Sed scelerisque ultricies mi, id pharetra nunc porta sed. Aenean justo risus, luctus ut pharetra eu, maximus quis leo. Pellentesque sodales justo porttitor ante imperdiet sollicitudin. Donec maximus pulvinar lorem, at rutrum ante luctus at. In quis nunc id neque hendrerit egestas. Donec consequat, nisi non interdum venenatis, nunc augue suscipit quam, in condimentum erat dui ut mi. 
            """
            # Tests stream
            fle.write(teststream)
            # Clears file
            fle.write('')
            fle.close()
            # Sets file
            self.chatF = chatFile
        return True
    def return_latest_chat(self):
        #this should process the latest line in the chat and return it as 3 variables, time, person, msg
        chatfile = self.chatF
        chat = open(chatfile, 'r')
        text = chat.read()
        #TODO Process and change the text
        #print is for now
        print(text)
        #dummy values
        time = "time"
        person = "person"
        msg = "msg"
        return time, person, msg
    def chat(self, pName, message):
        """Writes to chat file the person name, and message.
        
        Arguments:
            pName {String} -- Name of person who is chatting.
            message {String} -- Message of person who is chattting.
        """

        log = Log("LOG.FACTORIES")
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

if __name__ == "__main__":
    chatthingy = Chat("tmp.chat")
    chatthingy.chat("dudo","dudo")
    print("LATEST CHAT:")
    chatthingy.return_latest_chat()
    chatthingy.chat("dudo","meep you")
    print("LATEST CHAT:")
    chatthingy.return_latest_chat()
    del chatthingy