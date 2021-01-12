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

# only report top x entities
MAX_ENTITIES = 50

stats_month = datetime.date(2020,12,1)
previous_month = stats_month - relativedelta(months=1)
previous_year = stats_month - relativedelta(months=12)

sne = SoapNameExtractor()
san = SoapAlternateNamer()
unique_soap_names = set()

for month in (stats_month, previous_month, previous_year):
    for comment, user_id in pl.get_comments_for_given_month_cached(month):
        unique_soap_names.add(sne.get_name(comment))

# pprint(unique_soap_names)
# pprint(sorted(san.tts_soaps))
#
san.prime_lookups(unique_soap_names)


fails = 0
for soap in unique_soap_names:
    res = san.get_principal_name(soap)
    if not res:
        fails += 1

print('number of misses: {0}'.format(fails))
    #print(soap, san.get_principal_name(soap))

process_entities = [
    {
        'name': 'Soap',
        'extractor': sne,
        'renamer': san,
    },
]

for entity in process_entities:
    usage = get_shave_data_for_month(stats_month, pl, entity['extractor'], entity['renamer'], name_fallback=False)
    pm_usage = get_shave_data_for_month(previous_month, pl, entity['extractor'], entity['renamer'], name_fallback=False)
    py_usage = get_shave_data_for_month(previous_year, pl, entity['extractor'], entity['renamer'], name_fallback=False)

    usage = add_ranking_delta(usage, pm_usage, previous_month.strftime('%b %Y'))
    usage = add_ranking_delta(usage, py_usage, previous_year.strftime('%b %Y'))
    usage.drop('rank', inplace=True, axis=1)

    # remove nulls
    usage.dropna(subset=['name'], inplace=True)

    # sort
    usage.sort_values(['shaves', 'unique users'], ascending=False, inplace=True)

    usage = usage.head(MAX_ENTITIES)

    print('##{0}\n'.format(inf_engine.plural(entity['name'])))

    print(usage.to_markdown(showindex=False))
    print('\n')


    # if not res:
    #     print(comment)
