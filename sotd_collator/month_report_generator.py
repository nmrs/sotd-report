import calendar
import datetime
from numpy import empty

import praw
from dateutil.relativedelta import relativedelta


from sotd_collator.runner import Runner
from sotd_collator.sotd_post_locator import SotdPostLocator
from sotd_collator.stage_builder import StageBuilder
from sotd_collator.utils import extract_date_from_thread_title

FORCE_REFRESH = False
TIME_PERIOD = "month"

runner = Runner()
pr = praw.Reddit("reddit")
pl = SotdPostLocator(pr)

target = datetime.date(2024, 2, 1)
# target = datetime.date.today().replace(day=1) - relativedelta(months=1)
delta_one = target - relativedelta(months=1)
delta_two = target - relativedelta(years=1)
delta_three = target - relativedelta(years=5)

sb = StageBuilder()
sb.build_stage(delta_one, target, FORCE_REFRESH)
sb.build_stage(delta_two, delta_two, FORCE_REFRESH)
sb.build_stage(delta_three, delta_three, FORCE_REFRESH)

thread_map = pl.get_thread_map(delta_three, delta_three)
thread_map = thread_map | pl.get_thread_map(delta_two, delta_two)
thread_map = thread_map | pl.get_thread_map(delta_one, target)

day_map = {}
for d in range(1, calendar.monthrange(target.year, target.month)[1] + 1):
    dd = datetime.date(target.year, target.month, d)
    day_map[dd] = dd

for id, thread in thread_map.items():
    dd = extract_date_from_thread_title(thread["title"])
    if dd in day_map:
        del day_map[dd]
    if len(day_map) == 0:
        break


missing = ""
missing_days = [d for d in day_map.values()]
missing_days_str = runner.list_to_english_string(
    [d.strftime("%b %-d") for d in missing_days]
)

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
comments_delta_one = pl.get_comments_for_given_month_staged(delta_one)
comments_delta_two = pl.get_comments_for_given_month_staged(delta_two)
comments_delta_three = pl.get_comments_for_given_month_staged(delta_three)

target_label = target.strftime("%B %Y")
delta_one_label = delta_one.strftime("%b %Y")
delta_two_label = delta_two.strftime("%b %Y")
delta_three_label = delta_three.strftime("%b %Y")
shave_reports = f"{len(comments_target):,}"

header = f"""
Welcome to your SOTD Hardware Report for {target_label}

## Observations

* A fairly nondescript {TIME_PERIOD}


## Notes & Caveats

* {shave_reports} shave reports from {target_label} were analyzed to produce this report.{missing}

* I only show the top n results per category to keep the tables readable and avoid max post length issues.

* Blade Format stats don't differentiate between DE and half DE razors, they are all counted as being DE blades

* Blades recorded as just 'GEM' will be matched to 'Personna GEM PTFE' per guidance [here](https://www.reddit.com/r/Wetshaving/comments/19a43q7/comment/kil95r8/)

* Any brush with a DG knot will come under the DG Bx category - eg Dogwood B8 is recorded as 'DG B8'

* In the case of most brush makers (eg Maggard) - knots are split into synthetic / badger / boar and attributed to the maker - eg 'Maggard Synthetic'

* Notable exceptions to this are Omega and Semogue, in order to retain the model number. Unless someone just puts 'Omega Boar' which I then report as 'Omega (model not specified) Boar' .

* The unique user column shows the number of different users who used a given razor / brush etc in the month. We can combine this with the total number of shaves to get the average number of times a user used a razor / brush etc

* The change Δ vs columns show how an item has moved up or down the rankings since that {TIME_PERIOD}. = means no change in position, up or down arrows indicate how many positions up or down the rankings an item has moved compared to that {TIME_PERIOD}. n/a means the item was not present in that {TIME_PERIOD}.

* I added a new table of "Highest Use Count per Blade". I'm not sure if this says more about the longevity of the blade or the tenacity of the user, so I'll leave that to you to assess.
"""

runner.run(
    header,
    thread_map,
    comments_target,
    comments_delta_one,
    comments_delta_two,
    comments_delta_three,
    delta_one_label,
    delta_two_label,
    delta_three_label,
    5,  # min_shaves for most used blade in most userd razor
    2,  # min_unique users for most used blade in most userd razor),
    target,
    target,
)
