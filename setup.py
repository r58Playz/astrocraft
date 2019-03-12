#Factories v0.0.4
#SETUP FILE
#This file generates all the files needed if not there,
#prints progress, and logs it.
#SETUP FILE v0.0.1
from log import Log
import os
#Log instance for logging
log = Log("SETUP.log")
#____________________________________
print("STARTING SETUP...")
log.log("Starting setup...", True, 'o')
def check_texture_is_here():
    print("Checking if file 'texture.png' is here...")
    log.log("Checking if file'texture.png' is here...", True, 'n')
    if os.path.exists("texture.png"):
        print("'texture.png' is here.")
        log.log("'texture.png' is here.")
    else:
        if os.path.exists('tex'):
            print("'texture.png' not found, but fallback file 'tex' found.Restoring 'texture.png'... ")
            log.log("'texture.png' not found, but fallback file 'tex' found.Restoring 'texture.png'...", True, 'e')
            tex = open("tex", 'r')
            texture = tex.read()
            tex.close()
            del tex
            tex = open("texture.png", 'w')
            tex.write(texture)
            tex.close()
            del tex
            del texture
        else:
            print("'texture.png' not found, fallback file 'tex' not found. Using fallback variable tex to restore...")
            log.log("'texture.png' not found, fallback file 'tex' not found. Using fallback variable tex to restore...", True
                ,'e')
            texture = open("texture.png", 'w')
            texture.write(tex)
            tex.close()
    print("Texture is present")
    log.log("Texture is present", True, 'n')
def run_tests():
    tests.runTests()
def setup():
    check_texture_is_here()
    run_tests()
if __name__ == "__main__":
    setup()