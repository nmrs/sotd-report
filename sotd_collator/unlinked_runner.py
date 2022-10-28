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
from sotd_collator.utils import add_ranking_delta, get_shave_data_for_month, get_shaving_histogram, get_unlinked_entity_data_for_month

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

stats_month = datetime.date(2022,7,1)
previous_month = stats_month - relativedelta(months=1)
previous_year = stats_month - relativedelta(months=12)

print("""
Unlinked entity detection 
""".format(stats_month.strftime('%b %Y')))

for entity in process_entities:
    usage = get_unlinked_entity_data_for_month(stats_month, pl, entity['extractor'], entity['renamer'])





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





