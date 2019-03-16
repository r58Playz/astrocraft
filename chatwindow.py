import Tkinter
from Tkconstants import *
from log import Chat
class ChatWindow(object):
    def __init__(self):
        print("")
    def chat(self,text,text1):
        person=text.get()
        msg=text1.get()
        CHAT = Chat("CHAT.FACTORIES")
        CHAT.chat(person, msg)

    def run(self):
        tk = Tkinter.Tk()
        tk.geometry("500x500")
        frame = Tkinter.Frame(tk, relief=FLAT, borderwidth=2)
        frame.pack(fill=BOTH,expand=1)
        person = Tkinter.Label(frame, text="Person")
        person.pack(fill=X, expand=1)
        person = ''
        msg = ''
        entry1 = Tkinter.Entry(frame, exportselection=0, textvariable = person)
        entry1.pack(fill=X, expand = 1)
        message = Tkinter.Label(frame, text="Message")
        entry2 = Tkinter.Entry(frame, exportselection=0, textvariable = msg)
        message.pack(fill=X, expand=1)
        entry2.pack(fill=X, expand = 1)
        button = Tkinter.Button(frame,text="Exit",command=tk.destroy)
        button.pack(side=BOTTOM)
        chatbtn = Tkinter.Button(frame,text="Chat", command= lambda: self.chat(entry1, entry2))
        chatbtn.pack(side=BOTTOM)
        tk.title("Chat")
        tk.mainloop()

if __name__ == "__main__":
    chatwin = ChatWindow()
    chatwin.run()