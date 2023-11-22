def get_reddit_auth():
    auth_dict = {
    # auth goes here
    }
    return auth_dict


def get_profile_config(profile):
    profile_config = {
        "default_captions": "bruh stfu",
        "no_of_post": {
            "aww": 2,
            "memes": 2},
        "niche": "cute"
    }
    return profile_config


def get_details_for_scraping():
    scraping_info = {
        "aww": {
            "no_of_posts": 2,
            "niche": "cute"
        },
        "memes": {
            "no_of_posts": 2,
            "niche": "funny"
        }
    }
    return scraping_info