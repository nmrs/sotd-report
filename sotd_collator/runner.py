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
from sotd_collator.knot_type_extractor import KnotTypeExtractor
from sotd_collator.razor_name_extractor import RazorNameExtractor
from sotd_collator.razor_alternate_namer import RazorAlternateNamer
from sotd_collator.razor_plus_blade_alternate_namer import RazorPlusBladeAlternateNamer
from sotd_collator.razor_plus_blade_name_extractor import RazorPlusBladeNameExtractor
from sotd_collator.sotd_post_locator import SotdPostLocator
from sotd_collator.utils import add_ranking_delta, get_shave_data_for_month, get_shaving_histogram, get_entity_histogram

pr = praw.Reddit('standard_creds', user_agent='arach')
pl = SotdPostLocator(pr)
inf_engine = inflect.engine()

MAX_ENTITIES = 50
MIN_SHAVES = 5


process_entities = [
    # {
    #     'name': 'Knot Type',
    #     'extractor': KnotTypeExtractor(),
    #     'renamer': None,
    # },
    {
        'name': 'Razor',
        'extractor': RazorNameExtractor(),
        'renamer': RazorAlternateNamer(),
        'max_entities': 50,
    },
    {
        'name': 'Blade',
        'extractor': BladeNameExtractor(),
        'renamer': BladeAlternateNamer(),
        'max_entities': 30,

    },
    {
        'name': 'Brush',
        'extractor': BrushNameExtractor(),
        'renamer': BrushAlternateNamer(),
        'max_entites': 50,

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

stats_month = datetime.date(2022,3,1)
previous_month = stats_month - relativedelta(months=1)
previous_year = stats_month - relativedelta(months=12)

print("""
Welcome to your SOTD Hardware Report for {0}

## Observations

* Henson Al and Ti have the same number of shaves this month, but many people used the aluminium 

* Yates and Lupo rise up the rankings

* Superspeed moves ahead of Tech (!)

* Congrats to the SE mafia for getting GEM blades to the #2 spot

# A couple of folks went heavy on their Semogue 2022s in March

* Historically Maggard synthetics have been the most strongly represented budget brushes in the SOTD threads. Interesting to see Yaqi edging down into 3rd place this time.


## Notes & Caveats

* I only show the top n results per category to keep the tables readable and avoid max post length issues.

* Any brush with a DG knot will come under the DG Bx category - eg Dogwood B8 is recorded as 'DG B8'

* In the case of most brush makers (eg Maggard) - knots are split into synthetic / badger / boar and attributed to the maker - eg 'Maggard Synthetic'

* Notable exceptions to this are Omega and Semogue, in order to retain the model number. Unless some jerk just puts 'Omega Boar' which I then report as 'Omega Boar (model not specified)' .

* The unique user column shows the number of different users who used a given razor / brush etc in the month. We can combine this with the total number of shaves to get the average number of times a user used a razor / brush etc

* The change Δ vs columns show how an item has moved up or down the rankings since the previous month or year. = means no change in position, up or down arrows indicate how many positions up or down the rankings an item has moved compared to the previous month or year. n/a means the item was not present in the previous month / year.

""".format(stats_month.strftime('%b %Y')))

for entity in process_entities:
    usage = get_shave_data_for_month(stats_month, pl, entity['extractor'], entity['renamer'])
    pm_usage = get_shave_data_for_month(previous_month, pl, entity['extractor'], entity['renamer'])
    py_usage = get_shave_data_for_month(previous_year, pl, entity['extractor'], entity['renamer'])

    usage = add_ranking_delta(usage, pm_usage, previous_month.strftime('%b %Y'))
    usage = add_ranking_delta(usage, py_usage, previous_year.strftime('%b %Y'))
    usage.drop('rank', inplace=True, axis=1)




    # remove nulls
    usage.dropna(subset=['name'], inplace=True)

    # sort
    usage.sort_values(['shaves', 'unique users'], ascending=False, inplace=True)

    # enforce max entities
    max_entities = entity['max_entities'] if 'max_entities' in entity else MAX_ENTITIES
    usage = usage.head(max_entities)


    print('##{0}\n'.format(inf_engine.plural(entity['name'])))

    print(usage.to_markdown(showindex=False))
    print('\n')


print('## Most Used Blades in Most Used Razors\n')

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
print('\n')


print('## Shaving Frequency Histogram\n')
print(get_shaving_histogram(stats_month, pl).to_markdown(showindex=False))
print('\n')



