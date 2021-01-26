import tkinter as tk
import win32clipboard as cl
import sys

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.get_clip = tk.Button(self)
        self.get_clip["text"] = "Start Convert"
        self.get_clip["command"] = self.get_paste_buffer
        self.get_clip.pack(side="top")

    def get_paste_buffer(self):
        cl.OpenClipboard(0)
        try:
            result = cl.GetClipboardData()
        except TypeError:
            result = ''  #non-text
        cl.CloseClipboard()
        print(result)
        # return result

root = tk.Tk()
app = Application(master=root)
app.mainloop()
