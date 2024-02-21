import datetime
import inflect

import praw
from dateutil.relativedelta import relativedelta
from blade_parser import BladeParser
from brush_parser import BrushParser
from razor_parser import RazorParser

from sotd_collator.blade_name_extractor import BladeNameExtractor
from sotd_collator.brush_name_extractor import BrushNameExtractor
from sotd_collator.knot_type_extractor import KnotTypeExtractor
from sotd_collator.razor_name_extractor import RazorNameExtractor
from sotd_collator.sotd_post_locator import SotdPostLocator
from sotd_collator.staged_name_extractors import (
    StagedRazorNameExtractor,
    StagedBladeNameExtractor,
    StagedBrushNameExtractor,
)
from sotd_collator.utils import get_unlinked_entity_data

pr = praw.Reddit("reddit")
pl = SotdPostLocator(pr)
inf_engine = inflect.engine()

MAX_ENTITIES = 150
MIN_SHAVES = 5


process_entities = [
    # {
    #     'name': 'Knot Type',
    #     'extractor': KnotTypeExtractor(),
    #     'renamer': None,
    # },
    {
        "name": "Razor",
        "extractor": StagedRazorNameExtractor(),
        "parser": RazorParser(),
        "parser field": "name",
        "max_entities": 50,
    },
    {
        "name": "Blade",
        "extractor": StagedBladeNameExtractor(),
        "parser": BladeParser(),
        "parser field": "name",
        "max_entities": 50,
    },
    {
        "name": "Brush",
        "extractor": BrushNameExtractor(),
        "parser": BrushParser(),
        "parser field": "name",
        "max_entites": 50,
    },
]

target = datetime.date(2024, 2, 1)
comments = pl.get_comments_for_given_month_staged(target)
print(
    """
Unlinked entity detection for {0}
""".format(
        target.strftime("%b %Y")
    )
)

for entity in process_entities:
    print("##{0}\n".format(inf_engine.plural(entity["name"])))

    usage = get_unlinked_entity_data(
        comments, entity["extractor"], entity["parser"], entity["parser field"]
    )

    # remove nulls
    usage.dropna(subset=["name"], inplace=True)

    # sort
    usage.sort_values(["shaves", "unique users"], ascending=False, inplace=True)

    # enforce max entities
    max_entities = entity["max_entities"] if "max_entities" in entity else MAX_ENTITIES
    usage = usage.head(max_entities)

    print(usage.to_markdown(index=False))
    print("\n")
