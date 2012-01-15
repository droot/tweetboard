from mongoengine import *
from datetime import datetime

class User(Document):
    """Collection to represent the users of the game
    """
    screen_name = StringField(max_length = 100)
    tw_id = StringField()
    name = StringField()
    description = StringField()
    location = StringField()
    next_twc = IntField(default = 0)
    followers_count = IntField(default = 0)
    tweet_count = IntField(default = 0)
    created_at = DateTimeField(default = datetime.utcnow)
    last_login_time = DateTimeField()
    access_token_key = StringField()
    access_token_secret = StringField()
    nr_right = IntField(default = 0)
    nr_wrong = IntField(default = 0)
    nr_attempts = IntField(default = 0)

    @staticmethod
    def get_user(screen_name):
        try:
            return User.objects(screen_name = screen_name).get()
        except DoesNotExist:
            return None
        except:
            raise

class CampaignTweet(Document):
    """Defines an individual tweet collection.
    It will be used to store incoming 4square tweets
    """
    query = StringField(required = True)
    tw_id = StringField(unique = True)
    img_url = StringField(default = None)
    processed = BooleanField(default = False)
    slug = DictField(default = None)

    comments = ListField(StringField(), default = [])
