import textwrap
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from gui.base_gui import BaseGUI
from tkpywidgets import LabelEntryList, Checklist, EntryType, Radiolist
from backend.constants import ExportFileType, SearchType
from backend import constants


class CommentGUI(BaseGUI):

    search_fields = {
                    'Search Term': EntryType.ENTRY,
                    'Max Results': EntryType.NUMBER,
                    'Author': EntryType.ENTRY,
                    'Subreddit': EntryType.ENTRY,
                    'Posted After': EntryType.DATETIME,
                    'Posted Before': EntryType.DATETIME
    }

    archived_only_return_fields = ['retrieved_datetime', 'retrieved_utc']

    default_return_fields = [
                            'author',
                            'body',
                            'created_datetime',
                            'score',
                            'subreddit'
                            ]

    tooltip_fields = {
                    'Search Term': textwrap.fill('Returns comments that include the term(s) in the filter. To search for multiple terms that all must be included in the same comment, use commas to delineate them.', constants.TEXT_WRAP),
                    'Max Results': textwrap.fill('Sets the maximum amount of results that DCfR will try to return. If there are fewer results available than the number you input, it will return every result it can.', constants.TEXT_WRAP),
                    'Author': textwrap.fill('Returns comments posted by the author in the filter', constants.TEXT_WRAP),
                    'Subreddit': textwrap.fill('Returns comments from the subreddit(s) in the filter. To search in multiple subreddits, use commas to delineate them.', constants.TEXT_WRAP)
    }

    api_fields = {
                    'Search Term': 'q',
                    'Max Results': 'limit',
                    'Author': 'author',
                    'Subreddit': 'subreddit',
                    'Posted After': 'after',
                    'Posted Before': 'before'
    }

    def __init__(self, pmaw, parent, root, executor, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)
        self.pmaw = pmaw
        self.root = root
        self.parent = parent
        self.executor = executor

        self.label_entries = LabelEntryList(self, self.search_fields, title='Search Filters', tooltip_dict=self.tooltip_fields, labelanchor='n')
        self.label_entries.grid(row=0, column=0, rowspan=2, sticky='ns')

        self.return_entries = Checklist(self, constants.COMMENT_RETURN_FIELDS, title='Data to Return', height = 170, scrollbar=True, labelanchor='n', default_checked=self.default_return_fields, can_select_all=True, can_select_default=True, can_clear_all=True)

        self.return_entries.grid(row=0, column=1, sticky='new')

        self.search_type_button = Radiolist(self, options=[e.value for e in SearchType], title='Download Data Using', command='on_search_type_selection', labelanchor='n')
        self.search_type_button.grid(row=1, column=1, sticky='sew')
        self.search_type_button.select(SearchType.PMAW.value)
        self.on_search_type_selection(SearchType.PMAW.value)

        self.file_selected = ''
        self.button_frame = tk.Frame(self)
        self.button_frame.grid(row=2, column=0, columnspan=2)
        self.button_frame.columnconfigure(0, pad=20)
        self.button_frame.columnconfigure(1, pad=20)

        self.run_button = tk.Button(self.button_frame, text='Run', command=self.run)
        self.file_button = tk.Button(self.button_frame, text='Select File', command=self.select_file)
        self.file_button.grid(row=0, column=0)

        self.rowconfigure(0, pad=10)
        self.rowconfigure(1, pad=10)
        self.rowconfigure(2, pad=10)
        self.columnconfigure(0, pad=20)
        self.columnconfigure(1, pad=20)


    def run(self):
        entry_dict = self.get_entries()
        if entry_dict['q'] is None and entry_dict['subreddit'] is None and entry_dict['author'] is None:
            messagebox.showerror(title='Impossible Search Filters', message='A Search Term, Author, or Subreddit must be provided')
            return
        if entry_dict['before'] is not None and entry_dict['after'] is not None:
            if entry_dict['before'] < entry_dict['after'] :
                messagebox.showerror(message='\'Posted Before\' is set to before \'Posted After\'. No data will be available.', title='Impossible Search Filters')
                return
            elif entry_dict['before'] == entry_dict['after']:
                messagebox.showerror(message='\'Posted Before\' is set exactly the same as \'Posted After\'. No data will be available.', title='Impossible Search Filters')
                return
        self.parent.select(constants.NotebookPage.OUTPUT_PAGE.value)
        self.executor.submit(self.pmaw.save_comment_file, entry_dict, file=self.file_selected, file_type=ExportFileType.CSV.value, search_type=self.search_type_button.get_choice())


    def select_file(self):
        self.file_selected = filedialog.asksaveasfilename()

        if self.file_selected:
            self.run_button.grid(row=0, column=1)
            self.file_button.grid(row=0, column=0)
        else:
            self.run_button.grid_forget()
            self.file_button.grid(row=0, column=0)

    def on_search_type_selection(self, search_type_value):
        if search_type_value == SearchType.PMAW.value: # archived
            self.return_entries.show_all_items()
        elif search_type_value == SearchType.PRAW.value: # reddit
            self.return_entries.hide_items(self.archived_only_return_fields)


    def get_entries(self):
        entry_dict = {}

        for key in self.search_fields.keys():
            entry_dict[self.api_fields[key]] = self.label_entries.get_entry(key)

            if entry_dict[self.api_fields[key]] == '':
                entry_dict[self.api_fields[key]] = None

        if entry_dict['limit']:
            entry_dict['limit'] = int(entry_dict['limit'])
        else:
            entry_dict['limit'] = None

        entry_dict['fields'] = self.return_entries.get_checked_items()

        if entry_dict['after']['date']:
            entry_dict['after'] = self.date_time_to_epoch(entry_dict['after']['date'], entry_dict['after']['time'])
        else:
            entry_dict['after'] = None
            
        if entry_dict['before']['date']:
            entry_dict['before'] = self.date_time_to_epoch(entry_dict['before']['date'], entry_dict['before']['time'])
        else:
            entry_dict['before'] = None

        return entry_dict

    
    def disable_run(self):
        self.run_button['state'] = 'disabled'

    def enable_run(self):
        self.run_button['state'] = 'normal'