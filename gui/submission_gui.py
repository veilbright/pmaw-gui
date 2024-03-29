import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkpywidgets import LabelEntryList, Checklist, EntryType, Radiolist
from gui.base_gui import BaseGUI
from enum import Enum
from backend.constants import ExportFileType, SearchType
import textwrap
import backend.constants as constants


class Dropdowns(Enum):
    NSFW = ('NSFW Submissions', 'No Filter', 'NSFW Only', 'SFW Only')
    VIDEO = ('Video Submissions', 'No Filter', 'Video Only', 'Exclude Videos')
    LOCKED = ('Locked Comments', 'No Filter', 'Locked Only', 'Unlocked Only')
    STICKIED = ('Stickied Submission', 'No Filter', 'Stickied Only', 'Exlude Stickied')
    SPOILERS = ('Spoliers', 'No Filter', 'Spoliers Only', 'Exclude Spoilers')
    CONTEST = ('Using Contest Mode', 'No Filter', 'Contest Mode Only', 'Exclude Contest Mode')



class SubmissionGUI(BaseGUI):
    search_fields = {
                    'Search Title and Body': EntryType.ENTRY,
                    #'Exclude Search Term': EntryType.ENTRY,
                    'Search Title': EntryType.ENTRY,
                    #'Exclude Title Text': EntryType.ENTRY,
                    'Search Body': EntryType.ENTRY,
                    #'Exclude Body Text': EntryType.ENTRY,
                    'Max Results': EntryType.NUMBER,
                    'Author': EntryType.ENTRY,
                    'Subreddit': EntryType.ENTRY,
                    #'Score': EntryType.RANGE,
                    #'Number of Comments': EntryType.RANGE,
                    ('NSFW Submissions', 'No Filter', 'NSFW Only', 'SFW Only'): EntryType.DROPDOWN,
                    ('Video Submissions', 'No Filter', 'Video Only', 'Exclude Videos'): EntryType.DROPDOWN,
                    ('Locked Comments', 'No Filter', 'Locked Only', 'Unlocked Only'): EntryType.DROPDOWN,
                    ('Stickied Submission', 'No Filter', 'Stickied Only', 'Exlude Stickied'): EntryType.DROPDOWN,
                    ('Spoliers', 'No Filter', 'Spoliers Only', 'Exclude Spoilers'): EntryType.DROPDOWN,
                    ('Using Contest Mode', 'No Filter', 'Contest Mode Only', 'Exclude Contest Mode'): EntryType.DROPDOWN,
                    'Posted after': EntryType.DATETIME,
                    'Posted before': EntryType.DATETIME
    }

    tooltip_fields = {
                    'Search Title and Body': textwrap.fill('Returns submissions that include the term(s) in the filter in the submission’s title or body. To search for multiple terms that all must be included in the same submission, use commas to delineate them.', constants.TEXT_WRAP),
                    'Search Title': textwrap.fill('Returns submissions that include the term(s) in the filter in the submission’s title. To search for multiple terms that all must be included in the same title, use commas to delineate them.', constants.TEXT_WRAP),
                    'Search Body': textwrap.fill('Returns submissions that include the term(s) in the filter in the submission’s body. To search for multiple terms that all must be included in the body, use commas to delineate them.', constants.TEXT_WRAP),
                    'Max Results': textwrap.fill('Sets the maximum amount of results that DCfR will try to return. If there are fewer results available than the number you input, it will return every result it can.', constants.TEXT_WRAP),
                    'Author': textwrap.fill('Returns submissions posted by the author in the filter.', constants.TEXT_WRAP),
                    'Subreddit': textwrap.fill('Returns submissions from the subreddit(s) in the filter. To search in multiple subreddits, use commas to delineate them.', constants.TEXT_WRAP)
    }

    archived_only_return_fields = ['full_link', 'retrieved_datetime', 'retrieved_on']

    default_return_fields = [
                            'author',
                            'created_datetime',
                            'score',
                            'selftext',
                            'subreddit',
                            'title'
                            ]

    api_fields = {
                    'Search Title and Body': 'q',
                    'Exclude Search Term': 'q:not',
                    'Search Title': 'title',
                    'Exclude Title Text': 'title:not',
                    'Search Body': 'selftext',
                    'Exclude Body Text': 'selftext:not',
                    'Max Results': 'limit',
                    'Author': 'author',
                    'Subreddit': 'subreddit',
                    'Score': 'score',
                    'Number of Comments': 'num_comments',
                    'NSFW Submissions': 'over_18',
                    'Video Submissions': 'is_video',
                    'Locked Comments': 'locked',
                    'Stickied Submission': 'stickied',
                    'Spoliers': 'spoiler',
                    'Using Contest Mode': 'contest_mode',
                    'Posted after': 'after',
                    'Posted before': 'before'
    }

    def __init__(self, pmaw, parent, root, executor, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)
        self.pmaw = pmaw
        self.root = root
        self.parent = parent
        self.executor = executor

        self.label_entries = LabelEntryList(self, self.search_fields, title='Search Filters', tooltip_dict=self.tooltip_fields, labelanchor='n')
        self.label_entries.grid(row=0, column=0, rowspan=2, sticky='ns')
        self.label_entries.update()

        self.return_entries = Checklist(self, constants.SUBMISSION_RETURN_FIELDS, title='Data to Return', scrollbar=True, height=420, labelanchor='n', default_checked=self.default_return_fields, can_clear_all=True, can_select_all=True, can_select_default=True)

        self.return_entries.grid(row=0, column=1, sticky='new')

        self.file_type_button = Radiolist(self, options=[e.value for e in ExportFileType], title='Save as File Type', labelanchor='n')

        self.search_type_button = Radiolist(self, options=[e.value for e in SearchType], title='Download Data Using', command='on_search_type_selection', labelanchor='n')
        self.search_type_button.grid(row=1, column=1, sticky='sew')
        self.search_type_button.select(SearchType.PMAW.value)

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
        if entry_dict['q'] is None and entry_dict['title'] is None and entry_dict['selftext'] is None and entry_dict['author'] is None and entry_dict['subreddit'] is None:
            messagebox.showerror(title='Impossible Search Filters', message='A Search Term, Author, or Subreddit must be provided')
            return
        if entry_dict['before'] is not None and entry_dict['after'] is not None:
            if entry_dict['before'] < entry_dict['after'] :
                messagebox.showerror(message='\'Posted Before\' is set to before \'Posted After\'. No data will be available.', title='Impossible Search Filters')
                return
        self.parent.select(constants.NotebookPage.OUTPUT_PAGE.value)
        self.executor.submit(self.pmaw.save_submission_file, entry_dict, file=self.file_selected, file_type=self.file_type_button.get_choice(), search_type=self.search_type_button.get_choice())
    
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
            if type(key) is tuple:
                entry_dict[self.api_fields[key[0]]] = self.label_entries.get_entry(key[0])

                if entry_dict[self.api_fields[key[0]]] == '' or entry_dict[self.api_fields[key[0]]] == key[1]:
                    entry_dict[self.api_fields[key[0]]] = None
                elif entry_dict[self.api_fields[key[0]]] == key[2]:
                    entry_dict[self.api_fields[key[0]]] = 'true'
                elif entry_dict[self.api_fields[key[0]]] == key[3]:
                    entry_dict[self.api_fields[key[0]]] = 'false'

            else:
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