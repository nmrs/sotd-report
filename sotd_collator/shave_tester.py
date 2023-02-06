# test what our extractors pull from a sample SOTD
from sotd_collator.blade_alternate_namer import BladeAlternateNamer
from sotd_collator.blade_format_extractor import BladeFormatExtractor
from sotd_collator.blade_name_extractor import BladeNameExtractor
from sotd_collator.brush_alternate_namer import BrushAlternateNamer
from sotd_collator.brush_name_extractor import BrushNameExtractor
from sotd_collator.knot_size_extractor import KnotSizeExtractor
from sotd_collator.razor_alternate_namer import RazorAlternateNamer
from sotd_collator.razor_name_extractor import RazorNameExtractor

t = """
* **Brush:** Razor Emporium best badger, orange acrylic, 26mm x 55mm

* **Face Razor:** Calypso M2

* **Head/Body Razor:** Gillette Flare Tip Super Speed

* **Blade:** Trig (8)

* **Lather:** Barrister & Mann - Cologne Russe

Post Shave: Antiga Barbearia de Bairro - Principe Real (Green) - Balm

Post Shave: Razor Emporium - Sandalwood - Beard Oil
"""

extractors = [
    {
        'name': 'Blade Format',
        'extractor': BladeFormatExtractor(),
        'renamer': None,
    },
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
]


for e in extractors:
    print('****')
    print(e['name'])
    entity_name = e['extractor'].get_name(t)
    if entity_name is not None:
        principal_name = None
        if e['renamer']:
            principal_name = e['renamer'].get_principal_name(entity_name)
            print(principal_name) if principal_name else print(entity_name)
        else:
            print(entity_name)
    else:
        print('No result')
    print('***')
