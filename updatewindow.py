from Tkinter import *
from tkinter.ttk import Progressbar
import time

class UpdateWindow(object):
    def run(self):
        tk = Tk()
        tk.geometry("400x50")
        tk.iconbitmap(default='icon.ico')
        tk.option_add("*Font", "Ubuntu 10")
        tk.option_add("*Button.Font","Ubuntu 10")
        tk.title("Updating...")

        update=Label(tk, text="Updating...")
        update.pack()
        prg=Progressbar(tk, orient="horizontal",length=200, mode="indeterminate")
        prg.start()
        prg.pack()
        tk.mainloop()

if __name__ == "__main__":
    up=UpdateWindow()
    up.run()