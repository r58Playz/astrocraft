from tkinter import *
from tkinter.ttk import *

window = Tk()
window.geometry("500x500")
window.pack_propagate(0)


def testbar():
    import time
    for i in range(1000):
        import time
        prgbar['value'] = prgbar["value"] + 0.1
        window.update_idletasks()
        time.sleep(0.01)


prgframe = Frame(window)
lbl = Label(prgframe, text="Updating to bleeding edge(NOTE: Git is required)")
lbl.config(width=15)
lbl.pack(side=LEFT)
prgbar = Progressbar(prgframe, orient=HORIZONTAL, length=300, mode="determinate")
prgbar.pack(side=RIGHT)
prgframe.grid(row=0)

# testbtn = Button(window, text="Test PrgBAR", command=testbar)
# testbtn.grid(row=2, column=0)

text = Text(window)
text.insert(END, "AstroCraft Update has been started\n")
text.grid(row=3, column=0)

def startupdate():
    import os
    path = os.getcwd()
    text.insert(END, "Update started.\n")
    prgbar["value"] = 5
    text.insert(END, "Downloading bleeding edge source code\n")
    import subprocess
    import sys
    import pathlib
    ans = os.popen(
        "git clone https://github.com/r58Playz/astrocraft-python.git "
        + str(pathlib.Path.home()) + "/astro-update").read()
    text.insert(END, ans)
    prgbar["value"] = 10
    text.insert(END, "Preparing to compile(DO NOT WORRY, it will not take a lot of time)\n")
    os.chdir(str(pathlib.Path.home()) + "/astro-update")
    ans = subprocess.run("cd " + str(pathlib.Path.home()) + "/astro-update" + "&&" + "pipenv run echo This is working", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=dict(os.environ, PIPENV_IGNORE_VIRTUALENVS="1")).stdout
    text.insert(END, "\n" + ans)
    ans = os.popen("pipenv run pip list --outdated --format=freeze | grep -v '^\-e' | cut -d = -f 1  | xargs -n1 pip install -U").read()
    text.insert(END, "\n" + ans)
    prgbar["value"] = 30
    text.insert(END, "\nStarting to compile...\n")
    ans = os.popen("pipenv run python setup.py build").read()
    text.insert(END, ans)
    prgbar["value"] = 60
    text.insert(END, "\nStarting to copy files...")
    import shutil
    for subdir, dirs, files in os.walk(os.path.dirname(sys.argv[0])):
        for file in files:
            # print os.path.join(subdir, file)
            filepath = subdir + os.sep + file
            shutil.copyfile(filepath, os.path.dirname(sys.argv[0]))
            text.insert("\nCopied " + filepath + " to " + os.path.dirname(sys.argv[0]) + "\\" + file)
            prgbar["value"] = prgbar["value"] + 0.04962779156





upbtn = Button(window, text="Start update", command=startupdate)
upbtn.grid(row=4, column=0)

window.mainloop()
