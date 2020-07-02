import pickle
from pickle import UnpicklingError
from pprint import pprint

import pkg_resources
import praw
import datetime

import prawcore
from dateutil.relativedelta import *
from praw.models import MoreComments


class SotdPostLocator(object):
    """
    Get
    """

    SOTD_THREAD_PATTERNS = ['sotd thread', 'lather games']
    CACHE_DIR = pkg_resources.resource_filename('sotd_collator', '../misc/')

    def __init__(self, praw):
        self.praw = praw

    @property
    def last_month(self):
        return datetime.date.today() - relativedelta(months=2)

    def _get_sotd_query_str(self, given_month):
        return 'flair_name:SOTD ({0} OR {1}) {2}'.format(
            given_month.strftime('%b').lower(),
            given_month.strftime('%B').lower(),
            given_month.year,
        )


    def get_x_most_recent_threads(self, threads_to_fetch=50):
        res = self.praw.subreddit('wetshaving').search(
            query='flair_name:SOTD',
            limit=threads_to_fetch,
        )
        return [
            x for x in res if [
                # filter out threads with SOTD flair that arent true SOTD threads
                y for y in self.SOTD_THREAD_PATTERNS if y in x.title.lower()
            ]
        ]

    def get_threads_from_last_month(self):
        """
        Return list of threads from previous month
        :return:
        """
        rec = self.get_x_most_recent_threads(120)
        return [x for x in rec if datetime.datetime.utcfromtimestamp(x.created_utc).month == self.last_month.month]

    def get_threads_for_given_month(self, given_month):
        """
        Return list of threads from previous month
        :return:
        """
        if not isinstance(given_month, datetime.date):
            raise AttributeError('Must pass in a datetime.date object')

        rec = self.praw.subreddit('wetshaving').search(
            query=self._get_sotd_query_str(given_month),
            limit=100,
        )

        return [
            x for x in rec if datetime.datetime.utcfromtimestamp(x.created_utc).month == given_month.month and [
                # filter out threads with SOTD flair that arent true SOTD threads
                y for y in self.SOTD_THREAD_PATTERNS if y in x.title.lower()
            ]
        ]

    def get_comments_for_given_month_cached(self, given_month):
        # be kind to reddit, persist results to disk so we dont hit it everytime we change the razor cleanup / processing

        def _get_comments(comment_list):
            # compatible with recursion / more comments objects
            collected_comments = []
            for x in comment_list:
                if isinstance(x, MoreComments):
                    collected_comments.extend(_get_comments(x.comments()))
                else:
                    try:
                        author = x.author.id if x.author else ''
                        comments.append((x.body, author))
                    except prawcore.exceptions.NotFound:
                        print('Missing comment')
                        pass

            return collected_comments


        cache_file = '{0}{1}{2}.cache'.format(self.CACHE_DIR, given_month.year, given_month.month)

        try:
            with open(cache_file, 'rb') as f_cache:
                return pickle.load(f_cache)
        except (FileNotFoundError, UnpicklingError):
            comments = []
            for thread in self.get_threads_for_given_month(given_month):
                print('Iterate day')
                comments.extend(_get_comments(thread.comments))
                print(len(comments))

            # dont cache current / future months
            if datetime.date.today().replace(day=1) > given_month.replace(day=1):
                with open(cache_file, 'wb') as f_cache:
                    pickle.dump(comments, f_cache)

            return comments



if __name__ == '__main__':
    # debug / testing
    pl = SotdPostLocator(praw.Reddit('standard_creds', user_agent='arach'))

    res = pl.get_threads_for_given_month(datetime.date(2019, 6, 1))

    # res = pl.get_threads_from_last_month()
    orderable = {x.created_utc: x.title for x in res}

    for sotd_date in sorted(orderable.keys()):
        print(sotd_date, orderable[sotd_date])
