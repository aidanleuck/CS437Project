from tkinter import *

import PIL
from PIL import ImageTk
from PIL import Image
from identify_candidate_resources import Identifier
from Ranker.QueryRanker import QueryRanker
import constants as constant
import pickle
from Tokenize.tokenizer import Tokenizer
import re
import Global as globals
from snippet import Snippet
from collections import defaultdict
from better_profanity import profanity

try:
    from tkinter import StringVar, Entry, Frame, Listbox, Scrollbar, Label, Button, PhotoImage, Image
    from tkconstants import *
except ImportError:
    from tkinter import StringVar, Entry, Frame, Listbox, Scrollbar
    from tkinter.constants import *

from QLog.QuerySuggester import QuerySuggester



def autoscroll(sbar, first, last):
    """Hide and show scrollbar as needed."""
    first, last = float(first), float(last)
    if first <= 0 and last >= 1:
        sbar.grid_remove()
    else:
        sbar.grid()
    sbar.set(first, last)

class Combobox_Autocomplete(Entry, object):
    def __init__(self, master, list_of_items=None, autocomplete_function=None, listbox_width=None, listbox_height=7, ignorecase_match=False, startswith_match=True, vscrollbar=True, hscrollbar=True, **kwargs):
        if hasattr(self, "autocomplete_function"):
            if autocomplete_function is not None:
                raise ValueError("Combobox_Autocomplete subclass has 'autocomplete_function' implemented")
        else:
            if autocomplete_function is not None:
                self.autocomplete_function = autocomplete_function
            else:
                if list_of_items is None:
                    raise ValueError("If not guiven complete function, list_of_items can't be 'None'")

                if ignorecase_match:
                    if startswith_match:
                        def matches_function(entry_data, item):
                            return item.startswith(entry_data)
                    else:
                        def matches_function(entry_data, item):
                            return item in entry_data

                    self.autocomplete_function = lambda entry_data: [item for item in self.list_of_items if matches_function(entry_data, item)]
                else:
                    if startswith_match:
                        def matches_function(escaped_entry_data, item):
                            if re.match(escaped_entry_data, item, re.IGNORECASE):
                                return True
                            else:
                                return False
                    else:
                        def matches_function(escaped_entry_data, item):
                            if re.search(escaped_entry_data, item, re.IGNORECASE):
                                return True
                            else:
                                return False

                    def autocomplete_function(entry_data):  #vmcerda ~ sorts through list to find matching values
                        spaces = sum(1 for match in re.finditer('\s+', entry_data))
                        words = entry_data.split()
                        if(spaces == len(words)):
                            entry_data=entry_data.strip()
                            suggester = QuerySuggester()
                            suggestions = suggester.getQuerySuggestions(entry_data)
                            # return [item for item in self.list_of_items if matches_function(escaped_entry_data,item)]
                            return (suggestions)

                    self.autocomplete_function = autocomplete_function

        self._listbox_height = int(listbox_height)
        self._listbox_width = listbox_width

        self.list_of_items = list_of_items

        self._use_vscrollbar = vscrollbar
        self._use_hscrollbar = hscrollbar

        kwargs.setdefault("background", "white")

        if "textvariable" in kwargs:
            self._entry_var = kwargs["textvariable"]
        else:
            self._entry_var = kwargs["textvariable"] = StringVar()

        Entry.__init__(self, master, **kwargs)

        self._trace_id = self._entry_var.trace('w', self._on_change_entry_var)

        self._listbox = None

        self.bind("<Tab>", self._on_tab)
        self.bind("<Up>", self._previous)
        self.bind("<Down>", self._next)
        self.bind('<Control-n>', self._next)
        self.bind('<Control-p>', self._previous)
        self.bind("<Delete>", self._delete)

        self.bind("<Return>", self._update_entry_from_listbox)
        self.bind("<Escape>", lambda event: self.unpost_listbox())

    def _on_tab(self, event):
        self.post_listbox()
        return "break"

    def _on_change_entry_var(self, name, index, mode):

        entry_data = self._entry_var.get()

        if entry_data == '':
            self.unpost_listbox()
            self.focus()
        else:
            values = self.autocomplete_function(entry_data)
            if values:
                if self._listbox is None:
                    self._build_listbox(values)
                else:
                    self._listbox.delete(0, END)

                    height = min(self._listbox_height, len(values))
                    self._listbox.configure(height=height)

                    for item in values:
                        self._listbox.insert(END, item)

            else:
                self.unpost_listbox()
                self.focus()

    def _build_listbox(self, values):
        listbox_frame = Frame()

        self._listbox = Listbox(listbox_frame, background="white", selectmode=SINGLE, activestyle="none",
                                exportselection=False)
        self._listbox.grid(row=0, column=0,sticky = N+E+W+S)

        self._listbox.bind("<ButtonRelease-1>", self._update_entry_from_listbox)
        self._listbox.bind("<Return>", self._update_entry_from_listbox)
        self._listbox.bind("<Escape>", lambda event: self.unpost_listbox())

        self._listbox.bind('<Control-n>', self._next)
        self._listbox.bind('<Control-p>', self._previous)
        self._listbox.bind('<Delete>', self._delete)

        if self._use_vscrollbar:
            vbar = Scrollbar(listbox_frame, orient=VERTICAL, command= self._listbox.yview)
            vbar.grid(row=0, column=1, sticky=N+S)

            self._listbox.configure(yscrollcommand= lambda f, l: autoscroll(vbar, f, l))

        if self._use_hscrollbar:
            hbar = Scrollbar(listbox_frame, orient=HORIZONTAL, command= self._listbox.xview)
            hbar.grid(row=1, column=0, sticky=E+W)

            self._listbox.configure(xscrollcommand= lambda f, l: autoscroll(hbar, f, l))

        listbox_frame.grid_columnconfigure(0, weight= 1)
        listbox_frame.grid_rowconfigure(0, weight= 1)

        x = -self.cget("borderwidth") - self.cget("highlightthickness")
        y = self.winfo_height()-self.cget("borderwidth") - self.cget("highlightthickness")

        if self._listbox_width:
            width = self._listbox_width
        else:
            width=self.winfo_width()

        listbox_frame.place(in_=self, x=x, y=y, width=width)

        height = min(self._listbox_height, len(values))
        self._listbox.configure(height=height)

        for item in values:
            self._listbox.insert(END, item)

    def post_listbox(self):
        if self._listbox is not None: return

        entry_data = self._entry_var.get()
        if entry_data == '': return

        values = self.autocomplete_function(entry_data)
        if values:
            self._build_listbox(values)

    def unpost_listbox(self):
        if self._listbox is not None:
            self._listbox.master.destroy()
            self._listbox = None

    def get_value(self):
        return self._entry_var.get()

    def set_value(self, text, close_dialog=False):
        self._set_var(text)

        if close_dialog:
            self.unpost_listbox()

        self.icursor(END)
        self.xview_moveto(1.0)

    def _set_var(self, text):
        self._entry_var.trace_vdelete("w", self._trace_id)
        self._entry_var.set(text)
        self._trace_id = self._entry_var.trace('w', self._on_change_entry_var)

    def _update_entry_from_listbox(self, event):
        if self._listbox is not None:
            current_selection = self._listbox.curselection()

            if current_selection:
                text = self._listbox.get(current_selection)
                self._set_var(text)

            self._listbox.master.destroy()
            self._listbox = None

            self.focus()
            self.icursor(END)
            self.xview_moveto(1.0)

        return "break"

    def _previous(self, event):
        if self._listbox is not None:
            current_selection = self._listbox.curselection()

            if len(current_selection) == 0:
                self._listbox.selection_set(0)
                self._listbox.activate(0)
            else:
                index = int(current_selection[0])
                self._listbox.selection_clear(index)

                if index == 0:
                    index = END
                else:
                    index -= 1

                self._listbox.see(index)
                self._listbox.selection_set(first=index)
                self._listbox.activate(index)

        return "break"

    def _next(self, event):
        if self._listbox is not None:

            current_selection = self._listbox.curselection()
            if len(current_selection) == 0:
                self._listbox.selection_set(0)
                self._listbox.activate(0)
            else:
                index = int(current_selection[0])
                self._listbox.selection_clear(index)

                if index == self._listbox.size() - 1:
                    index = 0
                else:
                    index += 1

                self._listbox.see(index)
                self._listbox.selection_set(index)
                self._listbox.activate(index)
        return "break"

    def _delete(self):
        if self._listbox is not None:
            return "break"

def get_snippets(results, query):
    snippets = []
    t = Tokenizer()
    query = t.clean_line(query).lower() # clean query
    query_words = query.split() # get words from query
    for doc in results:
        doc.text = re.sub(r"\n\n", '. ', doc.text)
        sentences = re.split(r"[.?!]\s*", doc.text) # split on sentences
        sentences_pq = []

        query_wordFreq = {}
        for sentence in sentences: # loop through sentences
            sentence = sentence.lower()
            for queryWord in query_words:
                count = sentence.count(" "+queryWord+" ")
                if(count > 0):
                    if(query_wordFreq.get(queryWord)):
                        query_wordFreq[queryWord] +=count
                    else:
                        query_wordFreq[queryWord] = count
        for sentence in sentences:
            sentence = sentence.lower()
            tokenFrequency = 0
            totalTermFrequency = 0
            tf_idf = 0
            mostFrequentDict = defaultdict(int)
            if any(word in sentence for word in query_words): # if sentence contains words in query
                for word in sentence.split(" "):
                    mostFrequentDict[word] += 1
                for queryWord in query_words:
                    tokenFrequency = sentence.count(queryWord)
                    mostFrequentTerm = max(mostFrequentDict, key=mostFrequentDict.get)
                    frequentTerm = mostFrequentDict[mostFrequentTerm]
                    numSentences = len(sentences)
                    termFrequency = query_wordFreq.get(queryWord)
                    if not termFrequency:
                        termFrequency = 0
                    tf_idf += globals.calc_TFIDF(tokenFrequency, frequentTerm, numSentences, termFrequency) # find tfidf of sentence
                sentences_pq.append((tf_idf, sentence)) # store sentence along with tfidf val in prio q
        count = 0
        sentences_pq.sort(reverse=True)
        snip_sentences = []
        while sentences_pq and count < 2: # grab two sentences (or less) with associated highest value
            snip_sentences.append(sentences_pq.pop(0)[1])
            count += 1
        snippet = Snippet(doc.id,doc.title, snip_sentences) # create a new snippet object, setting the sentences and
        # the
        # title.
        snippets.append(snippet) # add it to snippets
    return snippets# return snippets

def generate_results(combo_val):
    with open(constant.BASEDIR + constant.INDEX_PATH, 'rb') as i:
        index = pickle.load(i)
    with open(constant.BASEDIR + constant.STOPWORD_PATH, 'rb') as sw:
        stop_words = pickle.load(sw)
    identifier = Identifier(combo_val.strip(), index, stop_words)
    qr = QueryRanker(combo_val, index, stop_words)
    results = qr.getRanks(identifier.filter_query())
    snippetList = get_snippets(results, combo_val)
    return snippetList

def build_search(lb, param):
    lb.delete('1.0',END)
    lb.tag_config('heading', foreground="BLUE")
    result = generate_results(param)
    if(result):
        for keys in result[0:10]:
            #id = str(keys.id)
            # lb.insert(INSERT, keys.title + " " + id + "\n", 'heading')
            lb.insert(INSERT, profanity.censor(keys.title) + "\n", 'heading')
            lb.insert(END, profanity.censor(keys.sentences) + "\n\n")
    else:
        lb.insert(INSERT,"No Search Results")
    lb.pack(padx=5, pady=5)


if __name__ == '__main__':
    try:
        from tkinter import Tk
    except ImportError:
        from tkinter import Tk

    list_of_items = []
    root = Tk()
    root.title("Information Retrieval")
    root.geometry("600x600")
    root.configure(background='#66cc00')

    my_pic = PIL.Image.open("Images/avo2.png")
    resized = my_pic.resize((200,120))
    img = ImageTk.PhotoImage(resized)

    Label(root, bg='#66cc00', image=img, font=('Times', 21), text='AVO-cado Query').pack()
    combobox_autocomplete = Combobox_Autocomplete(root, list_of_items, width=30, highlightthickness=1)
    combobox_autocomplete.pack()
    lb = Text(root,bg="white",width=650,height=550, wrap=WORD)
    Button(root, text="SEARCH", fg="red",command=lambda:build_search(lb, combobox_autocomplete.get_value().strip()),
           highlightbackground='#66cc00').pack()

    combobox_autocomplete.focus()

    root.mainloop()