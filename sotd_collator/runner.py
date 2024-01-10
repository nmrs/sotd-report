import datetime
from pprint import pprint
import inflect
import pandas as pd

import praw
from dateutil.relativedelta import relativedelta
from pydantic import InstanceOf

from sotd_collator.blade_alternate_namer import BladeAlternateNamer
from sotd_collator.blade_format_extractor import BladeFormatExtractor
from sotd_collator.blade_name_extractor import BladeNameExtractor
from sotd_collator.brush_alternate_namer import BrushAlternateNamer
from sotd_collator.brush_name_extractor import BrushNameExtractor
from sotd_collator.karve_plate_extractor import KarvePlateExtractor
from sotd_collator.game_changer_plate_extractor import GameChangerPlateExtractor
from sotd_collator.knot_size_extractor import KnotSizeExtractor
from sotd_collator.knot_type_extractor import KnotTypeExtractor
from sotd_collator.razor_name_extractor import RazorNameExtractor
from sotd_collator.razor_alternate_namer import RazorAlternateNamer
from sotd_collator.razor_plus_blade_alternate_namer import RazorPlusBladeAlternateNamer
from sotd_collator.razor_plus_blade_name_extractor import RazorPlusBladeNameExtractor
from sotd_collator.sotd_post_locator import SotdPostLocator
from sotd_collator.staged_name_extractors import StagedBladeNameExtractor, StagedBrushNameExtractor, StagedRazorNameExtractor
from sotd_collator.utils import add_ranking_delta, get_shave_data, get_shave_data_for_month, get_shaving_histogram, get_entity_histogram

pr = praw.Reddit('reddit')
pl = SotdPostLocator(pr)
inf_engine = inflect.engine()

MAX_ENTITIES = 50
MIN_SHAVES = 5


process_entities = [
    {
        'name': 'Blade Format',
        'extractor': BladeFormatExtractor(),
        'renamer': None,
    },
    {
        'name': 'Razor',
        'extractor': StagedRazorNameExtractor(),
        'renamer': RazorAlternateNamer(),
        'max_entities': 50,
    },
    {
        'name': 'Blade',
        'extractor': StagedBladeNameExtractor(),
        'renamer': BladeAlternateNamer(),
        'max_entities': 30,

    },
    {
        'name': 'Brush',
        'extractor': StagedBrushNameExtractor(),
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
    {
        'name': 'Game Changer Plate',
        'extractor': GameChangerPlateExtractor(),
        'renamer': None,
    },
]

mode = "annual"

target = datetime.date(2023,12,1)
delta_one = target - relativedelta(years=1)
delta_two = target - relativedelta(years=5)

comments_target = pl.get_comments_for_given_year_staged(target.year)
comments_delta_one = pl.get_comments_for_given_year_staged(delta_one.year)
comments_delta_two = pl.get_comments_for_given_year_staged(delta_two.year)

target_label = target.strftime('%Y')
delta_one_label = delta_one.strftime('%Y')
delta_two_label = delta_two.strftime('%Y')

print(f"""
Welcome to your SOTD Hardware Report for {target_label}

## Observations

* A fairly nondescript month


## Notes & Caveats

* I only show the top n results per category to keep the tables readable and avoid max post length issues.

* Blade Format stats dont differentiate between DE and half DE razors, they are all counted as being DE blades

* Any brush with a DG knot will come under the DG Bx category - eg Dogwood B8 is recorded as 'DG B8'

* In the case of most brush makers (eg Maggard) - knots are split into synthetic / badger / boar and attributed to the maker - eg 'Maggard Synthetic'

* Notable exceptions to this are Omega and Semogue, in order to retain the model number. Unless some jerk just puts 'Omega Boar' which I then report as 'Omega Boar (model not specified)' .

* The unique user column shows the number of different users who used a given razor / brush etc in the month. We can combine this with the total number of shaves to get the average number of times a user used a razor / brush etc

* The change Δ vs columns show how an item has moved up or down the rankings since the previous month or year. = means no change in position, up or down arrows indicate how many positions up or down the rankings an item has moved compared to the previous month or year. n/a means the item was not present in the previous month / year.

""")

razor_usage = None
for entity in process_entities:
    print('##{0}\n'.format(inf_engine.plural(entity['name'])))

    # print(f'retrieving {target_label} usage', end='\r')
    usage = get_shave_data(comments_target, entity['extractor'], entity['renamer'])
    # print(f'retrieving {delta_one_label} usage', end='\r')
    pm_usage = get_shave_data(comments_delta_one, entity['extractor'], entity['renamer'])
    # print(f'retrieving {delta_two_label} usage', end='\r')
    py_usage = get_shave_data(comments_delta_two, entity['extractor'], entity['renamer'])


    # print(f'adding {delta_one_label} delta', end='\r')
    usage = add_ranking_delta(usage, pm_usage, delta_one_label)
    # print(f'adding {delta_two_label} delta', end='\r')
    usage = add_ranking_delta(usage, py_usage, delta_two_label)
    # print(f'dropping rank', end='\r')
    usage.drop('rank', inplace=True, axis=1)

    # remove nulls
    # print('removing nulls', end='\r')
    usage.dropna(subset=['name'], inplace=True)

    # sort
    # print('sorting', end='\r')
    usage.sort_values(['shaves', 'unique users'], ascending=False, inplace=True)

    # enforce max entities
    # print('enforcing max entities', end='\r')
    max_entities = entity['max_entities'] if 'max_entities' in entity else MAX_ENTITIES
    usage = usage.head(max_entities)

    print(usage.to_markdown(index=False))
    print('\n')

    if isinstance(entity["extractor"], StagedRazorNameExtractor):
        razor_usage = usage

print('## Most Used Blades in Most Used Razors\n')

# do razor plus blade combo, filtered on most popular razors...
# razor_usage = get_shave_data(comments_target, RazorNameExtractor(), RazorAlternateNamer())
rpb_usage = get_shave_data(comments_target, RazorPlusBladeNameExtractor(), RazorPlusBladeAlternateNamer())
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

print(rpb_usage.to_markdown(index=False))
print('\n')


# print('## Shaving Frequency Histogram\n')
# print(get_shaving_histogram(stats_month, pl).to_markdown(index=False))
# print('\n')



