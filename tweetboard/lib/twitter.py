"""Twitter related functions
"""
import tweepy
import logging
#from totem.services import twitterpool
from random import Random
from core import image_extracter

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
TW_KEY = 'KS1C3RP9cBUvjxqjoW95ig'
TW_SECRET = 'CC6ugMv2JoYzzKyWyq2djWkghPnrK35jsHk8Cprlxcw'

#RESULTS_PER_PAGE = 100
RESULTS_PER_PAGE = 100
#RESULTS_PER_SEARCH = 1500
RESULTS_PER_SEARCH = 100 

PIPELINE_INPUT_SET_SIZE = 50

log = logging.getLogger(__name__)

def get_handle():
    #it should take input for a method-name as well
    #tw_users = twitterpool.get_all_pool_users()
    #pick One which has quota available for this method call.
    #tw_user = Random().choice(tw_users)
    
    #if tw_user is None:
	#log.error('No twitter user selected..')
	#return None

    access_token_key = '138827241-R6LAu4J7Cj7s8o1h9dQduzjoaphE4vaW3PQmUQuN'
    access_token_secret = 'bvQ7D4TyTPNN6Q5CnMWluv5X3ZNvKJExk6XF5iz0gE' 
    auth = tweepy.OAuthHandler(TW_KEY, TW_SECRET)
    auth.set_access_token(access_token_key, access_token_secret)
    api = tweepy.API(auth) 
    return api

def search_tweets(term, since_id = None, max_id = None):
    """Given input, get tweets"""
    handle = get_handle()

    if handle is None:
	log.error('Oops.. we have exhausted twitter pool... so lets wait for some more time')
	return (None, None, None)

    filter_tweets = []
    geo_code = None
    max_since_id = None
    min_since_id = None
    i = 0
    status = None
    images = {}
    q = '%s filter:links' % (term)
    for status in tweepy.Cursor(handle.search,
		    q = q, rpp = RESULTS_PER_PAGE,
		    since_id = since_id,
		    max_id = max_id,
		    include_entities = True
		    ).items(RESULTS_PER_SEARCH):
	try:
	    expanded_url = status.entities.get('urls')[0].get('expanded_url')
	except:
	    expanded_url = None
	    print 'status:%s: %s : %s : %s' % (i, status.text, status.id, status.entities)
	else:
	    if expanded_url:
		img = image_extracter(status.entities.get('urls')[0].get('expanded_url'))
		if img:
		    print "found image........"
		    if img not in images:
			c = CampaignTweet(query = term,
				    tw_id = str(status.id),
				    img_url = img,
				    comments = [status.text],
				    slug = status.__dict__)
			c.save()
			images[img] = c
		    else:
			#img already exist because retweeted
			c = images[img]
			CampaignTweet.objects(id = str(c.id)).update(push__comments = status.text)

	if max_since_id is None:
	    max_since_id = status.id
	i = i + 1
	#print 'status:%s: %s : %s : %s' % (i, status.text, status.id, status.entities)
    else:
	if status:
	    min_since_id = status.id 
	else:
	    log.debug('seems there are no further results ')
	log.debug('max-since-id: %s min-since-id: %s' % (max_since_id, min_since_id))
    return (filter_tweets, max_since_id, min_since_id)

def get_new_tweets(term, since_id):
    try:
	return search_tweets(term, since_id)
    except:
	log.exception('error in search tweet operation')
	return ([], None, None)

def get_past_tweets(term, max_id):
    try:
	return search_tweets(term, None, max_id, log = log)
    except:
	log.exception('error in search tweet operation')
	return ([], None, None)

def fetch_tweets_for_campaign(c):
    if c.past_tweets_exhausted:
	log.debug('campaign-s past tweets are exhausted. So lets fetch some new ones.')
	(tweets, max_since_id, max_id) = get_new_tweets(c.query, c.since_id, log)
	if tweets:
	    #some data received, lets move the pointers...
	    c.update(set__since_id = max_since_id)
	return tweets
    else:
	log.debug('lets fetch some past tweets for this campaign..')
	(tweets, max_since_id, max_id) = get_past_tweets(c.query, c.max_id, log)
	#update max_since_id and max_id 
	if tweets:
	    c.update(set__max_id = max_id - 1)
	    if c.since_id is None or c.since_id < max_since_id:
		c.update(set__since_id = max_since_id)
	else:
	    log.debug('marking campaign-s past tweets exhausted')
	    c.update(set__past_tweets_exhausted = True)
	return tweets

if __name__ == '__main__':
    import sys 
    connect('tweetboard_db')
    r = search_tweets(sys.argv[1]) 