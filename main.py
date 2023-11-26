import argparse

from Scraper import Reddit
from Utils import configs


def startRedditScraper():
    obj = Reddit.RedditScraper(configs.get_reddit_auth())
    obj.start_scraping(configs.get_details_for_scraping())


def get_input():
    description = '''
            Example script for parsing command line arguments. 
            python main.py -r subredditName -n 3
            (or)
            python main.py -y https://youtube_link.com/gtecop -s hh:mm:ss -e hh:mm:ss
            '''

    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('-p', '--profile', type=str,
                        default="profile_1",
                        help='Profile to be uploaded in')
    parser.add_argument('-scrape', '--scrape',
                        action='store_false')

    args = parser.parse_args()
    return args


def main():
    user_input = get_input()
    if user_input.scrape:
        startRedditScraper()
    else:
        pass


if __name__ == '__main__':
    main()
