from Scraper import Reddit


def main():
    config = {
        'profile': 'viral_videos'
    }
    obj = Reddit.RedditScraper(config)
    obj.test()


if __name__ == '__main__':
    main()
