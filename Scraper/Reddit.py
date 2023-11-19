class RedditScraper:
    def __init__(self, config):
        self.id = config['id']

    def test(self):
        print(self.id)