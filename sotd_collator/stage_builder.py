import calendar
from genericpath import exists
from pprint import pprint
from dateutil import rrule
from datetime import date
from dateutil.relativedelta import relativedelta
import json
import os
import praw
from sotd_collator.blade_alternate_namer import BladeAlternateNamer
from sotd_collator.blade_name_extractor import BladeNameExtractor
from sotd_collator.brush_alternate_namer import BrushAlternateNamer
from sotd_collator.brush_name_extractor import BrushNameExtractor
from sotd_collator.cache_provider import CacheProvider
from sotd_collator.razor_alternate_namer import RazorAlternateNamer
from sotd_collator.razor_name_extractor import RazorNameExtractor

from sotd_collator.sotd_post_locator import SotdPostLocator
from sotd_collator.thread_cache_builder import ThreadCacheBuilder
from sotd_collator.utils import timer_func

class StageBuilder(object):

    __last_month = date.today().replace(day=1) - relativedelta(months=1)
    
    @timer_func
    def build_stage(self, start_month: date = None, end_month: date = None, force_refresh:bool=False):
        if start_month is None: start_month = self.__last_month
        if end_month is None: end_month = self.__last_month
        if (start_month > end_month): raise ValueError("Start month must be earlier than end month")
        print(f'staging comments for {start_month} to {end_month}')

        pr = praw.Reddit("reddit")
        pl = SotdPostLocator(pr)

        extractors = {
            "razor": [ RazorNameExtractor(), RazorAlternateNamer() ],
            "blade": [ BladeNameExtractor(), BladeAlternateNamer() ],
            "brush": [ BrushNameExtractor(), BrushAlternateNamer() ]
        }


        curr_month = start_month
        cached_files = {}
        for dirpath,dirname,filenames in os.walk('misc'):
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
            filename = '{0}{1}.json'.format(
                curr_month.year,
                curr_month.month if curr_month.month >= 10 else f'0{curr_month.month}'
            )

            if (force_refresh):
                try:
                    for file in cached_files[filename]:
                        os.remove(file)
                except Exception as error:
                    print(error)

            # threads = pl.get_threads_for_given_month(curr_month)
            comments = pl.get_comments_for_given_month_cached(curr_month)
            results = []
            for comment in comments:
                # body = comment["body"]
                match = False
                for label, extractor in extractors.items():
                    name = extractor[0].get_name(comment)
                    if name: 
                        match = True
                        comment[label] = name
                        # normalized = extractor[1].get_principal_name(name)
                        # if normalized:
                        #     comment['{0}_normalized'.format(label)] = normalized

                if match: results.append(comment)

            stage_file = 'misc/staged_comments/{0}'.format(filename)

            with open(stage_file, 'w') as f_stage:
                json.dump(results, f_stage, indent=4, sort_keys=False)

            comments_in += len(comments)
            comments_out += len(results)
            
            print('{0} - {1} comments in -> {2} comments out ({3}% reduction)'.format(
                format(curr_month),
                len(comments),
                len(results),
                round((len(results) - len(comments))/len(comments)*-100, 2)
            ))

            curr_month += relativedelta(months=1)
                
        print('Total - {0} comments in -> {1} comments out ({2}% reduction)'.format(
                comments_in,
                comments_out,
                round(comments_out - comments_in)/comments_in*-100, 2)
        )

    @timer_func
    def validate_stage(self, start_month: date = None, end_month: date = None):
        if start_month is None: start_month = self.__last_month
        if end_month is None: end_month = self.__last_month
        if (start_month > end_month): raise ValueError("Start month must be earlier than end month")
        print(f'validating staged comments for {start_month} to {end_month}')
        cp = CacheProvider()

        for m in rrule.rrule(rrule.MONTHLY, dtstart=start_month, until=end_month):
            threads = ThreadCacheBuilder().load(cp.get_thread_cache_file_path(m))
        #     thread_dict = {}
        #     # this isn't perfect since it may miss some of the special even threads
        #     # but it will at least make sure we have a thread per day
        #     for thread in threads: thread_dict[thread['created_utc'][0:10]] = thread

            for d in range(1, calendar.monthrange(m.year, m.month)[1]+1):
                dt = m.replace(day=d)
                title = dt.strftime('%A SOTD Thread - %b %d, %Y')
                thread_found = False
                for thread in threads:
                    if thread['title'].find(title) >= 0: 
                        thread_found = True
                        break
                if not thread_found: print(title)


if __name__ == '__main__':
    StageBuilder().build_stage(start_month=date(2023, 2, 1), end_month=date(2023, 2, 1), force_refresh=False)
