import Tkinter
from Tkconstants import *

class HelpWindow(object):
    def hlp(self):
        return """
Description:
    Factories is a game like Minecraft.
Key mappings:
    W for forward
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
    
    def run(self):
        tk = Tkinter.Tk()
        

        # configuration settings
        tk.geometry("300x300")
        tk.iconbitmap(default='icon.ico')
        tk.option_add("*Font", "Ubuntu 10")
        tk.option_add("*Button.Font","Ubuntu 10")
        tk.title("Help:Factories")


        hlp=Tkinter.Label(tk, text=self.hlp(), justify="left")
        hlp.pack()
        close=Tkinter.Button(tk, text="Close", command=tk.destroy)
        close.pack()
        tk.mainloop()

if __name__ == "__main__":
    hlp=HelpWindow()
    hlp.run()