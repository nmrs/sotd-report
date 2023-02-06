import inflect
import pandas as pd

import praw

from sotd_collator.blade_alternate_namer import BladeAlternateNamer
from sotd_collator.blade_format_extractor import BladeFormatExtractor
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
from sotd_collator.utils import add_ranking_delta, get_shave_data_for_year

pr = praw.Reddit('standard_creds', user_agent='arach')
pl = SotdPostLocator(pr)
inf_engine = inflect.engine()

# only report entities with >= this many shaves
MIN_SHAVES = 50
MAX_ENTITIES = 50



process_entities = [
    {
        'name': 'Blade Format',
        'extractor': BladeFormatExtractor(),
        'renamer': None,
    },
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

stats_year = 2022
previous_year = stats_year - 1



for entity in process_entities:
    usage = get_shave_data_for_year(stats_year, pl, entity['extractor'], entity['renamer'])
    py_usage = get_shave_data_for_year(previous_year, pl, entity['extractor'], entity['renamer'])

    usage = add_ranking_delta(usage, py_usage, previous_year)
    usage.drop('rank', inplace=True, axis=1)

    # remove nulls
    usage.dropna(subset=['name'], inplace=True)

    # sort
    usage.sort_values(['shaves', 'unique users'], ascending=False, inplace=True)

    # enforce max entities
    max_entities = entity['max_entities'] if 'max_entities' in entity else MAX_ENTITIES
    usage = usage.head(max_entities)

    print('##{0}\n'.format(inf_engine.plural(entity['name'])))

    print(usage.to_markdown(index=False))
    print('\n')


print('## Most Used Blades in Most Used Razors\n')

# do razor plus blade combo, filtered on most popular razors...
razor_usage = get_shave_data_for_year(stats_year, pl, RazorNameExtractor(), RazorAlternateNamer())
rpb_usage = get_shave_data_for_year(stats_year, pl, RazorPlusBladeNameExtractor(), RazorPlusBladeAlternateNamer())
razor_usage.sort_values(['shaves', 'unique users'], ascending=False, inplace=True)

# get most popular razors in use this year
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





