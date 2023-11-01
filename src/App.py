import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from functools import partial
import webbrowser

from .managers.HyperlinkManager import HyperlinkManager
from .Searcher import Searcher

# def callback(url):
#    print(11)
#    webbrowser.open_new_tab(url)

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.attributes('-type', 'splash')
        self.title('Editor')
        # self.geometry("800x500")
        self.folder_path = tk.StringVar()
        self.searcher = Searcher()
        self.__build()

    def __build(self):
        # Button to quit the app.
        options_frame = tk.Frame(self)
        options_frame.pack()
        quit_button = tk.Button(options_frame, text="Quit", command=self.quit)
        quit_button.pack(side=tk.RIGHT)

        help_button = tk.Button(options_frame, text="Help", command=None)
        help_button.pack(side=tk.LEFT)

        # Entry to type search string.
        search_frame = tk.Frame(self)
        search_frame.pack()
        self.string_entry = tk.Entry(search_frame, width=40,  bg="#D3D3D3")
        self.string_entry.pack(side=tk.LEFT)

        # Button to run main script.
        go_button = tk.Button(search_frame, text="Go", command=self.search_files)
        go_button.pack(side=tk.LEFT)

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
        search_string = self.string_entry.get()
        self.text_box.delete("1.0", tk.END)

        # List to store all lines where string is found.
        wordlist = self.searcher.search(search_string)

        self.print_to_textbox(wordlist)

    def print_to_textbox(self, wordlist):
        """Print all lines in wordlist to textbox"""

        for lines in wordlist:
            self.text_box.insert("end", "\n"+lines, self.hyperlink.add(partial(webbrowser.open, 'file:///home/cati0n/Labs/7/ЕЯИИС/Information-retrieval/data/'+lines)))
        if len(wordlist) == 0:
            self.text_box.insert("1.0", "\nNothing To Display")

    def run(self):
        self.mainloop()
