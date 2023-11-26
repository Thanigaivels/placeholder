import json
import sys
import time
import praw
from Utils import storage_handler


class RedditScraper:
    def __init__(self, auth):
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
        self.source = "reddit"

    def start_scraping(self, scrapping_info):
        for subreddit_name, info in scrapping_info.items():
            print(f"Scraping content from {subreddit_name}\n")
            subreddit = self.client.subreddit(subreddit_name)
            thread_list = subreddit.top(time_filter="day", limit=5)
            curr_reddit_posts = []
            for post_obj in thread_list:
                link_attr = {}
                upload_type = "image"
                if post_obj.is_self:  # text convert it into carousel
                    link_attr = {
                        "type": "text",
                        "content": ["blah"]
                    }
                    upload_type = "story"
                elif post_obj.domain == 'i.redd.it' and 'gif' not in post_obj.url:  # image
                    link_attr = {
                        "type": "image",
                        "content": [post_obj.url],
                        "width": 2316,
                        "height": 3088
                    }
                    upload_type = "image"
                elif post_obj.domain == 'v.redd.it':  # video
                    link_attr = {
                        "type": "reel",
                        "content": [post_obj.media["reddit_video"]["fallback_url"],
                                    post_obj.media["reddit_video"]["fallback_url"].split("DASH_")[0] +
                                    "DASH_AUDIO_128.mp4"],
                        "width": 720,
                        "height": 1280,
                        "duration": post_obj.media["reddit_video"]["duration"]
                    }
                    upload_type = "reel"
                elif post_obj.domain == 'reddit.com':  # carousel
                    link_attr = {  # work on this for multiple images
                        "type": "carousel",
                        "content": [post_obj.url]
                    }
                    upload_type = "carousel"
                caption = f"\n\n\nFollow Us for more exciting content @gommala\n\n" \
                          f"Credit: r/{subreddit_name}\n\nPING US FOR CREDIT OR REMOVAL\n\nHashtags below\n.\n.\n.\n"
                post_obj.comment_sort = 'top'
                post_obj.comment_limit = 5
                for top_level_comment in post_obj.comments:
                    if str(top_level_comment.__class__) == "<class 'praw.models.reddit.comment.Comment'>" and 200 > len(
                            top_level_comment.body) > 15 and 'http' not in top_level_comment.body:
                        caption = str(top_level_comment.body) + caption
                        break
                curr_post = (self.source, post_obj.id, post_obj.url, json.dumps(link_attr), caption,
                             post_obj.title, upload_type, int(time.time()), post_obj.created, subreddit_name, None)
                curr_reddit_posts.append(curr_post)
            # write_to_db
            storage_handler.insert_scraped_data(curr_reddit_posts)

    def test(self):
        print(self.client)
