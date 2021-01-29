import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import win32clipboard as cl
import sys

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.btnClipToHtml = tk.Button(self)
        self.btnClipToHtml["text"] = "Start Convert"
        self.btnClipToHtml["command"] = self.get_paste_buffer
        self.btnClipToHtml.pack(fill = "x", padx = 20, pady = 20, side="left")
        self.textArea = ScrolledText(self, font = ("", 10), height = 40, width = 80)
        self.textArea.pack(fill=tk.BOTH, padx = 20, pady = 40)

    def get_paste_buffer(self):
        cl.OpenClipboard(0)
        cfHtml = cl.RegisterClipboardFormat("HTML Format")
        try:
            result = cl.GetClipboardData(cfHtml)
        except TypeError:
            result = 'unknown'  #non-text
        cl.CloseClipboard()
        print(result.decode("utf-8", errors="ignore"))
        self.textArea.insert(tk.END, result.decode("utf-8", errors = "ignore"))
        # return result

root = tk.Tk()
app = Application(master=root)
root.title("Clipboard To Markdown Converter")
root.geometry("800x800")
app.mainloop()
