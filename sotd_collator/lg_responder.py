import re

import openai
KEY_FILE = '/Users/warnerj1/.openai_key'
FT_MODEL = 'text-davinci-002'
# FT_MODEL = 'curie:ft-personal-2022-05-15-13-01-15'


OTHER_PARTICIPANT = 'hairykopite'

TEXT_CHAIN = [
    "How's it going",
    """I think they should bring u / The_Real_Shaver in for the Podcast and give them their own Segment "Real Talk with The Real Shaver".""",
    # "Happy Birthday for next week",
]

prompt = ''
for x in range(0, len(TEXT_CHAIN) + 1):
    prompt += OTHER_PARTICIPANT + ': ' if x % 2 else 'The_Real_Shaver: '
    try:
        prompt += TEXT_CHAIN[x] + '\n'
    except IndexError:
        pass

print(prompt.strip())

NUM_TO_GEN = 5

with open(KEY_FILE, 'r') as fin:
    key = fin.read()
    openai.api_key = key.strip()

res = openai.Completion.create(
    model=FT_MODEL,
    prompt=prompt.strip(),
    temperature=0.9,
    max_tokens=128,
    n=NUM_TO_GEN,
    # logit_bias={16469: 1},
)

for x in res['choices']:

    print(x)
    print('\n\n')
    print(x['text'].strip())
    print("\n\n\n^_^_^_^_^_^_^_^_^_^_^_^_^_^_^__^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^__^_^\n\n\n")