import json

import praw

from sotd_collator.lather_games_post_locator import LatherGamesPostLocator
import pkg_resources

lgpl = LatherGamesPostLocator(praw.Reddit("standard_creds", user_agent="arach"))

res = []
PROMPT = "Write a Lather Games SOTD post on the theme of Spring into the Games"

OUTPUT_FILE = pkg_resources.resource_filename(
    "sotd_collator", "../misc/lg_corpuses/2020.json"
)

for comment, author in lgpl.get_comments_for_theme("2020"):
    res.append({"prompt": " ", "completion": comment})

with open(OUTPUT_FILE, "w") as fout:
    json.dump(res, fout)
