import os
from pprint import pprint
import datetime
from tokenize import Comment
import praw
import json

from dateutil.relativedelta import relativedelta
from praw.models import Submission
from sotd_collator.blade_name_extractor import BladeNameExtractor
from sotd_collator.brush_name_extractor import BrushNameExtractor
from sotd_collator.cache_provider import CacheProvider
from sotd_collator.razor_name_extractor import RazorNameExtractor


class SotdPostLocator(object):
    """
    Get
    """

    SOTD_THREAD_PATTERNS = ["sotd thread", "lather games"]

    def __init__(self, praw: praw = None, cp: CacheProvider = None):
        self.praw = praw
        self.cache_provider = cp if cp != None else CacheProvider()

    # @property
    # def last_month(self):
    #     return datetime.date.today() - relativedelta(months=1)

    def _get_sotd_month_query_str(self, given_month: datetime.date):
        return "flair:SOTD {0} {1} {2} {2}SOTD".format(
            given_month.strftime("%b").lower(),
            given_month.strftime("%B").lower(),
            given_month.year,
        )

    def get_threads_for_given_month(self, given_month: datetime.date) -> [Submission]:
        """
        Return list of threads from given month
        """
        if not isinstance(given_month, datetime.date):
            raise AttributeError("Must pass in a datetime.date object")

        cache_file = self.cache_provider.get_thread_cache_file_path(given_month)
        cached_threads = []
        threads = []

        try:
            with open(cache_file, "r") as f_cache:
                cached_threads = json.load(f_cache)
        except FileNotFoundError:
            pass
            # print(f'Cache miss for {cache_file}. Querying reddit.')
            # threads = self._get_threads_for_given_month(given_month)

        threads = self._get_threads_for_given_month_from_reddit(given_month)

        # see if any new threads came back that we haven't seen before
        # and cache the comments for those threads
        for thread in threads:
            if thread.id not in [
                t["id"] for t in cached_threads if t["id"] == thread.id
            ]:
                self._add_thread_comments_to_cache(thread, given_month)

        # see if any we've seen any threads before that didn't
        # come back for whatever reason and add those back
        # into the results
        missing_threads = []
        for thread in cached_threads:
            if thread["id"] not in [t.id for t in threads if t.id == thread["id"]]:
                missing_threads.append(Submission(self.praw, id=thread["id"]))

        if len(missing_threads) > 0:
            threads = threads + missing_threads

        to_cache = []
        threads = sorted(threads, key=lambda x: x.created_utc)
        for thread in threads:
            to_cache.append(self._thread_to_dict(thread))

        with open(cache_file, "w") as f_cache:
            json.dump(to_cache, f_cache, indent=4, sort_keys=True)

        # threads = sorted([t for t in missing_threads], key=lambda t : t.created_utc, reverse=False)

        return threads

    def _get_threads_for_given_month_from_reddit(
        self, given_month: datetime.date
    ) -> [Submission]:
        """
        Searches reddit to retrieve list of threads from given month
        """
        if not isinstance(given_month, datetime.date):
            raise AttributeError("Must pass in a datetime.date object")

        threads = []

        query = self._get_sotd_month_query_str(given_month)
        print(query)

        rec = self.praw.subreddit("wetshaving").search(
            query=query, sort="relevance", limit=None
        )
        ids = []
        for thread in rec:
            created_utc = datetime.datetime.utcfromtimestamp(thread.created_utc)
            if (
                created_utc.month == given_month.month
                and created_utc.year == given_month.year
            ):
                for pattern in self.SOTD_THREAD_PATTERNS:
                    if pattern in thread.title.lower():
                        if thread.id not in ids:
                            ids.append(thread.id)
                            threads.append(thread)
                            # print(thread.title)

        return threads

    def _add_thread_comments_to_cache(
        self, thread: Submission, given_month: datetime.date
    ):
        cache_file = self.cache_provider.get_comment_cache_file_path(given_month)
        cache = []
        try:
            with open(cache_file, "r") as f_cache:
                cache = json.load(f_cache)
        except (FileNotFoundError, json.JSONDecodeError):
            pass

        # for comment in thread.comments.list():
        for comment in self._get_comments_for_threads([thread]):
            if comment["id"] not in [
                c["id"] for c in cache if c["id"] == comment["id"]
            ]:
                cache.append(comment)

        with open(cache_file, "w") as f_cache:
            json.dump(cache, f_cache, indent=4, sort_keys=True)

    def _comment_to_dict(self, comment: Comment) -> dict:
        """Converts a praw Comment to a dictionary for caching"""
        return {
            "author": comment.author.name if comment.author is not None else None,
            "body": comment.body,
            "created_utc": datetime.datetime.fromtimestamp(
                comment.created_utc
            ).strftime("%Y-%m-%d %H:%M:%S"),
            "id": comment.id,
            "url": f"https://www.reddit.com/r/Wetshaving/comments/{comment.link_id.removeprefix('t3_')}/comment/{comment.id}/",
        }

    def _thread_to_dict(self, thread: Submission) -> dict:
        return {
            "author": thread.author.name if thread.author is not None else None,
            "body": thread.selftext,
            "created_utc": datetime.datetime.fromtimestamp(thread.created_utc).strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "id": thread.id,
            "title": thread.title,
            "url": thread.url,
        }

    def get_comments_for_given_month_staged(
        self, given_month: datetime, force_refresh=False
    ) -> [dict]:
        if not isinstance(given_month, datetime.date):
            raise AttributeError("Must pass in a datetime.date object")

        stage_file = self.cache_provider.get_comment_stage_file_path(given_month)
        if force_refresh:
            os.remove(stage_file)

        try:
            with open(stage_file, "r") as f_cache:
                return json.loads(f_cache.read())
        except (FileNotFoundError, json.JSONDecodeError):
            self.get_comments_for_given_month_cached(given_month)
            return self.__stage_comments(given_month)

    def get_comments_for_given_month_cached(self, given_month: datetime.date) -> [dict]:
        # be kind to reddit, persist results to disk so we dont hit it everytime we change the razor cleanup / processing

        if not isinstance(given_month, datetime.date):
            raise AttributeError("Must pass in a datetime.date object")

        cache_file = self.cache_provider.get_comment_cache_file_path(given_month)
        cache_miss = False
        comments = []
        try:
            with open(cache_file, "r") as f_cache:
                comments = json.loads(f_cache.read())
        except (FileNotFoundError, json.JSONDecodeError):
            cache_miss = True
            print(f"Cache miss for {cache_file}. Querying reddit.")
            comments = self._get_comments_for_given_month(given_month)

            with open(cache_file, "w") as f_cache:
                json.dump(comments, f_cache, indent=4, sort_keys=True)

        return comments

    def __stage_comments(self, given_month: datetime.date) -> [dict]:
        extractors = {
            "razor": RazorNameExtractor(),
            "blade": BladeNameExtractor(),
            "brush": BrushNameExtractor(),
        }

        # threads = pl.get_threads_for_given_month(curr_month)
        comments = self.get_comments_for_given_month_cached(given_month)
        results = []
        for comment in comments:
            # body = comment["body"]
            match = False
            for label, extractor in extractors.items():
                val = extractor.get_name(comment)
                if val:
                    comment[label] = val
                    match = True
            if match:
                results.append(comment)

        stage_file = self.cache_provider.get_comment_stage_file_path(given_month)

        with open(stage_file, "w") as f_stage:
            json.dump(results, f_stage, indent=4, sort_keys=False)

        return results

    def _get_comments_for_threads(self, threads: [Submission]) -> [dict]:
        LINE_CLEAR = "\x1b[2K"  # <-- ANSI sequence
        comments = []
        for thread in threads:
            for comment in thread.comments.list():
                if hasattr(comment, "body") and comment.body != "[deleted]":
                    comments.append(self._comment_to_dict(comment))
                    print(end=LINE_CLEAR)
                    print(
                        f"Loading comments for {thread.title}: {len(comments)} loaded",
                        end="\r",
                    )

        print(end=LINE_CLEAR)
        return comments

    def _get_comments_for_given_month(self, given_month: datetime.date) -> [Comment]:
        threads = self.get_threads_for_given_month(given_month)
        comments = self._get_comments_for_threads(threads)
        # print(f'Processed {format(given_month)} ({len(comments)} comments)')
        return comments

    def get_comments_for_given_year_staged(self, given_year: int) -> [dict]:
        collected_comments = []
        for m in range(1, 13):
            collected_comments.extend(
                self.get_comments_for_given_month_staged(
                    datetime.date(given_year, m, 1)
                )
            )

        return collected_comments

    def get_comments_for_given_year_cached(self, given_year: int) -> [dict]:
        collected_comments = []
        for m in range(1, 13):
            collected_comments.extend(
                self.get_comments_for_given_month_cached(
                    datetime.date(given_year, m, 1)
                )
            )

        return collected_comments


if __name__ == "__main__":
    pr = praw.Reddit("reddit")
    pl = SotdPostLocator(pr)
    pl.manually_add_threads(["10wq1bw", "10xo5lt", "10yirpy"])
