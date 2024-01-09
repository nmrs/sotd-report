from ast import Dict
from ctypes import Array
import datetime
import json
from praw.reddit import Submission

class ThreadCacheBuilder(object):
    
    def load(self, cache_file: str):
        try:
            with open(cache_file, 'r') as f_cache:
                contents = json.load(f_cache)
                if isinstance(contents, dict):
                    for item in contents["manual"] + contents["added"]:
                        if item["id"] not in [t["id"] for t in contents["data"] if t["id"] == item["id"]]:
                            contents["data"].append(item)
                    return contents["data"]

                elif isinstance(contents, list):
                    return contents

        except (FileNotFoundError):
            return []

    def dump(self, cache_file: str, submissions: [Submission]) -> [Submission]:
        """
        Takes a list of Submission object to cache and returns the subset that
        that were not already present in the file.
        """
        def tojson(thread):
            return {
                "author": thread.author.name if thread.author is not None else None,
                "body": thread.selftext,
                "created_utc": datetime.datetime.fromtimestamp(thread.created_utc).strftime("%Y-%m-%d %H:%M:%S"),
                "id": thread.id,
                "title": thread.title,
                "url": thread.url,
            }
        
        cache_data = self.load(cache_file)
        found_existing_cache = len(cache_data) > 0
        added = []
        for thread in submissions:
            if thread.id not in [t["id"] for t in cache_data if t["id"] == thread.id]:
                added.append(thread)

        contents = {
            "added": [],
            "data": [],
            "manual": []
        }

        try:
            with open(cache_file, 'r') as f_cache:
                contents = json.load(f_cache)
        except (FileNotFoundError):
            pass

        result = []
        for submission in added:
            thread = tojson(submission)
            if found_existing_cache and submission.id not in [t["id"] for t in contents["added"] if t["id"] == submission.id]:
                contents["added"].append(thread)
            if submission.id not in [t["id"] for t in contents["data"] if t["id"] == submission.id]:
                contents["data"].append(thread)
                result.append(submission)
                print(f'added {thread["created_utc"]} - {thread["title"]}')
        
        for thread in contents["manual"]:
            if thread["id"] not in [t["id"] for t in contents["data"] if t["id"] == thread["id"]]:
                contents["data"].append(thread)

        for section in ["added", "data", "manual"]:
            contents[section] = sorted(contents[section], key=lambda item: item["created_utc"], reverse=True)

        with open(cache_file, 'w') as f_cache:
            json.dump(contents, f_cache, indent=4, sort_keys=True)

        return result
