import datetime
from collections import defaultdict
import praw

from sotd_collator.blade_name_extractor import BladeNameExtractor
from sotd_collator.blade_alternate_namer import BladeAlternateNamer
from sotd_collator.sotd_post_locator import SotdPostLocator


# only report blades with >= this many shaves
MIN_SHAVES = 5
raw_usage = defaultdict(int)
clustered_usage = defaultdict(int)

pr = praw.Reddit('standard_creds', user_agent='arach')
pl = SotdPostLocator(pr)
ne = BladeNameExtractor()
an = BladeAlternateNamer()
#

"""
"""

stats_month = datetime.date(2019,6,1)

for comment in pl.get_comments_for_given_month_cached(stats_month):
    blade_name = ne.get_name(comment)
    if blade_name is not None:
        raw_usage[blade_name] += 1

total_shaves_for_month = 0

for blade_name, uses in raw_usage.items():
    if not blade_name:
        continue
    principal_name = an.get_principal_name(blade_name)
    if principal_name:
        clustered_usage[principal_name] += uses
    else:
        # avoid nulls
        clustered_usage[blade_name] += uses
    total_shaves_for_month += uses


print('|blade|Shaves in {0}|% of all shaves in {0}|'.format(stats_month.strftime('%b %Y')))
print('|---|---|---|')
for blade_name, num_shaves in sorted(clustered_usage.items(), key=lambda item: item[1], reverse=True):
    if num_shaves < MIN_SHAVES:
        continue
    print('|{0}|{1}|{2:0.2f}|'.format(*[blade_name, num_shaves, num_shaves * 100.0 / total_shaves_for_month]))
