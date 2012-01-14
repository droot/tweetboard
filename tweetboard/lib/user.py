from tweetboard.model import *
import logging
from random import Random

log = logging.getLogger(__name__)

def get_user(screen_name):
    return User.get_user(screen_name = screen_name)

def get_author(screen_name):
    return Author.get_author(screen_name)

def get_or_create_user(screen_name, tw_id, key, secret):
    """Save most important stuff for now"""
    assert screen_name and tw_id and key and secret, "Missing Arguments"
    try:
	(user, created) = User.get_or_create(screen_name = screen_name,\
						    defaults = dict(
								tw_id = tw_id,
								access_token_key = key,
								access_token_secret = secret)
						    )
	if created:
	    log.info("New user created")
	else:
	    log.info('User already exist')

	return user
    except:
	log.exception("Error while saving User Info")
	return None
