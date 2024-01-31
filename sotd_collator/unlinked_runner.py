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
from sotd_collator.game_changer_plate_extractor import GameChangerPlateExtractor
from sotd_collator.karve_plate_extractor import KarvePlateExtractor
from sotd_collator.knot_size_extractor import KnotSizeExtractor
from sotd_collator.knot_type_extractor import KnotTypeExtractor
from sotd_collator.razor_name_extractor import RazorNameExtractor
from sotd_collator.razor_alternate_namer import RazorAlternateNamer
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
        "renamer": RazorAlternateNamer(),
        "max_entities": 50,
    },
    {
        "name": "Blade",
        "extractor": StagedBladeNameExtractor(),
        "renamer": BladeAlternateNamer(),
        "max_entities": 50,
    },
    {
        "name": "Brush",
        "extractor": BrushNameExtractor(),
        "renamer": BrushAlternateNamer(link_other=False),
        "max_entites": 50,
    },
]

comments = None
mode = "annual"

if mode == "annual":
    target = 2023
    comments = pl.get_comments_for_given_year_staged(2023)
    print(
        """
    Unlinked entity detection for {0}
    """.format(
            target
        )
    )
else:
    target = datetime.date(2023, 12, 1)
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

    usage = get_unlinked_entity_data(comments, entity["extractor"], entity["renamer"])

    # remove nulls
    usage.dropna(subset=["name"], inplace=True)

    # sort
    usage.sort_values(["shaves", "unique users"], ascending=False, inplace=True)

    # enforce max entities
    max_entities = entity["max_entities"] if "max_entities" in entity else MAX_ENTITIES
    usage = usage.head(max_entities)

    print(usage.to_markdown(index=False))
    print("\n")
