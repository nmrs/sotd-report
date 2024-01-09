from pprint import pprint
import datetime
from tokenize import Comment
import praw
import json

from dateutil.relativedelta import relativedelta
from praw.models import Submission

from sotd_collator.thread_cache_builder import ThreadCacheBuilder

class CacheProvider(object):
    
    CACHE_DIR = "misc"

    def __init__(self, cache_dir:str=None):
        if cache_dir is not None: 
            self.CACHE_DIR = cache_dir
    
    def get_comment_cache_file_path(self, given_month: datetime.date) -> str:
        return self.__get_cache_file_path(given_month, "comments")

    def get_thread_cache_file_path(self, given_month: datetime.date) -> str:
        return self.__get_cache_file_path(given_month, "threads")
    
    def __get_cache_file_path(self, given_month: datetime.date, type: str) -> str:
            return '{0}/{1}/{2}{3}.{1}.json'.format(
                self.CACHE_DIR, 
                type,
                given_month.year, 
                given_month.month if given_month.month >= 10 else f'0{given_month.month}'
            )

class SotdPostLocator(object):
    """
    Get
    """

    SOTD_THREAD_PATTERNS = ['sotd thread', 'lather games']

    def __init__(self, praw: praw=None, cp: CacheProvider=None):
        self.praw = praw
        self.cache_provider = cp if cp != None else CacheProvider()

    # @property
    # def last_month(self):
    #     return datetime.date.today() - relativedelta(months=1)

    def _get_sotd_month_query_str(self, given_month: datetime.date):
        return "flair:SOTD {0} {1} {2} {2}SOTD".format(
            given_month.strftime('%b').lower(),
            given_month.strftime('%B').lower(),
            given_month.year
        )
    
    def get_threads_for_given_month(self, given_month: datetime.date) -> [Submission]:
        """
        Return list of threads from given month
        """
        if not isinstance(given_month, datetime.date):
            raise AttributeError('Must pass in a datetime.date object')

        cache_file = self.cache_provider.get_thread_cache_file_path(given_month)
        cached_threads = []
        threads = []
        cb = ThreadCacheBuilder()

        try:
            cached_threads = cb.load(cache_file)
        except (FileNotFoundError):
            pass
            # print(f'Cache miss for {cache_file}. Querying reddit.')
            # threads = self._get_threads_for_given_month(given_month)

        threads = self._get_threads_for_given_month_from_reddit(given_month)

        missing_threads = []
        if isinstance(cached_threads, list):
            for thread in cached_threads:
                if thread["id"] not in [t.id for t in threads if t.id == thread["id"]]:
                    missing_threads.append(praw.reddit.Submission(thread["id"]))
        
        
        if len(missing_threads) > 0:
            result = threads + missing_threads
            threads = result

        added = cb.dump(cache_file, threads)
        threads = sorted([t for t in added], key=lambda t : t.created_utc, reverse=True)
        for thread in threads:
            self._add_thread_comments_to_cache(thread, given_month)

        return threads
            
    def _get_threads_for_given_month_from_reddit(self, given_month: datetime.date) -> [Submission]:
        """
        Searches reddit to retrieve list of threads from given month
        """
        if not isinstance(given_month, datetime.date):
            raise AttributeError('Must pass in a datetime.date object')

        threads = []

        query = self._get_sotd_month_query_str(given_month)
        print(query)
        
        rec = self.praw.subreddit('wetshaving').search(
            query=query,
            sort='relevance',
            limit=None
        )  
        ids = []
        for thread in rec:
            created_utc = datetime.datetime.utcfromtimestamp(thread.created_utc)
            if created_utc.month == given_month.month and created_utc.year == given_month.year:
                for pattern in self.SOTD_THREAD_PATTERNS:
                    if pattern in thread.title.lower():
                        if thread.id not in ids:
                            ids.append(thread.id)
                            threads.append(thread)
                            # print(thread.title)

        return threads

    def _add_thread_comments_to_cache(self, thread: Submission, given_month: datetime.date):
        cache_file = self.cache_provider.get_comment_cache_file_path(given_month)
        cache = []
        try:
            with open(cache_file, 'r') as f_cache:
                cache = json.load(f_cache)
        except (FileNotFoundError, json.JSONDecodeError):
            pass

        # for comment in thread.comments.list():
        for comment in self._get_comments_for_threads([thread]):
            if comment["id"] not in [c["id"] for c in cache if c["id"] == comment["id"]]:
                cache.append(comment)

        with open(cache_file, 'w') as f_cache:
            json.dump(cache, f_cache, indent=4, sort_keys=True)
    
    def _comment_to_dict(self, comment: Comment) -> dict:
        """Converts a praw Comment to a dictionary for caching"""
        return {
                "author": comment.author.name if comment.author is not None else None,
                "body": comment.body,
                "created_utc": datetime.datetime.fromtimestamp(comment.created_utc).strftime("%Y-%m-%d %H:%M:%S"),
                "id": comment.id,
                "url": f"https://www.reddit.com/r/Wetshaving/comments/{comment.link_id.removeprefix('t3_')}/comment/{comment.id}/"
                }


    def get_comments_for_given_month_cached(self, given_month: datetime, force_refresh=False) -> [dict]:
        # be kind to reddit, persist results to disk so we dont hit it everytime we change the razor cleanup / processing

        if not isinstance(given_month, datetime.date):
            raise AttributeError('Must pass in a datetime.date object')

        cache_file = self.cache_provider.get_comment_cache_file_path(given_month)
        cache_miss = False
        comments = []
        if force_refresh:
            comments = self._get_comments_for_given_month(given_month)
        else:
            try:
                with open(cache_file, 'r') as f_cache:
                    comments = json.loads(f_cache.read())
            except (FileNotFoundError, json.JSONDecodeError):
                cache_miss = True
                print(f'Cache miss for {cache_file}. Querying reddit.')
                comments = self._get_comments_for_given_month(given_month)
        
        if force_refresh or cache_miss:
            with open(cache_file, 'w') as f_cache:
                json.dump(comments, f_cache, indent=4, sort_keys=True)
        
        return comments
    
    def _get_comments_for_threads(self, threads: [Submission]) -> [dict]:
        LINE_CLEAR = '\x1b[2K' # <-- ANSI sequence
        comments = []
        for thread in threads:
            for comment in thread.comments.list():
                if hasattr(comment, 'body') and comment.body != "[deleted]":
                    comments.append(self._comment_to_dict(comment))
                    print(end=LINE_CLEAR)
                    print(f'Loading comments for {thread.title}: {len(comments)} loaded', end='\r')
                     
        print(end=LINE_CLEAR)
        return comments

    def _get_comments_for_given_month(self, given_month: datetime.date) -> [Comment]:
        threads = self.get_threads_for_given_month(given_month)
        comments = self._get_comments_for_threads(threads)
        # print(f'Processed {format(given_month)} ({len(comments)} comments)')
        return comments

    def get_comments_for_given_year_cached(self, given_year: int) -> [dict]:
        collected_comments = []
        for m in range(1,13):
            collected_comments.extend(self.get_comments_for_given_month_cached(datetime.date(given_year, m, 1)))

        return collected_comments


if __name__ == '__main__':
    
    # debug / testing

    cp = CacheProvider()
    # with open(cp.get_thread_cache_file_path(datetime.date(2023, 12, 1)), 'r') as f_cache:
    #     cache = json.load(f_cache)
    #     pprint(cache)

    # print(cp.__get_cache_file_path(datetime.date.today(), 'comments'))
    

    # pr = praw.Reddit('reddit')
    # pl = SotdPostLocator(pr)

    # print(pl._get_sotd_month_query_str(pl.last_month))
    # pl.get_threads_from_last_month_cached()
    # res = pl.get_comments_for_given_day_cached(datetime.date(2021, 4, 30), filter_pattern='sotd', use_author_name=True)
    # print(res)
    # pl.get_threads_for_given_month(datetime.date(2023,5,1))
    # orderable = {x.created_utc: x.title for x in res}

    # for sotd_date in sorted(orderable.keys()):
    #     print(datetime.datetime.fromtimestamp(sotd_date).strftime("%Y-%m-%d %H:%M:%S"), orderable[sotd_date])