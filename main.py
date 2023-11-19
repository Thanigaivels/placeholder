from Scraper import Reddit


def main():
    config = {
        'id': '32isim'
    }
    obj = Reddit.RedditScraper(config)
    obj.test()


if __name__ == '__main__':
    main()
