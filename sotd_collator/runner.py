import datetime
from pprint import pprint
import inflect
import pandas as pd

import praw
from dateutil.relativedelta import relativedelta

from sotd_collator.blade_alternate_namer import BladeAlternateNamer
from sotd_collator.blade_name_extractor import BladeNameExtractor
from sotd_collator.brush_alternate_namer import BrushAlternateNamer
from sotd_collator.brush_name_extractor import BrushNameExtractor
from sotd_collator.karve_plate_extractor import KarvePlateExtractor
from sotd_collator.knot_size_extractor import KnotSizeExtractor
from sotd_collator.razor_name_extractor import RazorNameExtractor
from sotd_collator.razor_alternate_namer import RazorAlternateNamer
from sotd_collator.razor_plus_blade_alternate_namer import RazorPlusBladeAlternateNamer
from sotd_collator.razor_plus_blade_name_extractor import RazorPlusBladeNameExtractor
from sotd_collator.sotd_post_locator import SotdPostLocator
from sotd_collator.utils import add_ranking_delta, get_shave_data_for_month, get_shaving_histogram, get_entity_histogram

pr = praw.Reddit('standard_creds', user_agent='arach')
pl = SotdPostLocator(pr)
inf_engine = inflect.engine()

# only report entities with >= this many shaves
MIN_SHAVES = 5



process_entities = [

    {
        'name': 'Razor',
        'extractor': RazorNameExtractor(),
        'renamer': RazorAlternateNamer(),
    },
    {
        'name': 'Blade',
        'extractor': BladeNameExtractor(),
        'renamer': BladeAlternateNamer(),
    },
    {
        'name': 'Brush',
        'extractor': BrushNameExtractor(),
        'renamer': BrushAlternateNamer(),
    },
    {
        'name': 'Knot Size',
        'extractor': KnotSizeExtractor(),
        'renamer': None,
    },
    {
        'name': 'Karve Plate',
        'extractor': KarvePlateExtractor(),
        'renamer': None,
    },
]

stats_month = datetime.date(2020,9,1)
previous_month = stats_month - relativedelta(months=1)
previous_year = stats_month - relativedelta(months=12)


# do razor plus blade combo, filtered on most popular razors...
razor_usage = get_shave_data_for_month(stats_month, pl, RazorNameExtractor(), RazorAlternateNamer())
rpb_usage = get_shave_data_for_month(stats_month, pl, RazorPlusBladeNameExtractor(), RazorPlusBladeAlternateNamer())
razor_usage.sort_values(['shaves', 'unique users'], ascending=False, inplace=True)

# get most popular razors in use this month
top_x_razors = razor_usage.head(10).loc[:, ['name']]
top_x_razors.columns = ['razor_name']

# extract razor name from combined razor + blades df
rpb_usage.loc[:, 'razor_name'] = rpb_usage['name'].apply(lambda x: x.split('+')[0].strip())
rpb_usage.sort_values(['shaves', 'unique users'], ascending=False, inplace=True)

rpb_usage = pd.merge(
    left=rpb_usage,
    right=top_x_razors,
    on='razor_name',
    how='inner'
).drop(['rank', 'razor_name'], axis=1)

rpb_usage = rpb_usage.where(rpb_usage['shaves'] >= MIN_SHAVES).where(rpb_usage['unique users'] > 1).dropna()

print(rpb_usage.to_markdown(showindex=False))
exit()

for entity in process_entities:
    usage = get_shave_data_for_month(stats_month, pl, entity['extractor'], entity['renamer'])
    pm_usage = get_shave_data_for_month(previous_month, pl, entity['extractor'], entity['renamer'])
    py_usage = get_shave_data_for_month(previous_year, pl, entity['extractor'], entity['renamer'])

    usage = add_ranking_delta(usage, pm_usage, previous_month.strftime('%b %Y'))
    usage = add_ranking_delta(usage, py_usage, previous_year.strftime('%b %Y'))
    usage.drop('rank', inplace=True, axis=1)

    # enforce min shaves
    usage = usage.where(usage['shaves'] >= MIN_SHAVES)

    # remove nulls
    usage.dropna(subset=['name'], inplace=True)

    # sort
    usage.sort_values(['shaves', 'unique users'], ascending=False, inplace=True)

    print('##{0}\n'.format(inf_engine.plural(entity['name'])))

    print(usage.to_markdown(showindex=False))
    print('\n')

print('## Shaving Frequency Histogram\n')
print(get_shaving_histogram(stats_month, pl).to_markdown(showindex=False))
print('\n')

print('## Razor Frequency Histogram\n')
print(get_entity_histogram(stats_month, pl, RazorNameExtractor(), RazorAlternateNamer(), 'Razors').to_markdown(showindex=False))
print('\n')

print('## Brush Frequency Histogram\n')
print(get_entity_histogram(stats_month, pl, BrushNameExtractor(), BrushAlternateNamer(), 'Brushes').to_markdown(showindex=False))
print('\n')


