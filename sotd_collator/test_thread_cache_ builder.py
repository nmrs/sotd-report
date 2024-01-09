import datetime
import json
import praw
import shutil

from unittest import TestCase

from sotd_collator.sotd_post_locator import SotdPostLocator
from sotd_collator.thread_cache_builder import ThreadCacheBuilder


class TestThreadCacheBuilder(TestCase):

    longMessage = True

    def test_load_setup(self):
        cache_file_in = 'misc/test/test.threads.result.json'
        contents = None
        with open(cache_file_in, 'r') as f_cache:
            contents = json.load(f_cache)

    def test_load_submissions(self):
        cache_file_in = 'misc/test/test.threads.missing_threads.json'
        cb = ThreadCacheBuilder()
        threads = cb.load(cache_file_in)
        self.assertEqual(len(threads), 31)

        from_reddit = SotdPostLocator(praw.Reddit('reddit'))._get_threads_for_given_month_from_reddit(datetime.date(2023, 12, 1))
        self.assertEqual(len(from_reddit), 31)

    def test_load_add_submission(self):
        cache_file_in = 'misc/test/test.threads.empty_added.json'
        cache_file_out = 'misc/test/test.threads.temp.json'
        cache_file_result = 'misc/test/test.threads.result.json'
        cb = ThreadCacheBuilder()
        threads = cb.load(cache_file_in)
        self.assertEqual(len(threads), 29)

        from_reddit = SotdPostLocator(praw.Reddit('reddit'))._get_threads_for_given_month_from_reddit(datetime.date(2023, 12, 1))
        self.assertEqual(len(from_reddit), 31)

        shutil.copy(cache_file_in, cache_file_out)

        a = None
        b = None
        cb.dump(cache_file_out, from_reddit)

        with open(cache_file_out, 'r') as f_cache:
            a = f_cache.read()
        
        with open(cache_file_result, 'r') as f_cache:
            b = f_cache.read()
        
        self.assertEqual(a, b)

if __name__ == '__main__':
    TestThreadCacheBuilder().test_load_add_submission()