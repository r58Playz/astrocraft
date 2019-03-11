import log
import os
import sys
import time
def finishOff(success = False):
    if success == True:
        temp = open("unittests.log", 'a')
        temp.write("Tests finished successfully" + os.linesep)
        temp.write("__________________________________________________________" + os.linesep)
        temp.close()
        del temp
    else:
        temp = open("unittests.log", 'a')
        temp.write("Tests failed" + os.linesep)
        temp.write("__________________________________________________________" + os.linesep)
        temp.close()
        del temp

def runTests():
    LOG = log.Log("unittests.log")
    print("*************" + os.linesep + "RUNNING TESTS" + os.linesep + "*************" + os.linesep)
    time.sleep(1)
    print("Setting up tests")
    time.sleep(1)
    print(".")
    time.sleep(1)
    testSuccess = True
    print(".")
    time.sleep(1)
    temp = open("unittests.log", 'a')
    temp.write("______________________Test(of log)______________________" + os.linesep)
    temp.close()
    del temp
    time.sleep(1)
    print(".")
    print("Test 1: log a message of type 'ERROR'saying 'Game Crashed' in file 'unittests.log'" + os.linesep)
    time.sleep(1)
    try:
        LOG.log("Game Crashed", True, 'e')
        time.sleep(1)
        print("Test 1 is a success" + os.linesep)
    except:
        testSuccess = False
        time.sleep(1)
        print("Test 1 failed")
    time.sleep(1)
    print("Test 2: log a message of type 'NOTICE' saying 'Game started' in file 'unittests.log'" + os.linesep)
    time.sleep(1)
    if testSuccess == True:
        try:
            LOG.log("Game started", True, 'n')
            time.sleep(1)
            print("Test 2 is a success" + os.linesep)
        except:
            testSuccess = False
            time.sleep(1)
            print("Test 2 failed")
    else:
        finishOff()
        sys.exit("Test failed, exiting...")
    time.sleep(1)
    print("Test 3: log a message of type 'DEBUG' saying 'Game loaded' in file 'unittests.log'" + os.linesep)
    time.sleep(1)
    if testSuccess == True:
        try:
            LOG.log("Game loaded", True,'d')
            time.sleep(1)
            print("Test 3 is a success")
        except:
            testSuccess = False
            time.sleep(1)
            print("Test 3 failed")
    else:
        finishOff()
        sys.exit("Test 2 failed, exiting...")
    time.sleep(1)
    print("All tests finished successfully. Please open unittests.log for more info.")
    rF = str(input("Would you like to open unittests.log now?(y, n)"))
    if rF == 'y':
        openF = open("unittests.log", 'r')
        testinfo = openF.read()
        print("Here is the text in unittests.log:")
        print(testinfo)
        clrlg = str(input("Would yu likt to clear unittests.log?(y,n)"))
        if clrlg == 'y':
            openF.close()
            del openF
            openF = open("unittests.log", 'w')
            openF.write('')
            print("unittests.log successfully cleared.")
            openF.close()
            del openF
            pass
        else:
            pass
    else:
        pass
    print("*********************************************")
    print("Cleaning up tests")
    time.sleep(1)
    print(".")
    time.sleep(1)
    print(".")
    time.sleep(1)
    finishOff(True)
    time.sleep(1)
    print(".")
    time.sleep(1)
    print("***********************************************" + os.linesep + "Finished tests, stopping" + os.linesep + "***********************************************" + os.linesep)
if __name__ == "__main__":
    runTests()
