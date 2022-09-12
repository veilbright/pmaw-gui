from pmaw import PushshiftAPI
import pandas as pd
import os


class CallPmaw:

    def __init__(self) -> None:
        self.api = PushshiftAPI()

    def get_df(self, dict):
        q = dict['q']
        limit = dict['limit']
        fields = dict['fields']
        author = dict['author']
        subreddit = dict['subreddit']
        after = dict['after']
        before = dict['before']

        if 'file' not in dict:
            file = os.path.dirname(os.path.realpath(__file__)) + '\\pmaw.csv'
        else:
            file = dict['file']

        if isinstance(after, int) and isinstance(before, int):
            comments = self.api.search_comments(q=q, limit=limit, fields=fields, author=author, subreddit=subreddit, after=after, before=before)
        elif isinstance(after, int):
            comments = self.api.search_comments(q=q, limit=limit, fields=fields, author=author, subreddit=subreddit, after=after)
        elif isinstance(before, int):
            comments = self.api.search_comments(q=q, limit=limit, fields=fields, author=author, subreddit=subreddit, before=before)
        else:
            comments = self.api.search_comments(q=q, limit=limit, fields=fields, author=author, subreddit=subreddit)

        comment_list = [comment for comment in comments]
        df = pd.DataFrame(comment_list)

        df.to_csv(file)

        print('Data saved to ' + file)