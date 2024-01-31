import datetime


class CacheProvider(object):
    CACHE_DIR = "misc"

    def __init__(self, cache_dir: str = None):
        if cache_dir is not None:
            self.CACHE_DIR = cache_dir

    def get_comment_stage_file_path(self, given_month: datetime.date) -> str:
        return self.__get_cache_file_path(given_month, "staged_comments")

    def get_comment_cache_file_path(self, given_month: datetime.date) -> str:
        return self.__get_cache_file_path(given_month, "comments")

    def get_thread_cache_file_path(self, given_month: datetime.date) -> str:
        return self.__get_cache_file_path(given_month, "threads")

    def __get_cache_file_path(self, given_month: datetime.date, type: str) -> str:
        return "{0}/{1}/{2}{3}.json".format(
            self.CACHE_DIR,
            type,
            given_month.year,
            given_month.month if given_month.month >= 10 else f"0{given_month.month}",
        )

    def __get_cache_file_path(self, given_month: datetime.date, type: str) -> str:
        return "{0}/{1}/{2}{3}.json".format(
            self.CACHE_DIR,
            type,
            given_month.year,
            given_month.month if given_month.month >= 10 else f"0{given_month.month}",
        )
