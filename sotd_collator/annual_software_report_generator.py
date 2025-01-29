import calendar
import datetime
from numpy import empty

import praw
from dateutil.relativedelta import relativedelta


from soap_parser import SoapParser
from soap_runner import SoapRunner
from sotd_collator.runner import Runner
from sotd_collator.sotd_post_locator import SotdPostLocator
from sotd_collator.stage_builder import StageBuilder
from sotd_collator.utils import extract_date_from_thread_title
from staged_name_extractors import StagedSoapNameExtractor

FORCE_REFRESH = False
TIME_PERIOD = "year"

runner = SoapRunner()

pr = praw.Reddit("reddit")
pl = SotdPostLocator(pr)

# target = datetime.date(2023,12,1)
target = datetime.date(2024, 1, 1)
delta_one = target - relativedelta(years=1)
delta_two = target - relativedelta(years=3)
delta_three = target - relativedelta(years=5)

sb = StageBuilder()
# sb.build_stage(delta_one, target.replace(month=12), FORCE_REFRESH)
# sb.build_stage(delta_two, delta_two.replace(month=12), FORCE_REFRESH)
# sb.build_stage(delta_three, delta_three.replace(month=12), FORCE_REFRESH)

thread_map = pl.get_thread_map(delta_three, delta_three.replace(month=12))
thread_map = thread_map | pl.get_thread_map(delta_two, delta_two.replace(month=12))
thread_map = thread_map | pl.get_thread_map(delta_one, target.replace(month=12))

day_map = {}
for m in range(1, 13):
    for d in range(1, calendar.monthrange(target.year, m)[1] + 1):
        dd = datetime.date(target.year, m, d)
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

comments_target = pl.get_comments_for_given_year_staged(target.year)
comments_delta_one = pl.get_comments_for_given_year_staged(delta_one.year)
comments_delta_two = pl.get_comments_for_given_year_staged(delta_two.year)
comments_delta_three = pl.get_comments_for_given_year_staged(delta_three.year)

target_label = target.strftime("%Y")
delta_one_label = delta_one.strftime("%Y")
delta_two_label = delta_two.strftime("%Y")
delta_three_label = delta_three.strftime("%Y")
shave_reports = f"{len(comments_target):,}"

sne = StagedSoapNameExtractor()
snp = SoapParser()
brand_usage = runner.usage_for_field(
    thread_map,
    comments_target,
    comments_delta_one,
    comments_delta_two,
    comments_delta_three,
    delta_one_label,
    delta_two_label,
    delta_three_label,
    sne,
    snp,
    "brand",
    False,
)

print(f"brand usage: {brand_usage}")

scent_usage = runner.usage_for_field(
    thread_map,
    comments_target,
    comments_delta_one,
    comments_delta_two,
    comments_delta_three,
    delta_one_label,
    delta_two_label,
    delta_three_label,
    sne,
    snp,
    "name",
    False,
)

print(f"scent usage: {scent_usage}")


shavers = {}
for comment in comments_target:
    shavers[comment["author"]] = 0

header = f"""
Welcome to your SOTD Lather Log for {target_label}

* {shave_reports} shave reports from {len(shavers.keys())} distinct shavers during {target_label} were analyzed to produce this report. Collectively, these shavers used {len(scent_usage.index)} distinct soaps from {len(brand_usage.index)} distinct brands.

## Observations

* Somthing insightful

## Notes & Caveats

* I only show the top n results per category to keep the tables readable and avoid max post length issues.

* The unique user column shows the number of different users who used a given brand/soap/etc in the {TIME_PERIOD}.

* The Brand Diversity table details the number of distinct soaps used during the {TIME_PERIOD} from that particular brand.

* The change Δ vs columns show how an item has moved up or down the rankings since that {TIME_PERIOD}. = means no change in position, up or down arrows indicate how many positions up or down the rankings an item has moved compared to that {TIME_PERIOD}. n/a means the item was not present in that {TIME_PERIOD}.

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
    target + relativedelta(months=11),
)
