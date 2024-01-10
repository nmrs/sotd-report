from curses import noraw
import datetime
from datetime import date
from time import time
from dateutil.relativedelta import relativedelta
import json
import praw
from sotd_collator.blade_alternate_namer import BladeAlternateNamer
from sotd_collator.blade_name_extractor import BladeNameExtractor
from sotd_collator.brush_alternate_namer import BrushAlternateNamer
from sotd_collator.brush_name_extractor import BrushNameExtractor
from sotd_collator.razor_alternate_namer import RazorAlternateNamer
from sotd_collator.razor_name_extractor import RazorNameExtractor

from sotd_collator.sotd_post_locator import SotdPostLocator

def timer_func(func): 
    # This function shows the execution time of  
    # the function object passed 
    def wrap_func(*args, **kwargs): 
        t1 = time() 
        result = func(*args, **kwargs) 
        t2 = time() 
        print(f'Function {func.__name__!r} executed in {(t2-t1):.4f}s') 
        return result 
    return wrap_func 

@timer_func
def build_stage():
    start_month = curr_month = datetime.date(2016,5,1)
    # start_month = curr_month = datetime.date(2019,11,1)
    # end_month = datetime.date(2016,5,1)
    end_month = date.today().replace(day=1) - relativedelta(months=1)
    print(f'staging comments for {start_month} to {end_month}')

    pr = praw.Reddit("reddit")
    pl = SotdPostLocator(pr)

    extractors = {
        "razor": [ RazorNameExtractor(), RazorAlternateNamer() ],
        "blade": [ BladeNameExtractor(), BladeAlternateNamer() ],
        "brush": [ BrushNameExtractor(), BrushAlternateNamer() ]
    }

    comments_in = 0
    comments_out = 0
    while curr_month <= end_month:  
        # threads = pl.get_threads_for_given_month(curr_month)
        comments = pl.get_comments_for_given_month_cached(curr_month, False)
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

        stage_file = 'misc/staged_comments/{0}{1}.json'.format(
            curr_month.year,
            curr_month.month if curr_month.month >= 10 else f'0{curr_month.month}'
        )
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

if __name__ == '__main__':
    build_stage()
