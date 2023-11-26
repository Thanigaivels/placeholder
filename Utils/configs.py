def get_reddit_auth():
    auth_dict = {
        "client_id": 'RYo0LnHrepjPvwVyLy2Vlg',
        "client_secret": 'N8hX8aDIhozbCe5hqIDNiPqG3gn-gw',
        "user_agent": 'RedditBot-v1.0',
        "username": 'Which_Function_4202',
        "password": 'SaraNyAA@'
    }
    return auth_dict

def get_insta_profile(profile):
    all_profiles = {
    #profile data
    }
    if all_profiles[profile] != None:
        return all_profiles[profile]
    else:
        all_profiles['profile_1']

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