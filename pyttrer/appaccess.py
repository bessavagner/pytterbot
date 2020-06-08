from configparser import ConfigParser
class keys:
    """Get key token and secrets of your twiter app
    Got to https://developer.twitter.com/ for more info
    """
    def __init__(self, filename):
        config = ConfigParser()
        config.read(filename)

        self.CONSUMER_KEY = config['PYTTERBOT']['CONSUMER_KEY']
        self.CONSUMER_SECRET = config['PYTTERBOT']['CONSUMER_SECRET']
        self.ACCESS_KEY = config['PYTTERBOT']['ACCESS_KEY']
        self.ACCESS_SECRET = config['PYTTERBOT']['ACCESS_SECRET']
