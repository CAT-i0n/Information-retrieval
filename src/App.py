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
        self.geometry("800x600")
        self.folder_path = tk.StringVar()
        self.searcher = Searcher()
        self.__build()

    def __build(self):
        # Button to quit the app.
        options_frame = tk.Frame(self)
        options_frame.pack()
        quit_button = tk.Button(options_frame, text="Quit", command=self.destroy)
        quit_button.pack(side=tk.RIGHT)

        help_button = tk.Button(options_frame, text="Help", command=self.open_help)
        help_button.pack(side=tk.LEFT)

        metrics_button = tk.Button(options_frame, text="Metrics", command=self.open_metrics)
        metrics_button.pack(side=tk.LEFT)

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
            width=110, borderwidth=2, relief="sunken", padx=20, font=("Helvetica", 15))
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
        docs = self.searcher.search(search_string)

        self.print_to_textbox(docs)

    def print_to_textbox(self, docs):
        """Print all lines in docs to textbox"""
        for i, book in enumerate(docs):
            book, words, sent = book
            words = ", ".join(words)
            self.text_box.insert("end", "\n\n" + str(i+1)+ ". " + book.title + " - " + book.author, self.hyperlink.add(partial(webbrowser.open, 'file:///home/cati0n/Labs/7/ЕЯИИС/Information-retrieval/data/'+book.title+ ".fb2")))
            self.text_box.insert("end", '\n'+ "ключевые слова: "+ words)
            if sent!=[]:
                for i in sent:
                    self.text_box.insert("end", '\n' + i+".")
                    break
        if len(docs) == 0:
            self.text_box.insert("1.0", "\nNothing To Display")

    def open_help(self):
        top = tk.Toplevel()
        #top.geometry("180x100")
        top.attributes('-type', 'splash')
        top.title('Editor')
        l2 = tk.Label(top, text = """Справка:
Ведите поисковой запрос в поле поиска и нажмите Go, 
чтобы получить релевантные результаты
Нажмите Metrics, чтобы получить оценку поисковой системы
Нажмите Clear, чтобы очистить результаты поиска
Нажмите Quit, чтобы выйти""")
        l2.pack()
        quit_button = tk.Button(top, text="Quit", command=top.destroy)
        quit_button.pack(side=tk.BOTTOM)

        top.mainloop()

    def open_metrics(self):
        top = tk.Toplevel()
        #top.geometry("180x100")
        top.attributes('-type', 'splash')
        top.title('Editor')
        l2 = tk.Label(top, text = """Метрики:
Recall: 0.78225
Precision: 0.72364
Accuracy 0.8095
Error: 0.19048
F-measure: 0.72364""")
        l2.pack()
        quit_button = tk.Button(top, text="Quit", command=top.destroy)
        quit_button.pack(side=tk.BOTTOM)

        top.mainloop()

    def run(self):
        self.mainloop()
