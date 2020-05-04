import pickle
from pickle import UnpicklingError
from pprint import pprint

import pkg_resources
import praw
import datetime
from dateutil.relativedelta import *

class SotdPostLocator(object):
    """
    Get
    """

    THREAD_NAME_STR_PATTERN = ' SOTD Thread -'
    CACHE_DIR = pkg_resources.resource_filename('sotd_collator', '../misc/')

    def __init__(self, praw):
        self.praw = praw

    @property
    def last_month(self):
        return datetime.date.today() - relativedelta(months=2)

    def get_x_most_recent_threads(self, threads_to_fetch=50):
        res = self.praw.subreddit('wetshaving').search(
            query='"*SOTD Thread -"',
            limit=threads_to_fetch,
        )
        return [x for x in res if self.THREAD_NAME_STR_PATTERN in x.title]

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
            query='SOTD Thread {0} {1}'.format(given_month.strftime('%b'), given_month.year),
            limit=100,
        )

        return [x for x in rec if datetime.datetime.utcfromtimestamp(x.created_utc).month == given_month.month and self.THREAD_NAME_STR_PATTERN.lower() in x.title.lower()]

    def get_comments_for_given_month_cached(self, given_month):
        # be kind to reddit, persist results to disk so we dont hit it everytime we change the razor cleanup / processing
        cache_file = '{0}{1}{2}.cache'.format(self.CACHE_DIR, given_month.year, given_month.month)

        try:
            with open(cache_file, 'rb') as f_cache:
                return pickle.load(f_cache)
        except (FileNotFoundError, UnpicklingError):
            comments = []
            for thread in self.get_threads_for_given_month(given_month):
                print('Iterate day')
                for x in thread.comments:
                    author = x.author.id if x.author else ''
                    comments.append((x.body, author))
            # dont cache current / future months
            if datetime.date.today().replace(day=1) > given_month.replace(day=1):
                with open(cache_file, 'wb') as f_cache:
                    pickle.dump(comments, f_cache)

            return comments



if __name__ == '__main__':
    # debug / testing
    pl = SotdPostLocator(praw.Reddit('standard_creds', user_agent='arach'))

    res = pl.get_threads_for_given_month(datetime.date(2020, 4, 1))

    # res = pl.get_threads_from_last_month()
    orderable = {x.created_utc: x.title for x in res}

    for sotd_date in sorted(orderable.keys()):
        print(sotd_date, orderable[sotd_date])
