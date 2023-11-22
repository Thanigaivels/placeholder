from Scraper import Reddit
from Utils import configs


def startRedditScraper():
    obj = Reddit.RedditScraper(configs.get_reddit_auth())
    obj.start_scraping(configs.get_details_for_scraping())

def main():
    startRedditScraper()


if __name__ == '__main__':
    main()
