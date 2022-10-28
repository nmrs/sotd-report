import pkg_resources
import json

INFILES = [
    pkg_resources.resource_filename('sotd_collator', '../misc/lg_corpuses/2020.json'),
    pkg_resources.resource_filename('sotd_collator', '../misc/lg_corpuses/2021.json'),
]

OUTFILE = pkg_resources.resource_filename('sotd_collator', '../misc/lg_corpuses/merged.json')


merged = []

for infile in INFILES:
    with open(infile, 'r') as inf:
        merged.extend(json.load(inf))

cleaned = [{'prompt': '', 'completion': x['completion']} for x in merged]

with open(OUTFILE, 'w', encoding='utf-8') as outf:
    json.dump(cleaned, outf, ensure_ascii=False)