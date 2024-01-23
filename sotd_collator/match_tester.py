import datetime
from pprint import pprint
from dateutil.relativedelta import relativedelta
import praw
from sotd_collator.blade_alternate_namer import BladeAlternateNamer
from sotd_collator.blade_name_extractor import BladeNameExtractor, BladeNameExtractorB
import sotd_post_locator


pr = praw.Reddit('reddit')
pl = sotd_post_locator.SotdPostLocator(pr)

start = datetime.date(2023, 12, 1)
end = datetime.date(2023, 12, 1)
curr_month = start

ban = BladeAlternateNamer()
bne_a = BladeNameExtractor()
bne_b = BladeNameExtractorB()

while (curr_month <= end):
    print(curr_month)

    comments = pl.get_comments_for_given_month_cached(curr_month)
    print(len(comments))

    for comment in comments:
        name_a = bne_a.get_name(comment)
        name_b = bne_b.get_name(comment)
        
        principal_name_a = None
        principal_name_b = None
        if name_a != None:
            principal_name_a = ban.get_principal_name(name_a)
        if name_b != None:
            principal_name_b = ban.get_principal_name(name_b)

        if (principal_name_a != principal_name_b):
            pprint({
                "a": principal_name_a,
                "b": principal_name_b
            })
            if name_a != None:
                principal_name_a = ban.get_principal_name(name_a)
            if name_b != None:
                principal_name_b = ban.get_principal_name(name_b)


    curr_month = curr_month + relativedelta(months=1)
