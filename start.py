import Tkinter

from log import Chat
from Tkconstants import *


class StartWindow(object):
    
    def __init__(self):
        print("")
    
    def hlp(self):
        return """W for forward
S for back
A for left
D for right
Space key to jump
R key to save
1 key to release mouse
Tab key to toggle flying
E key to chat (it's command-line)
Q key to exit
        """
    def gethelp(self, label, notice):
        label.pack_forget()
        notice.set(self.hlp())
        label.pack()
    def run(self):
        tk = Tkinter.Tk()
        frame = Tkinter.Frame(tk, relief=RIDGE, borderwidth=2)
        frame.pack(fill=BOTH,expand=1)
        person = Tkinter.Label(frame, text="Factories v0.0.4")
        person.pack(fill=X, expand=1)
        notice = Tkinter.StringVar()
        label = Tkinter.Label(frame, textvariable=notice)
        notice.set("Help will show here.")
        label.pack(side=BOTTOM)
        button = Tkinter.Button(frame,text="Exit",command=tk.destroy)
        button.pack(side=BOTTOM)
        import main
        startbtn = Tkinter.Button(frame,text="Start", command=main.run)
        startbtn.pack(side=BOTTOM)
        helpbtn = Tkinter.Button(frame, text="Help", command= lambda: self.gethelp(label, notice))
        helpbtn.pack()
        tk.mainloop()

if __name__ == "__main__":
    startwin = StartWindow()
    startwin.run()
