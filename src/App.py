from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText
import pandas as pd
import tkinter as tk
import os
import re
import sys
from functools import partial
import webbrowser


class HyperlinkManager:
    def __init__(self, text):
        self.text = text
        self.text.tag_config("hyper", foreground="blue", underline=1)
        self.text.tag_bind("hyper", "<Button-1>", self._click)

        self.reset()

    def reset(self):
        self.links = {}

    def add(self, action):
        # add an action to the manager.  returns tags to use in
        # associated text widget
        tag = "hyper-%d" % len(self.links)
        self.links[tag] = action
        return "hyper", tag
    
    def _click(self, event):
        for tag in self.text.tag_names(tk.CURRENT):
            if tag[:6] == "hyper-":
                self.links[tag]()
                return

# def callback(url):
#    print(11)
#    webbrowser.open_new_tab(url)

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.attributes('-type', 'splash')
        self.title('Editor')
        # self.geometry("800x500")
        self.attributes('-type', 'splash')
        self.folder_path = tk.StringVar()
        self.__build()

    def __build(self):
        # Entry to type search string.

        f_top = tk.Frame(self)
        f_top.pack()
        self.string_entry = tk.Entry(f_top, width=40,  bg="#D3D3D3")
        self.string_entry.pack(side=tk.LEFT)

        # Button to run main script.
        go_button = tk.Button(f_top, text="Go", command=self.search_files)
        go_button.pack(side=tk.LEFT)

        # Button to quit the app.
        quit_button = tk.Button(self, text="Quit", command=self.quit)
        quit_button.pack()

        # Text box to display output of main text.
        self.text_box = ScrolledText(
            width=110, borderwidth=2, relief="sunken", padx=20)
        self.text_box.pack()

        self.hyperlink = HyperlinkManager(self.text_box)

        # Button to clear the text box display.
        clear_button = tk.Button(
            self, text="Clear", command=lambda: self.text_box.delete("1.0", tk.END))
        clear_button.pack()

    def search_files(self):
        """Search all files in specified directory"""
        searchString = self.string_entry.get()
        self.text_box.delete("1.0", tk.END)

        # List to store all lines where string is found.
        wordlist = []

        wordlist = ['terror.fb2', 'time_child.fb2']

        self.print_to_textbox(wordlist)

    def print_to_textbox(self, wordlist):
        """Print all lines in wordlist to textbox"""

        for lines in wordlist:
            self.text_box.insert("end", "\n"+lines, self.hyperlink.add(partial(webbrowser.open, 'file:///home/cati0n/pyCommon/'+lines)))
        if len(wordlist) == 0:
            self.text_box.insert("1.0", "\nNothing To Display")

    def run(self):
        self.mainloop()
