import os
class Log(object):
    '''
    This function logs the text you give in a file, with a "ERROR|", "NOTICE|", or custom prefix.
    _________________________
    Arguments
    _________________________
    text : string - the text you want to log    
    newline: boolean - if you want this log to be seperated with a newline, set this to true. 
    Example(newline = true):
    NOTICE| test
    test| This is great!!
    Example:(newline = false)
    NOTICE| testtest| This is great!!
    tpeoflg : boolean - Type of log you want. Options: 'e' = error, 'n' = notice, 'd' = debug, 'o' = none, 'oo' = nothing
    customPrefix : boolean - if this is true, the prefix you give in the next argument will be added with
    a "| ". Automatically defaults to false
    prefix : string - the prefix you want to give. Automatically defaults to ''
    logFile : string - the filename, with extension, you want to save the message to. Automatically defaults
    to 'log.log'.
    factoriesToggle: overrides the filename to "LOG.FACTORIES" Automatically defaults to false.

    '''
    def log(self,text, newline = True, tpeoflg = 'o', customPrefix = False, prefix = '', logFile = "log.log", factoriesToggle = False):
        if newline == True:
            packup = os.linesep
            if factoriesToggle == False:
                if customPrefix == False:
                    if tpeoflg == 'e':
                        log = open(logFile, 'a')
                        logtxt = "ERROR| " + text
                        log.write(logtxt)
                        log.write(packup)
                        log.close()
                    elif tpeoflg == 'n':
                        log = open(logFile, 'a')
                        logtxt = "NOTICE| " + text
                        log.write(logtxt)
                        log.write(packup)
                        log.close()
                    elif tpeoflg == 'd':
                        log = open(logFile, 'a')
                        logtxt = "DEBUG| " + text
                        log.write(logtxt)
                        log.write(packup)
                        log.close()
                    elif tpeoflg == 'o':
                        log = open(logFile, 'a')
                        logtxt = text
                        log.write(logtxt)
                        log.write(packup)
                        log.close()
                    elif tpeoflg == 'oo':
                        pass
                else:
                    log = open(logFile, 'a')
                    logtxt = prefix + "| " + text
                    log.write(logtxt)
                    log.write(packup)
                    log.close()
            else:
                logFile = "LOG.FACTORIES"
                if customPrefix == False:
                    if tpeoflg == 'e':
                        log = open(logFile, 'a')
                        logtxt = "ERROR| " + text
                        log.write(logtxt)
                        log.write(packup)
                        log.close()
                    elif tpeoflg == 'n':
                        log = open(logFile, 'a')
                        logtxt = "NOTICE| " + text
                        log.write(logtxt)
                        log.write(packup)
                        log.close()
                    elif tpeoflg == 'd':
                        log = open(logFile, 'a')
                        logtxt = "DEBUG|" + text
                        log.write(logtxt)
                        log.write(packup)
                        log.close()
                else:
                    log = open(logFile, 'a')
                    logtxt = prefix + "| " + text
                    log.write(logtxt)
                    log.write(packup)
                    log.close()
        else:
            if factoriesToggle == False:
                if customPrefix == False:
                    if tpeoflg == False:
                        log = open(logFile, 'a')
                        logtxt = "ERROR| " + text
                        log.write(logtxt)
                        log.close()
                    else:
                        log = open(logFile, 'a')
                        logtxt = "NOTICE| " + text
                        log.write(logtxt)
                        log.close()
                else:
                    log = open(logFile, 'a')
                    logtxt = prefix + "| " + text
                    log.write(logtxt)
                    log.close()
            else:
                logFile = "LOG.FACTORIES"
                packup = os.linesep
                if factoriesToggle == False:
                    if customPrefix == False:
                        if tpeoflg == 'e':
                            log = open(logFile, 'a')
                            logtxt = "ERROR| " + text
                            log.write(logtxt)
                            log.close()
                        elif tpeoflg == 'n':
                            log = open(logFile, 'a')
                            logtxt = "NOTICE| " + text
                            log.write(logtxt)
                            log.close()
                        elif tpeoflg == 'd':
                            log = open(logFile, 'a')
                            logtxt = "DEBUG| " + text
                            log.write(logtxt)
                            log.close()
                        elif tpeoflg == 'o':
                            log = open(logFile, 'a')
                            logtxt = text
                            log.write(logtxt)
                            log.close()
                        elif tpeoflg == 'oo':
                            pass
                else:
                    log = open(logFile, 'a')
                    logtxt = prefix + "| " + text
                    log.write(logtxt)
                    log.close()
