import Tkinter
from Tkconstants import *
from helpwindow import HelpWindow
from updater import update as updte

class StartWindow(object):
    
    def start(self, tk):
        import main
        main.run(tk)
    def hlp(self):
        hlp=HelpWindow()
        hlp.run()
        del hlp
    def update(self):
        updte()
    def run(self):
        """Runs the window
        """

        # Window
        tk = Tkinter.Tk()


        # configuration settings
        tk.geometry("350x400")
        tk.iconbitmap(default='icon.ico')
        tk.option_add("*Font", "Ubuntu 10")
        tk.option_add("*Button.Font","Ubuntu 10")
        tk.title("Factories 0.1.0")


        # frame
        frame = Tkinter.Frame(tk, relief=FLAT, borderwidth=2)
        frame.pack(fill=BOTH,expand=1)

        # labels and other things
        factories = Tkinter.Label(frame, text="Factories v0.1.0", font="Ubuntu 20")
        factories.pack()
        button = Tkinter.Button(frame,text="Exit",command=tk.destroy)
        button.pack()
        startbtn = Tkinter.Button(frame,text="Start", command=lambda: self.start(tk))
        startbtn.pack()
        helpbtn = Tkinter.Button(frame, text="Help", command=self.hlp)
        helpbtn.pack()
        upbtn = Tkinter.Button(frame, text="Update", command=self.update)
        upbtn.pack()
        newshead = Tkinter.Label(frame, text="News",font="Ubuntu 20")
        newshead.pack()
        newsvar=Tkinter.StringVar()
        newsvar.set("Factories 0.1.0 includes a new graphical interface(windows made by tkinter).")
        news = Tkinter.Label(frame,textvariable=newsvar, font="Ubuntu", wraplength=400, justify="left")
        news.pack()
        tk.mainloop()

if __name__ == "__main__":
    startwin = StartWindow()
    startwin.run()
