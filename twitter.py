import tweepy
import constant
import time
import _json
from requests_oauthlib import OAuth1
import requests
import os

class Twitter :
    def __init__(self):
        print("Init twitter api")

    @staticmethod
    def init_tweepy():
        api = tweepy.OAuthHandler(constant.CONSUMER_KEY, constant.CONSUMER_SECRET)
        api.set_access_token(constant.ACCESS_KEY, constant.ACCESS_SECRET)
        return tweepy.API(api)

    def delete_dm(self, id):
        print("Delete dm with id "+ str(id))
        try:
            api = self.init_tweepy()
            api.destroy_direct_message(id)
            time.sleep(30)
        except Exception as ex:
            print(ex)
            time.sleep(30)
            pass


    def read_dm(self):
        print("Get Direct Message..")
        dms = list()
        try:
            api = self.init_tweepy()
            dm = api.list_direct_messages()
            for x in range(len(dm)):
                sender_id = dm[x].message_create['sender_id']
                message = dm[x].message_create['message_data']['text']
                message_data = str(dm[x].message_create['message_data'])
                json_data = _json.encode_basestring(message_data)
                print("Getting message -> "+str(message)+" by sender id "+str(sender_id))

            if "attachment" not in json_data:
                print("Dm does not have any media...")
                d = dict(message=message, sender_id=sender_id, id=dm[x].id, media=None)
                dms.append(d)
                dms.reverse()
            else:
                print("Dm have an attachment..")
                attachment = dm[x].message_create['message_data']['attachment']
                d = dict(message=message, sender_id=sender_id, id=dm[x].id, media=attachment['media']['media_url'])
                dms.append(d)
                dms.reverse()

            print(str(len(dms)) + " collected")
            time.sleep(60)
            return dms

        except Exception as ex:
            print(ex)
            time.sleep(60)
            pass

    def post_tweet(self):
        print("Uploading..")
        api = self.init_tweepy()
        api.update_with_media(filename="ready.png")

    def post_tweet_text(self, tweet):
        print("Uploading without image..")
        api = self.init_tweepy()
        api.update_status(tweet)

    def get_user_screen_name(self, id):
        print("Getting username")
        api = self.init_tweepy()
        user = api.get_user(id)
        return user.screen_name

    def post_tweet_with_media(self, tweet, media_url):
        print("Downloading media...")
        arr = str(media_url).split('/')
        auth = OAuth1(client_key=constants.CONSUMER_KEY,
                      client_secret=constants.CONSUMER_SCRET,
                      resource_owner_secret=constants.ACCESS_SECRET,
                      resource_owner_key=constants.ACCESS_KEY)
        r = requests.get(media_url, auth=auth)
        with open(arr[9], 'wb') as f:
            f.write(r.content)
        print("Media downloaded successfully!")
        api = self.init_tweepy()
        api.update_with_media(filename=arr[9], status=tweet)
        os.remove(arr[9])
        print("Upload with media success!")