import calendar
import datetime
from numpy import empty

import praw
from dateutil.relativedelta import relativedelta


from sotd_collator.runner import Runner
from sotd_collator.sotd_post_locator import SotdPostLocator
from sotd_collator.stage_builder import StageBuilder
from sotd_collator.utils import extract_date_from_thread_title

runner = Runner()
pr = praw.Reddit("reddit")
pl = SotdPostLocator(pr)

# target = datetime.date(2023,12,1)
target = datetime.date.today().replace(day=1) - relativedelta(months=1)
last_month = target - relativedelta(months=1)
last_year = target - relativedelta(years=1)

sb = StageBuilder()
sb.build_stage(last_month, target)
sb.build_stage(last_year, last_year)

thread_map = pl.get_thread_map(last_year, last_year)
thread_map = thread_map | pl.get_thread_map(last_month, target)
day_map = {}
for d in range(1, calendar.monthrange(target.year, target.month)[1]+1):
    dd = datetime.date(target.year, target.month, d)
    day_map[dd] = dd

for id, thread in thread_map.items():
    dd = extract_date_from_thread_title(thread['title'])
    if dd in day_map:
        del day_map[dd]
    if len(day_map) == 0:
        break


missing = ''
missing_days = [d for d in day_map.values()]
missing_days_str = runner.list_to_english_string([d.strftime("%b %-d") for d in missing_days])

if len(missing_days) > 0:
    s0 = "threads"
    s1 = "those days"
    s2 = "any of those threads"
    if len(missing_days) == 1:
        s0 = "thread"
        s1 = "that day"
        s2 = "that thread"
    elif len(missing_days) == 2:
        s2 = "either of those threads"

    missing = f"\n\n* I was unable to find the SOTD {s0} for {missing_days_str}, so shaves from {s1} were not included. If you have a link to {s2}, please add it to the comments and I will rerun the report with it included."

comments_target = pl.get_comments_for_given_month_staged(target)
comments_last_month = pl.get_comments_for_given_month_staged(last_month)
comments_last_year = pl.get_comments_for_given_month_staged(last_year)

target_label = target.strftime("%B %Y")
last_month_label = last_month.strftime("%b %Y")
last_year_label = last_year.strftime("%b %Y")
shave_reports = f"{len(comments_target):,}"

header = f"""
Welcome to your SOTD Hardware Report for {target_label}

## Observations

* A fairly nondescript month


## Notes & Caveats

* {shave_reports} shave reports from {target_label} were analyzed to produce this report.{missing}

* I only show the top n results per category to keep the tables readable and avoid max post length issues.

* Blade Format stats don't differentiate between DE and half DE razors, they are all counted as being DE blades

* Blades recorded as just 'GEM' will be matched to 'Personna GEM PTFE' per guidance [here](https://www.reddit.com/r/Wetshaving/comments/19a43q7/comment/kil95r8/)

* Any brush with a DG knot will come under the DG Bx category - eg Dogwood B8 is recorded as 'DG B8'

* In the case of most brush makers (eg Maggard) - knots are split into synthetic / badger / boar and attributed to the maker - eg 'Maggard Synthetic'

* Notable exceptions to this are Omega and Semogue, in order to retain the model number. Unless someone just puts 'Omega Boar' which I then report as 'Omega (model not specified) Boar' .

* The unique user column shows the number of different users who used a given razor / brush etc in the month. We can combine this with the total number of shaves to get the average number of times a user used a razor / brush etc

* The change Δ vs columns show how an item has moved up or down the rankings since the previous month or year. = means no change in position, up or down arrows indicate how many positions up or down the rankings an item has moved compared to the previous month or year. n/a means the item was not present in the previous month / year.

"""

runner.run(
    header,
    thread_map,
    comments_target,
    comments_last_month,
    comments_last_year,
    last_month_label,
    last_year_label,
    5,  # min_shaves for most used blade in most userd razor
    2,  # min_unique users for most used blade in most userd razor),
    target,
    target,
)  
