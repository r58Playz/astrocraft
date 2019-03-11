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
    def _process_line(self, line, delim1, delim2):
        """Processes a line given as line, and returns it. Meant to be a private function.
        
        Arguments:
            line {String} -- The line wished to process. Must be of one line.
            delim1 {String} -- Delimiter 1. Include any spaces wished to be removed along with the delimiter.
            delim2 {String} -- Delimiter 2. Include any spaces wished to be removed along with the delimiter.
        """
        step1 = line.split(delim1)
        tmp = step1[1]
        step1.append(tmp.split(delim2)[1])
        del step1[1]
        step1.append(tmp.split(delim2)[0])
        # delibrately flipped since the person's name is at index 2, not index 1
        line_processed = [step1[0],step1[2],step1[1].rstrip()]
        return line_processed

    def return_latest_chat(self):
        """Gets the last line(the latest line) from the chatfile and returns it as 3 variables
        
        Returns:
            String -- 3 variables which represent time, person, msg
        """

        chatfile = self.chatF
        chat = open(chatfile, 'r')
        lines = chat.readlines()
        last = lines[-1]
        last = last.rstrip()
        if last == "No chat...":
            person = ''
            msg = ''
            return last, person,msg
        else:
            delim1 = "|"
            delim2 = " wrote: "
            processed_line = self._process_line(last,delim1,delim2)
            # need to put on different lines because otherwise:
            # ValueError: too many values to unpack
            time = processed_line[0]
            person = processed_line[1]
            msg = processed_line[2]
            return time, person, msg
    def format_for_chatlabel(self):
        """Formats for chatlabel in main.py
        """
        time, person, msg = self.return_latest_chat()
        if msg != '':
            output = time + ": " + person + " said '" + msg + "'"
            return output
        else:
            return time



    def clearChat(self):
        """Clears the chat.
        """

        chatfile = self.chatF
        chat = open(chatfile, 'w')
        # Writes an empty string, essentially clearing the file.
        chat.write('')
        chat.close()
        # NO GARBAGE LEFT!
        del chat
        del chatfile
    
    def chat(self, pName, message):
        """Writes to chat file the person name, and message.
        
        Arguments:
            pName {String} -- Name of person who is chatting.
            message {String} -- Message of person who is chattting.
        """

        log = Log("LOG.FACTORIES")
        ender = os.linesep
        person = pName + " wrote: "
        time = strftime("%m-%d-%Y %H:%M:%S|")
        chat = open(self.chatF, 'a')
        formattedChat = time + person + message
        chat.write(formattedChat)
        chat.write(ender)
        chat.close()
        log.log("Wrote message to chat with person name " + pName + "with message '" + message + "'", True, 'n')
        print(time + "|" + "Wrote message to chat with person name " + pName + " with message '" + message + "'")

if __name__ == "__main__":
    chatthingy = Chat("tmp.chat")
    chatthingy.chat("dudo","dudo")
    print("LATEST CHAT:")
    time,person,message = chatthingy.return_latest_chat()
    print("At " + time + ", " + person + " said,'" + message + "'")
    chatthingy.chat("dudo","meep you")
    print("LATEST CHAT:")
    time,person,message = chatthingy.return_latest_chat()
    print("At " + time + ", " + person + " said,'" + message + "'")
    del chatthingy