import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import win32clipboard as cl
import sys
import re

def delete_crlf_code_from_top(original_text):
    new_text = re.sub(r"^\r|\n\r|\n", r"", original_text)
    return new_text

def delete_crlf_and_tab(original_text):
    new_text = re.sub(r"\r|\n\r|\n|\t", r"", original_text)
    return new_text

def get_table_item(html_text):
    pattern = re.compile(r"(<TABLE[\s\S]*?</TABLE>)")
    match = pattern.search(html_text)
    if match:
        result = match.group()
    else:
        result = ""
    return result

def delete_tag_area(html_text):
    pattern = re.compile(r"<[^>]+>")
    new_text = pattern.sub("", html_text)
    return new_text

def get_table_row_data_list(html_text):
    pattern = re.compile(r"<TR[\s\S]*?</TR>")
    match_list = pattern.findall(html_text)
    return match_list

def get_table_col_data_list(html_text):
    pattern = re.compile(r"(<TD[\s\S]*?</TD>)")
    match_list = pattern.findall(html_text)
    return match_list

def generate_markdown_table_text(html_text):
    markdown_text = ""
    new_text = delete_crlf_code_from_top(html_text)
    table_tag_area = get_table_item(new_text)
    table_row_list = get_table_row_data_list(table_tag_area)
    row_count = 0
    for table_row_data in table_row_list:
        row_text = "|"
        row_data = table_row_data
        table_col_list = get_table_col_data_list(row_data)
        col_count = 0
        for col_data in table_col_list:
            data = col_data
            data = delete_crlf_and_tab(data)
            data = delete_tag_area(data)
            if col_count == len(table_col_list) - 1:
                row_text = row_text + data + "|\n"
            else:
                row_text = row_text + data + "|"
            col_count += 1
        if row_count == 0:
            header_line = "|"
            for i in range(col_count - 1):
                header_line = header_line + "-|"
            row_text = row_text + header_line + "-|\n"
        markdown_text = markdown_text + row_text
        row_count += 1
    return markdown_text

def get_paste_buffer():
    cl.OpenClipboard(0)
    cfHtml = cl.RegisterClipboardFormat("HTML Format")
    try:
        result = cl.GetClipboardData(cfHtml)
    except TypeError:
        result = "unknown"  #non-text
    cl.CloseClipboard()
    result = result.decode("utf-8", errors = "ignore")
    return result

class Application(tk.Frame):
    def __init__(self, master = None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.btn_clipboard_to_html = tk.Button(self)
        self.btn_clipboard_to_html["text"] = "Start Convert to HTML"
        self.btn_clipboard_to_html["command"] = self.get_html_text
        self.btn_clipboard_to_html.pack(fill = "x", padx = 20, pady = 20, side="left")

        self.btn_clipboard_to_markdown = tk.Button(self)
        self.btn_clipboard_to_markdown["text"] = "Start Convert to MD"
        self.btn_clipboard_to_markdown["command"] = self.get_markdown_text
        self.btn_clipboard_to_markdown.pack(fill = "x", padx = 20, pady = 20, side="left")

        self.text_area = ScrolledText(self, font = ("", 10), height = 40, width = 80)
        self.text_area.pack(fill=tk.BOTH, padx = 20, pady = 40)

    def get_html_text(self):
        clipboard_text = get_paste_buffer()
        if clipboard_text != "unknown":
            html_text = delete_crlf_code_from_top(clipboard_text)
            html_text = get_table_item(html_text)
        else:
            html_text = ""
        self.text_area.delete("1.0", tk.END)
        self.text_area.insert(tk.END, html_text)
    def get_markdown_text(self):
        clipboard_text = get_paste_buffer()
        if clipboard_text != "unknown":
            markdown_text = generate_markdown_table_text(clipboard_text)
        else:
            markdown_text = ""
        self.text_area.delete("1.0", tk.END)
        self.text_area.insert(tk.END, markdown_text)

root = tk.Tk()
root.title("Clipboard To Markdown Converter")
root.geometry("800x600")
app = Application(master = root)
app.mainloop()
