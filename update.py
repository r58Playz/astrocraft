# Python packages
import shutil
import os
import zipfile
import urllib.request
from io import BytesIO

# Third-party libraries
# Nothing for now...

# Modules from this project
import globals as G

def update():
    updatezip = urllib.request.urlopen(G.UPDATE_URL)
    zipref = zipfile.ZipFile(BytesIO(updatezip.read()))
    zipref.extractall(G.UPDATE_DIR)
    zipref.close()
    files=os.listdir(G.UPDATE_DIR)
    for fle in files:
        full_filename = os.path.join(G.UPDATE_DIR, fle)
        if os.path.isfile(full_filename):
            if file != "update.py":
                current_dir=os.path.basename(os.getcwd())
                shutil.copy(full_filename, current_dir)
     shutil.rmtree(G.UPDATE_DIR)
     import main # Wonder what happens if you put this at the top? A TRACEBACK!
     main.start()# Should work...
