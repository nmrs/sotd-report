import datetime
import praw
import simplejson

from dateutil.relativedelta import relativedelta
from praw.models import Submission

class SotdPostLocator(object):
    """
    Get
    """

    SOTD_THREAD_PATTERNS = ['sotd thread', 'lather games']
    # CACHE_DIR = pkg_resources.resource_filename('sotd_collator', '../misc/')
    # CACHE_DIR = 'cache/'
    CACHE_DIR = 'misc'

    def __init__(self, praw=None):
        self.praw = praw

    @property
    def last_month(self):
        return datetime.date.today() - relativedelta(months=1)

    def _get_sotd_month_query_str(self, given_month):
        return "flair:SOTD {0} {1} {2} {2}SOTD".format(
            given_month.strftime('%b').lower(),
            given_month.strftime('%B').lower(),
            given_month.year
        )

    def get_threads_for_given_month_cached(self, given_month, force_refresh=False):
        """
        Return list of threads from given month
        :return:
        """
        if not isinstance(given_month, datetime.date):
            raise AttributeError('Must pass in a datetime.date object')

        cache_file = '{0}{1}{2}.threads.json'.format(self.CACHE_DIR + '/threads/', given_month.year, given_month.month if given_month.month >= 10 else f'0{given_month.month}')
        cache_miss = False
        threads = []
        if force_refresh:
            threads = self._get_threads_for_given_month(given_month)
        else:
            try:
                with open(cache_file, 'r') as f_cache:
                    threads = simplejson.loads(f_cache.read())
            except (FileNotFoundError):
                cache_miss = True
                print(f'Cache miss for {cache_file}. Querying reddit.')
                threads = self._get_threads_for_given_month(given_month)

        if force_refresh or cache_miss:
            submissions = [
                {
                    "id": thread.id,
                    "created_utc": datetime.datetime.fromtimestamp(thread.created_utc).strftime("%Y-%m-%d %H:%M:%S"),
                    "author": thread.author.name if thread.author is not None else None,
                    "title": thread.title,
                    "body": thread.selftext,
                    "url": thread.url,
                } for thread in threads
            ]            
            with open(cache_file, 'w') as f_cache:
                f_cache.write(simplejson.dumps(submissions, indent=4, sort_keys=True))
                f_cache.close()

        print(f'Processed {format(given_month.replace(day=1))} ({len(threads)} threads)')
        return threads
            
    def _get_threads_for_given_month(self, given_month):
        """
        Return list of threads from given month
        :return:
        """
        if not isinstance(given_month, datetime.date):
            raise AttributeError('Must pass in a datetime.date object')

        threads = []

        query = self._get_sotd_month_query_str(given_month)
        print(query)
        
        rec = self.praw.subreddit('wetshaving').search(
            query=query,
            sort='new',
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

        return threads

    def get_comments_for_given_month_cached(self, given_month, force_refresh=False):
        # be kind to reddit, persist results to disk so we dont hit it everytime we change the razor cleanup / processing

        if not isinstance(given_month, datetime.date):
            raise AttributeError('Must pass in a datetime.date object')

        cache_file = '{0}{1}{2}.comments.json'.format(self.CACHE_DIR + '/comments/', given_month.year, given_month.month if given_month.month >= 10 else f'0{given_month.month}')
        cache_miss = False
        comments = []
        if force_refresh:
            comments = self._get_comments_for_given_month(given_month)
        else:
            try:
                with open(cache_file, 'r') as f_cache:
                    comments = simplejson.loads(f_cache.read())
            except (FileNotFoundError):
                cache_miss = True
                print(f'Cache miss for {cache_file}. Querying reddit.')
                comments = self._get_comments_for_given_month(given_month)
        
        if force_refresh or cache_miss:
            with open(cache_file, 'w') as f_cache:
                f_cache.write(simplejson.dumps(comments, indent=4, sort_keys=True))
                f_cache.close()
        
        # else:
        #     print(f'Rehydrated {format(given_month)} ({len(comments)} comments)')
        
        # ('**[Jan. 31, 2023 - Soup is Done - 2nd Kill \'23](https://i.imgur.com/m5j4o4p.jpg)**\n\n* **Brush:** Maggard 24mm Marble Synthetic\n\n* **Razor:** Merkur 34C\n\n* **Blade:** Lord Platinum\n\n* **Lather:** Grooming Dept Veritas\n\n* **Post Shave:** Lucky Tiger Splash\n\n* **Post Shave:** Stirling Unscented Balm\n\n* **Fragrance:** Southern Witchcrafts Labyrinth EdP\n\n* **Grateful Dead:** [Crazy Fingers - One from the Vault 8/13/75](https://www.youtube.com/watch?v=_hi1nWaNvIY) \n\n----\n\nIt is complete. \n\n*Veritas*, despite its soupy controversy, was a most excellent soap to use. I am grateful for the shaves I had with it; you know the shaves you have where when you finish you say to yourself "this soap is awesome"? Well I had plenty of those with is stuff.\n\nI really enjoyed the earthy, cocoa-ness of *Veritas*, and on top of having excellent performance, the post shave and residual slickness were most pleasing to my standards. Glad it\'s gone, but also gonna miss it.\n\nI think I\'m gonna go on an Abbate y la Mantia spree next.\n\nPeace.\n\nAlso, imgur, WTF lemme load a picture pls.\n\nEdit: picture finally loaded', 'c7xhb')
        
        result = []
        for comment in comments:
            c = (comment["body"], comment["author"])
            result.append(c)
        return result

    def _get_comments_for_given_month(self, given_month):
        comments = []
        for submission in self.get_threads_for_given_month_cached(given_month, True):
            if isinstance(submission, dict): submission = Submission(self.praw, submission["id"])

            for comment in submission.comments.list():
                if hasattr(comment, 'body') and comment.body != "[deleted]":
                    sotd ={
                        "id": comment.id,
                        "created_utc": datetime.datetime.fromtimestamp(comment.created_utc).strftime("%Y-%m-%d %H:%M:%S"),
                        "author": comment.author.name if comment.author is not None else None,
                        "body": comment.body,
                        "link": f"https://www.reddit.com/r/Wetshaving/comments/{comment.link_id.removeprefix('t3_')}/comment/{comment.id}/"
                    }
                    comments.append(sotd)            
                    print('     ' + str(len(comments)), end='\r')
                    
        print(f'Processed {format(given_month)} ({len(comments)} comments)')
        return comments

    def get_comments_for_given_year_cached(self, given_year):
        collected_comments = []
        for m in range(1,13):
            collected_comments.extend(self.get_comments_for_given_month_cached(datetime.date(given_year, m, 1)))

        return collected_comments


if __name__ == '__main__':
    # debug / testing

    pr = praw.Reddit('reddit')
    pl = SotdPostLocator(pr)

    # print(pl._get_sotd_month_query_str(pl.last_month))
    # pl.get_threads_from_last_month_cached()
    # res = pl.get_comments_for_given_day_cached(datetime.date(2021, 4, 30), filter_pattern='sotd', use_author_name=True)
    # print(res)
    pl.get_threads_for_given_month_cached(datetime.date(2023,5,1))
    # orderable = {x.created_utc: x.title for x in res}

    # for sotd_date in sorted(orderable.keys()):
    #     print(datetime.datetime.fromtimestamp(sotd_date).strftime("%Y-%m-%d %H:%M:%S"), orderable[sotd_date])
