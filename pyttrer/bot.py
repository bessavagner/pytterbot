import tweepy
import os
import pyttrer.appaccess as access

class start:
    def __init__(self, filename):
        keys = access.keys(filename)
        self.auth = tweepy.OAuthHandler(
            keys.CONSUMER_KEY, keys.CONSUMER_SECRET)
        self.auth.set_access_token(keys.ACCESS_KEY, keys.ACCESS_SECRET)
        self.api = tweepy.API(self.auth, wait_on_rate_limit=True)

class mentions:
    def __init__(self, bot, last_id_file='last_id.txt'):
        self.api = bot.api
        self.last_id = self._read_id(last_id_file)

    def _read_id(self, filename):
        last_id = None
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                last_id = int(file.read())
                return last_id
        else:
            open(filename, 'a').close()
        return last_id

    def _write_id(self, last_id='0'):
        if os.path.exists(self.last_id_file):
            with open(self.last_id_file, 'w') as file:
                file.write(self.last_id)

    def _listtodict(self, data):
        return list(map(lambda x: x.__dict__, data))

    def _getlist(self, updated_id=False):
        if updated_id and self.last_id is not None:
                mentions_ = self.api.mentions_timeline(self.last_id)
        else:
            mentions_ = self.api.mentions_timeline()
        return mentions_

    def _getdict(self, updated_id=False):
        if updated_id and self.last_id is not None:

            mentions_ = self._listtodict((self.api.mentions_timeline(self.last_id)))
        else:
            mentions_ = self._listtodict((self.api.mentions_timeline()))
        return mentions_

    def _summarized_tweet(self, mentions_dict):
        infos_ = []
        for item in mentions_dict:
            infos_.append({
                'id': item['id'],
                'user': item['user'].screen_name,
                'tweet': item['text'],
                'date': item['created_at'],
            })
        return infos_
        
    def get(self, last=None, **kwargs):
        infos_ = self._summarized_tweet(self._getdict(**kwargs))
        if last is not None:
            if len(infos_) < last:
                return infos_
            else:
                return infos_[:last]
        return infos_
    
    def get_with_hastag(self, hashtag, **kwargs):
        mentions_ = self._getdict(**kwargs)
        tweets = []
        for item in mentions_:
            tags = item['_json']['entities']['hashtags']
            if len(tags) > 0:
                for tag in tags:
                    if hashtag == tag['text']:
                        tweets.append(item)
                        break
        return self._summarized_tweet(tweets)

class poster:
    def __init__(self, bot):
        self.api = bot.api
    
    def reply_mention(self, mention, text, in_reply=None, hashtag=None, last_tweet='last_tweet.txt'):
        to_user = ' tuitado em ' + str(mention['date']) + ' UTC'
        message = to_user + '\n' + text
        if isinstance(hashtag, str):
            message += hashtag
        if os.path.exists(last_tweet):
            with open('last_tweet.txt', 'r') as file:
                if message == file.read():
                    return
        else:
            open(last_tweet, 'a').close()
        if in_reply is not None:
            self.api.update_status(message, in_reply_to_status_id=in_reply,
                                    auto_populate_reply_metadata=True)
            with open('last_id.txt', 'w') as file:
                file.write(str(mention['id']))
        else:
            self.api.update_status(message)
        with open('last_tweet.txt', 'w') as file:
            file.write(message)



