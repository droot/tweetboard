from tweetboard.models import *
import logging
from random import Random

log = logging.getLogger(__name__)

def get_user(screen_name):
    return User.get_user(screen_name = screen_name)

def get_author(screen_name):
    return Author.get_author(screen_name)

def create_user(screen_name, tw_id, key, secret):
    """Save most important stuff for now"""

    user = User(screen_name = screen_name,
                tw_id = str(tw_id),
                access_token_key = key,
                access_token_secret = secret)
    user.save()
    user.reload()
    return user
