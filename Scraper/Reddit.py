import sys

import praw

from Utils import configs

class RedditScraper:
    def __init__(self, config):
        self.profile = config['profile']
        auth = configs.get_reddit_auth()
        try:
            self.client = praw.Reddit(
                client_id=auth["client_id"],
                client_secret=auth["client_secret"],
                user_agent=auth["user_agent"],
                username=auth["username"],
                passkey=auth["password"],
                check_for_async=False,
            )
        except Exception as e:
            print("Something went wrong when creating reddit client...\n", e)
            sys.exit(1)

    def start_scraping(self):
        profile_details = configs.get_profile_config(self.profile)
        subreddit_details = profile_details["no_of_post"]
        pass

    def test(self):
        print(self.client)