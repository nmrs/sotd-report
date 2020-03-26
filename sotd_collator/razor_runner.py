import datetime
from collections import defaultdict
import praw

from sotd_collator.razor_name_extractor import RazorNameExtractor
from sotd_collator.razor_alternate_namer import RazorAlternateNamer
from sotd_collator.sotd_post_locator import SotdPostLocator


# only report razors with >= this many shaves
MIN_SHAVES = 5
raw_usage = defaultdict(int)
clustered_usage = defaultdict(int)

pr = praw.Reddit('standard_creds', user_agent='arach')
pl = SotdPostLocator(pr)
rn = RazorNameExtractor()
arn = RazorAlternateNamer()
#

"""
2016-06 Back in time
2016-08 Mongeese!
2016-10 People sure loved NEWs around this time. Maggard V3A gets popular.  
2017-02 WR1s for everyone
2017-03 6S going strong
2017-05 rise of the Guerilla 
2017-08 Guerilla, WR1 on top. Everyone gets into Super Adjustables?!
2018-01 Karve CB appears for the first time. WR1 still the most used razor.
2018-08 More folks are using straights than the most popular DE (WR1). ATT R1 is unusually popular
2018-10 Karve CB goes from 4th place previous month to first overall (although there are still more rockwells in total) WR2 appears for the first time 
2019-03 WR1 falls down the list. Karves, Rockwells and Techs are dominant
2019-06 RR GC .84 is very popular. WR2 usage exceeds WR1 for the first time
2019-08 Karve more popular than anything, even Rockwell 6C and 6S combined 
"""

stats_month = datetime.date(2019,8,1)

for comment in pl.get_comments_for_given_month_cached(stats_month):
    razor_name = rn.get_name(comment)
    if razor_name is not None:
        raw_usage[razor_name] += 1

total_shaves_for_month = 0

for razor_name, uses in raw_usage.items():
    if not razor_name:
        continue
    principal_name = arn.get_principal_name(razor_name)
    if principal_name:
        clustered_usage[principal_name] += uses
    else:
        # avoid nulls
        clustered_usage[razor_name] += uses
    total_shaves_for_month += uses


print('|Razor|Shaves in {0}|% of all shaves in {0}|'.format(stats_month.strftime('%b %Y')))
print('|---|---|---|')
for razor_name, num_shaves in sorted(clustered_usage.items(), key=lambda item: item[1], reverse=True):
    if num_shaves < MIN_SHAVES:
        continue
    print('|{0}|{1}|{2:0.2f}|'.format(*[razor_name, num_shaves, num_shaves * 100.0 / total_shaves_for_month]))
