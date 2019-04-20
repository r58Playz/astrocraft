import shutil
import os
import zipfile
import main

def update():
    updatezip = urllib.request.urlopen('https://github.com/r58Playz/astrocraft-python/archive/master.zip')
    zipref = zipfile.ZipFile(BytesIO(updatezip.read()))
    zipref.extractall("astrocraft_update")
    zipref.close()
    files=os.listdir("astrocraft_update")
    for fle in files:
        full_filename = os.path.join("astrocraft_update", fle)
        if os.path.isfile(full_filename):
            if file != "update.py":
                current_dir=os.path.basename(os.getcwd())
                shutil.copy(full_filename, current_dir)
     shutil.rmtree("pycraft_update")
     main.start()# Should work...
