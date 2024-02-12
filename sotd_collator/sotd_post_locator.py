import os
from datetime import datetime, date
import re
import time
from typing import List
from uu import Error
from dateutil import rrule
import sys
from tokenize import Comment
import json
from numpy import empty

import praw
from praw import models
from praw.models import Comment, MoreComments, Submission

from sotd_collator.blade_name_extractor import BladeNameExtractor
from sotd_collator.brush_name_extractor import BrushNameExtractor
from sotd_collator.cache_provider import CacheProvider
from sotd_collator.razor_name_extractor import RazorNameExtractor


class SotdPostLocator(object):
    """
    Get
    """

    SOTD_THREAD_PATTERNS = ["sotd thread", "lather games"]

    def __init__(self, reddit: praw = None, cp: CacheProvider = None):
        self.reddit = reddit
        self.cache_provider = cp if cp is not None else CacheProvider()

    # @property
    # def last_month(self):
    #     return datetime.date.today() - relativedelta(months=1)

    def _get_sotd_month_query_str(self, given_month: date):
        month_abbr = given_month.strftime("%b").lower()
        month_full = given_month.strftime("%B").lower()
        year = given_month.year
        return f"flair:SOTD {month_abbr} {month_full} {year} {year}SOTD"

    def get_threads_for_given_month_cached(self, given_month: date) -> List[dict]:
        if not isinstance(given_month, date):
            raise AttributeError("Must pass in a datetime.date object")

        cache_file = self.cache_provider.get_thread_cache_file_path(given_month)

        with open(cache_file, "r", encoding=sys.getdefaultencoding()) as f_cache:
            return json.load(f_cache)

    def get_thread_map(self, start_month, end_month):
        result = {}
        for m in rrule.rrule(rrule.MONTHLY, dtstart=start_month, until=end_month):
            for thread in self.get_threads_for_given_month_cached(m):
                result[thread["id"]] = thread

        return result

    def get_threads_for_given_month(self, given_month: date) -> List[Submission]:
        """
        Return list of threads from given month
        """
        if not isinstance(given_month, date):
            raise AttributeError("Must pass in a datetime.date object")

        cache_file = self.cache_provider.get_thread_cache_file_path(given_month)
        cached_threads = []
        threads = []

        try:
            with open(cache_file, "r", encoding=sys.getdefaultencoding()) as f_cache:
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
                missing_threads.append(Submission(self.reddit, id=thread["id"]))

        if len(missing_threads) > 0:
            threads = threads + missing_threads

        to_cache = []
        threads = sorted(threads, key=lambda x: x.created_utc)
        for thread in threads:
            to_cache.append(self._thread_to_dict(thread))

        with open(cache_file, "w", encoding=sys.getdefaultencoding()) as f_cache:
            json.dump(to_cache, f_cache, indent=4, sort_keys=True)

        return threads

    def _get_threads_for_given_month_from_reddit(
        self, given_month: date
    ) -> List[Submission]:
        """
        Searches reddit to retrieve list of threads from given month
        """
        if not isinstance(given_month, date):
            raise AttributeError("Must pass in a datetime.date object")

        threads = []

        query = self._get_sotd_month_query_str(given_month)
        print(query)

        rec = self.reddit.subreddit("wetshaving").search(
            query=query, sort="relevance", limit=None
        )
        ids = []
        for thread in rec:
            created_utc = datetime.utcfromtimestamp(thread.created_utc)
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

        month = given_month.strftime("%Y-%m")
        manual_threads = []
        with open(
            "cache/threads/manual.json", "r", encoding=sys.getdefaultencoding()
        ) as f:
            manual = json.load(f)
            for thread in manual:
                if thread["date"].startswith(month):
                    manual_threads.append(thread)

        threads = [t for t in threads]

        for m in manual_threads:
            found = False
            for t in threads:
                if m["id"] == t.id:
                    found = True
                    break
            if not found and m["id"] != "":
                threads.append(Submission(self.reddit, id=m["id"]))

        return sorted(threads, key=lambda x: x.created_utc, reverse=False)

    def _add_thread_comments_to_cache(self, thread: Submission, given_month: date):
        cache_file = self.cache_provider.get_comment_cache_file_path(given_month)
        cache = []
        try:
            with open(cache_file, "r", encoding=sys.getdefaultencoding()) as f_cache:
                cache = json.load(f_cache)
        except (FileNotFoundError, json.JSONDecodeError):
            pass

        # for comment in thread.comments.list():
        for comment in self._get_comments_for_threads([thread]):
            if comment["id"] not in [
                c["id"] for c in cache if c["id"] == comment["id"]
            ]:
                cache.append(comment)

        with open(cache_file, "w", encoding=sys.getdefaultencoding()) as f_cache:
            json.dump(cache, f_cache, indent=4, sort_keys=True)

    def _comment_to_dict(self, comment: models.Comment) -> dict:
        """Converts a praw Comment to a dictionary for caching"""
        base = "www.reddit.com/r/Wetshaving/comments"
        return {
            "author": comment.author.name if comment.author is not None else None,
            "body": comment.body,
            "created_utc": datetime.fromtimestamp(comment.created_utc).strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "id": comment.id,
            "url": f"https://{base}/{comment.link_id.removeprefix('t3_')}/comment/{comment.id}/",
        }

    def _thread_to_dict(self, thread: Submission) -> dict:
        return {
            "author": thread.author.name if thread.author is not None else None,
            "body": thread.selftext,
            "created_utc": datetime.fromtimestamp(thread.created_utc).strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "id": thread.id,
            "title": thread.title,
            "url": thread.url,
        }

    def get_comments_for_given_month_staged(
        self, given_month: datetime, force_refresh=False
    ) -> List[dict]:
        if not isinstance(given_month, date):
            raise AttributeError("Must pass in a datetime.date object")

        stage_file = self.cache_provider.get_comment_stage_file_path(given_month)
        if force_refresh:
            os.remove(stage_file)

        try:
            with open(stage_file, "r", encoding=sys.getdefaultencoding()) as f_cache:
                return json.loads(f_cache.read())
        except (FileNotFoundError, json.JSONDecodeError):
            self.get_comments_for_given_month_cached(given_month)
            return self.__stage_comments(given_month)

    def get_comments_for_given_month_cached(self, given_month: date) -> List[dict]:
        # be kind to reddit, persist results to disk
        # so we dont hit it everytime we change the razor cleanup / processing

        if not isinstance(given_month, date):
            raise AttributeError("Must pass in a datetime.date object")

        cache_file = self.cache_provider.get_comment_cache_file_path(given_month)
        comments = []
        try:
            with open(cache_file, "r", encoding=sys.getdefaultencoding()) as f_cache:
                comments = json.loads(f_cache.read())
        except (FileNotFoundError, json.JSONDecodeError):
            print(f"Cache miss for {cache_file}. Querying reddit.")
            comments = self._get_comments_for_given_month(given_month)

            with open(cache_file, "w", encoding=sys.getdefaultencoding()) as f_cache:
                json.dump(comments, f_cache, indent=4, sort_keys=True)

        return comments

    def __stage_comments(self, given_month: date) -> List[dict]:
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

        with open(stage_file, "w", encoding=sys.getdefaultencoding()) as f_stage:
            json.dump(results, f_stage, indent=4, sort_keys=False)

        return results

    def _get_comments_for_threads(self, threads: List[Submission]) -> List[dict]:
        line_clear = "\x1b[2K"  # <-- ANSI sequence
        comments = []
        for thread in threads:
            thread.comments.replace_more()
            for comment in thread.comments.list():
                if comment.parent_id == comment.link_id:
                    if hasattr(comment, "body") and comment.body != "[deleted]":
                        comments.append(self._comment_to_dict(comment))
                        print(end=line_clear)
                        print(
                            f"Loading comments for {thread.title}: {len(comments)} loaded",
                            end="\r",
                        )

        print(end=line_clear)
        return comments

    def _get_comments_for_threadsX(self, threads: List[Submission]) -> List[dict]:
        LINE_CLEAR = "\x1b[2K"  # <-- ANSI sequence

        def _get_comments(comment_list):
            # compatible with recursion / more comments objects
            collected_comments = []
            for x in comment_list:
                if isinstance(x, MoreComments):
                    collected_comments.extend(_get_comments(x.comments()))
                else:
                    if comment.parent_id == comment.link_id:
                        if hasattr(comment, "body") and comment.body != "[deleted]":
                            collected_comments.append(comment)

            return collected_comments
        
        comments = []
        for thread in threads:
            for comment in thread.comments:
                comments.extend(_get_comments(thread.comments))
                print(end=LINE_CLEAR)
                print(
                    f"Loading comments for {thread.title}: {len(comments)} loaded",
                    end="\r",
                )

        dedupe_map = {}
        for comment in comments:
            if comment.id not in dedupe_map:
                dedupe_map[comment.id] = self._comment_to_dict(comment)

        return [x for x in dedupe_map.values()]


    def _get_comments_for_given_month(self, given_month: date, max_retries=10) -> List[models.Comment]:
        if max_retries == 0:
            threads = self.get_threads_for_given_month(given_month)
            comments = self._get_comments_for_threads(threads)
            return comments
        else:
            try:
                threads = self.get_threads_for_given_month(given_month)
                comments = self._get_comments_for_threads(threads)
                return comments
            except Exception as error:
                print(error)
                print(f'retrying. {max_retries} more attempts')
                time.sleep((11-max_retries)*2)
                return self._get_comments_for_given_month(self, given_month, max_retries-1)

        # print(f'Processed {format(given_month)} ({len(comments)} comments)')


    def get_comments_for_given_year_staged(self, given_year: int) -> List[dict]:
        collected_comments = []
        for m in range(1, 13):
            collected_comments.extend(
                self.get_comments_for_given_month_staged(date(given_year, m, 1))
            )

        return collected_comments

    def get_comments_for_given_year_cached(self, given_year: int) -> List[dict]:
        collected_comments = []
        for m in range(1, 13):
            collected_comments.extend(
                self.get_comments_for_given_month_cached(date(given_year, m, 1))
            )

        return collected_comments


if __name__ == "__main__":
    pr = praw.Reddit("reddit")
    pl = SotdPostLocator(pr)
    pl.manually_add_threads(["10wq1bw", "10xo5lt", "10yirpy"])
