import calendar
import sys
from datetime import date
import json
import os
from dateutil import rrule
from dateutil.relativedelta import relativedelta
import praw

from cache_provider import CacheProvider
from blade_name_extractor import BladeNameExtractor
from brush_name_extractor import BrushNameExtractor
from razor_name_extractor import RazorNameExtractor

from sotd_post_locator import SotdPostLocator
from utils import timer_func


class StageBuilder(object):
    __last_month = date.today().replace(day=1) - relativedelta(months=1)

    @timer_func
    def build_stage(
        self,
        start_month: date = None,
        end_month: date = None,
        force_refresh: bool = False,
    ):
        if start_month is None:
            start_month = self.__last_month
        if end_month is None:
            end_month = self.__last_month
        if start_month > end_month:
            raise ValueError("Start month must be earlier than end month")
        print(f"staging comments for {start_month} to {end_month}")

        pr = praw.Reddit("reddit")
        pl = SotdPostLocator(pr)

        extractors = {
            "razor": RazorNameExtractor(),
            "blade": BladeNameExtractor(),
            "brush": BrushNameExtractor(),
            # "soap": SoapNameExtractor(),
        }

        curr_month = start_month
        cached_files = {}
        for dirpath, dirname, filenames in os.walk("cache"):
            for filename in filenames:
                path = os.path.join(dirpath, filename)
                if filename in cached_files:
                    cached_files[filename].append(path)
                else:
                    cached_files[filename] = [path]

        comments_in = 0
        comments_out = 0
        curr_month = start_month
        while curr_month <= end_month:
            filename = curr_month.strftime("%Y%m.json")

            if force_refresh:
                if filename in cached_files:
                    for file in cached_files[filename]:
                        os.remove(file)

            # threads = pl.get_threads_for_given_month(curr_month)\
            comments = pl.get_comments_for_given_month_cached(curr_month)
            results = []
            for comment in comments:
                # body = comment["body"]
                match = False
                for label, extractor in extractors.items():
                    name = extractor.get_name(comment)
                    if name:
                        match = True
                        comment[label] = name
                        # normalized = extractor[1].get_principal_name(name)
                        # if normalized:
                        #     comment['{0}_normalized'.format(label)] = normalized

                if match:
                    results.append(comment)

            stage_file = f"cache/staged_comments/{filename}"

            with open(stage_file, "w", encoding=sys.getdefaultencoding()) as f_stage:
                json.dump(results, f_stage, indent=4, sort_keys=False)

            comments_in += len(comments)
            comments_out += len(results)

            m = format(curr_month)
            cin = len(comments)
            cout = len(results)
            reduction = 0
            if cin > 0:
                reduction = round((cout - cin) / cin * -100, 2)

            print(
                f"{m} - {cin} comments in -> {cout} comments out ({reduction}% reduction)"
            )

            curr_month += relativedelta(months=1)

        cin = comments_in
        cout = comments_out
        reduction = 0
        if cin > 0:
            reduction = round((comments_out - comments_in) / comments_in * -100, 2)

        print(
            f"Total - {cin} comments in -> {cout} comments out ({reduction}% reduction)"
        )

    @timer_func
    def validate_stage(self, start_month: date = None, end_month: date = None):
        if start_month is None:
            start_month = self.__last_month
        if end_month is None:
            end_month = self.__last_month
        if start_month > end_month:
            raise ValueError("Start month must be earlier than end month")
        print(f"validating staged comments for {start_month} to {end_month}")
        cp = CacheProvider()

        for m in rrule.rrule(rrule.MONTHLY, dtstart=start_month, until=end_month):
            threads = []

            cache_file = cp.get_thread_cache_file_path(m)
            with open(cache_file, "r", encoding=sys.getdefaultencoding()) as f_cache:
                threads = json.load(f_cache)

            #     thread_dict = {}
            #     # this isn't perfect since it may miss some of the special even threads
            #     # but it will at least make sure we have a thread per day
            #     for thread in threads: thread_dict[thread['created_utc'][0:10]] = thread

            for d in range(1, calendar.monthrange(m.year, m.month)[1] + 1):
                dt = m.replace(day=d)
                title = dt.strftime("%A SOTD Thread - %b %d, %Y")
                thread_found = False
                for thread in threads:
                    if thread["title"].find(title) >= 0:
                        thread_found = True
                        break
                if not thread_found:
                    print(title)


if __name__ == "__main__":
    StageBuilder().build_stage(
        start_month=date(2024, 5, 1), end_month=date(2024, 5, 1), force_refresh=True
    )
    # StageBuilder().validate_stage(
    #     start_month=date(2022, 4, 1), end_month=date(2022, 5, 1)
    # )
