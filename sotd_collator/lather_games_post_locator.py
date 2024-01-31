import praw
import prawcore
from praw.models import MoreComments

from sotd_collator.sotd_post_locator import SotdPostLocator


"""
Specifically for finding LG past threads etc
"""


class LatherGamesPostLocator(SotdPostLocator):
    SOTD_THREAD_PATTERNS = ["lather games"]
    SOTD_COMMENT_PATTERN = "**Razor:**"
    MIN_COMMENT_CHARS = 900

    def _get_sotd_query_str(self, theme_name):
        return "flair_name:SOTD games {0}".format(theme_name)

    def get_threads_for_given_theme(self, theme_name):
        """
        Return list of threads with given theme
        :return:
        """

        rec = self.praw.subreddit("wetshaving").search(
            query=self._get_sotd_query_str(theme_name),
            sort="hot",
            limit=100,
        )

        return [
            x
            for x in rec
            if "podcast" not in x.title.lower()
            and [
                # filter out threads with SOTD flair that arent true SOTD threads
                y
                for y in self.SOTD_THREAD_PATTERNS
                if y in x.title.lower()
            ]
        ]

    def get_comments_for_theme(self, theme_name):
        def _get_comments(comment_list):
            # compatible with recursion / more comments objects
            collected_comments = []
            for x in comment_list:
                if isinstance(x, MoreComments):
                    collected_comments.extend(_get_comments(x.comments()))
                else:
                    try:
                        author = x.author.id if x.author else ""
                        if (
                            self.SOTD_COMMENT_PATTERN in x.body
                            and len(x.body) >= self.MIN_COMMENT_CHARS
                        ):
                            collected_comments.append((x.body, author))
                    except prawcore.exceptions.NotFound:
                        print("Missing comment")
                        pass

            return collected_comments

        comments = []
        for thread in self.get_threads_for_given_theme(theme_name):
            print("Reading from thread: {0}".format(thread.title))
            try:
                comments.extend(_get_comments(thread.comments))
            except AttributeError:
                pass

        return comments


if __name__ == "__main__":
    lgpl = LatherGamesPostLocator(praw.Reddit("standard_creds", user_agent="arach"))
    res = lgpl.get_threads_for_given_theme("2020")
    orderable = {x.created_utc: x.title for x in res}

    for sotd_date in sorted(orderable.keys()):
        print(sotd_date, orderable[sotd_date])

    for comment in lgpl.get_comments_for_theme("spring"):
        print(comment)
