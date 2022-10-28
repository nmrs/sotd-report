import pickle
from pickle import UnpicklingError
from pprint import pprint
import inflect

import pkg_resources
import praw
import datetime

import prawcore
from dateutil.relativedelta import *
from praw.models import MoreComments

eng = inflect.engine()


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

    def _get_sotd_month_query_str(self, given_month):
        return 'flair_name:SOTD ({0} OR {1}) {2}'.format(
            given_month.strftime('%b').lower(),
            given_month.strftime('%B').lower(),
            given_month.year,
        )

    def _get_sotd_day_query_str(self, given_month):
        return '({0} OR {1}) ({2} OR {3} OR {4}) {5}'.format(
            given_month.strftime('%b').lower(),
            given_month.strftime('%B').lower(),
            given_month.day,
            str(given_month.day).zfill(2),
            eng.ordinal(given_month.day),
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
            query=self._get_sotd_month_query_str(given_month),
            sort='hot',
            limit=100,
        )

        return [
            x for x in rec if datetime.datetime.utcfromtimestamp(x.created_utc).month == given_month.month and [
                # filter out threads with SOTD flair that arent true SOTD threads
                y for y in self.SOTD_THREAD_PATTERNS if y in x.title.lower()
            ]
        ]

    def get_threads_for_given_day(self, given_day, **options):
        """
        Return list of threads from previous month
        :return:
        """
        if not isinstance(given_day, datetime.date):
            raise AttributeError('Must pass in a datetime.date object')

        print(self._get_sotd_day_query_str(given_day))
        rec = self.praw.subreddit('wetshaving').search(
            query=self._get_sotd_day_query_str(given_day),
            limit=10,
        )

        # print(list(rec)

        output = list()

        for x in rec:
            if 'filter_pattern' in options and options['filter_pattern'].lower() not in x.title.lower():
                continue
            elif (
                    datetime.datetime.utcfromtimestamp(x.created_utc).month == given_day.month
                and
                    datetime.datetime.utcfromtimestamp(x.created_utc).day == given_day.day
                and
                    datetime.datetime.utcfromtimestamp(x.created_utc).year == given_day.year
                and
                    [
                    # filter out threads with SOTD flair that arent true SOTD threads
                    y for y in self.SOTD_THREAD_PATTERNS if y in x.title.lower()
                ]
            ):
                output.append(x)
        for x in output:
            print(x.title)
        return output

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
                try:
                    comments.extend(_get_comments(thread.comments))
                except AttributeError:
                    pass
                print(len(comments))

            # dont cache current / future months
            if len(comments) > 2 and datetime.date.today().replace(day=1) > given_month.replace(day=1):
                with open(cache_file, 'wb') as f_cache:
                    pickle.dump(comments, f_cache)

            return comments

    def get_comments_for_given_day_cached(self, given_day, **options):
        # be kind to reddit, persist results to disk so we dont hit it everytime we change the razor cleanup / processing

        def _get_comments(comment_list):
            # compatible with recursion / more comments objects
            collected_comments = []
            for x in comment_list:
                if isinstance(x, MoreComments):
                    collected_comments.extend(_get_comments(x.comments()))
                else:
                    try:
                        if 'use_author_name' in options:
                            author = x.author.name if x.author else ''
                        else:
                            author = x.author.id if x.author else ''
                        comments.append((x.body, author))
                    except prawcore.exceptions.NotFound:
                        print('Missing comment')
                        pass

            return collected_comments

        cache_file = '{0}{1}{2}{3}.cache'.format(
            self.CACHE_DIR, given_day.year, str(given_day.month).zfill(2), str(given_day.day).zfill(2)
        )

        try:
            with open(cache_file, 'rb') as f_cache:
                return pickle.load(f_cache)
        except (FileNotFoundError, UnpicklingError):
            comments = []
            for thread in self.get_threads_for_given_day(given_day, **options):
                try:
                    comments.extend(_get_comments(thread.comments))
                except AttributeError:
                    pass

            if len(comments) > 2:
                with open(cache_file, 'wb') as f_cache:
                    pickle.dump(comments, f_cache)

            return comments

    def get_comments_for_given_year_cached(self, given_year):
        collected_comments = []
        for m in range(1,13):
            collected_comments.extend(self.get_comments_for_given_month_cached(datetime.date(given_year, m, 1)))

        return collected_comments


if __name__ == '__main__':
    # debug / testing
    pl = SotdPostLocator(praw.Reddit('standard_creds', user_agent='arach'))

    # res = pl.get_comments_for_given_day_cached(datetime.date(2021, 4, 30), filter_pattern='sotd', use_author_name=True)
    # print(res)
    res = pl.get_threads_for_given_month(datetime.date(2022,6,1))
    orderable = {x.created_utc: x.title for x in res}

    for sotd_date in sorted(orderable.keys()):
        print(sotd_date, orderable[sotd_date])
