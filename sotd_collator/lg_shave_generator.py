import re

import openai
KEY_FILE = '/Users/warnerj1/.openai_key'
FT_MODEL = 'curie:ft-personal-2022-05-15-13-01-15'
PROMPT = " "
NUM_TO_GEN = 10

with open(KEY_FILE, 'r') as fin:
    key = fin.read()
    openai.api_key = key.strip()

res = openai.Completion.create(
    model=FT_MODEL,
    prompt=PROMPT,
    temperature=0.9,
    max_tokens=1024,
    n=NUM_TO_GEN,
    # logit_bias={16469: 1},
)

for x in res['choices']:



    out = re.sub(
        r'202[0-1]',
        '2022',
        x['text'].replace('&#39;', "'"),
        re.MULTILINE,
    )

    print(out)
    print("\n\n\n^_^_^_^_^_^_^_^_^_^_^_^_^_^_^__^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^__^_^\n\n\n")