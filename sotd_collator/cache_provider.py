import datetime
from enum import Enum


class ContentType(Enum):
    THREADS = "threads"
    COMMENTS = "comments"
    STAGED_COMMENTS = "staged_comments"


class CacheProvider(object):
    CACHE_DIR = "cache"

    def __init__(self, cache_dir: str = None):
        if cache_dir is not None:
            self.CACHE_DIR = cache_dir

    def get_comment_stage_file_path(self, given_month: datetime.date) -> str:
        return self.__get_cache_file_path(given_month, ContentType.STAGED_COMMENTS)

    def get_comment_cache_file_path(self, given_month: datetime.date) -> str:
        return self.__get_cache_file_path(given_month, ContentType.COMMENTS)

    def get_thread_cache_file_path(self, given_month: datetime.date) -> str:
        return self.__get_cache_file_path(given_month, ContentType.THREADS)

    def __get_cache_file_path(
        self, given_month: datetime.date, ct: ContentType
    ) -> str:
        filename = given_month.strftime("%Y%m.json")
        return f"{self.CACHE_DIR}/{ct.value}/{filename}"
