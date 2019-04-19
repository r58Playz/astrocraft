from subprocess import check_call as run
import shutil
import os
import time
import sys

def update():
    UPDATE_CMD = ( # base command 
    'git clone ' 
    'https://github.com/r58Playz/astrocraft-python.git astrocraft_update --quiet' 
    )
    try:
        run(UPDATE_CMD)
    except:
        print("An error occured. Exiting...")
        time.sleep(3)
        sys.exit()
    files=os.listdir("astrocraft_update")
    for fle in files:
        full_filename = os.path.join("astrocraft_update", fle)
        if os.path.isfile(full_filename):
            if file != "update.py":
                current_dir=os.path.basename(os.getcwd())
                shutil.copy(full_filename, current_dir)
    shutil.rmtree("factories_update/.git", ignore_errors=True)
    shutil.rmtree("factories_update", ignore_errors=True)
    os.system('powershell.exe rm -r -fo astrocraft_update')
