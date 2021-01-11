import datetime
from pprint import pprint
import inflect
import pandas as pd

import praw
from dateutil.relativedelta import relativedelta

from sotd_collator.soap_name_extractor import SoapNameExtractor
from sotd_collator.soap_alternate_namer import SoapAlternateNamer
from sotd_collator.sotd_post_locator import SotdPostLocator
from sotd_collator.utils import add_ranking_delta, get_shave_data_for_month, get_shaving_histogram, get_entity_histogram

pr = praw.Reddit('standard_creds', user_agent='arach')
pl = SotdPostLocator(pr)
inf_engine = inflect.engine()

# only report entities with >= this many shaves
MIN_SHAVES = 5

stats_month = datetime.date(2020,12,1)
previous_month = stats_month - relativedelta(months=1)
previous_year = stats_month - relativedelta(months=12)

sn = SoapNameExtractor()
san = SoapAlternateNamer()
unique_soap_names = set()

for comment, user_id in pl.get_comments_for_given_month_cached(stats_month):
    unique_soap_names.add(sn.get_name(comment))

# pprint(unique_soap_names)
# pprint(sorted(san.tts_soaps))
#
# exit()
san.prime_lookups(unique_soap_names)

fails = 0
for soap in unique_soap_names:
    res = san.get_principal_name(soap)
    if not res:
        fails += 1

print('number of misses: {0}'.format(fails))
    #print(soap, san.get_principal_name(soap))



    # if not res:
    #     print(comment)
