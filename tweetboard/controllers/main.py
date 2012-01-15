import logging
from mongoengine import connect

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from tweetboard.lib.base import BaseController, render
import tweepy

from tweetboard.lib import user as user_service, helpers as h
from tweetboard.lib import twitter as tw_service

log = logging.getLogger(__name__)

TW_KEY = 'KS1C3RP9cBUvjxqjoW95ig'
TW_SECRET = 'CC6ugMv2JoYzzKyWyq2djWkghPnrK35jsHk8Cprlxcw'

USER_INFO_COOKIE='tw_sname'
PAGE_TYPE_HOME = 'home'
PAGE_TYPE_EXPLORE = 'explore'
PAGE_TYPE_GAME = 'game'

class MainController(BaseController):

    def __before__(self):
        """Stuff needed for every action"""
        mdb_host = 'localhost'
        mdb_port = 27017
        mdb_db = 'tweetboard_db'
        mdb_username = ''
        mdb_passwd = ''
	connect(mdb_db)
	self.tw_user = request.cookies[USER_INFO_COOKIE]

    def index(self):
        # Return a rendered template
        #return render('/main.mako')
        # or, return a response
	return render("board.html")

    @h.ourjsonify
    def search(self):

	q = request.params.get('q', 'srk')
	c = int(request.params.get('c', 10))
	start_idx = int(request.params.get('start_idx', 0))
	end_idx = start_idx + c
	resp = {}
	content = [x.to_json() for x in tw_service.CampaignTweet.objects(query = q)[start_idx:end_idx]]
	if content:
	    resp['data'] = content
	else:
	    resp['error'] = 'No data found'
	return resp

    def login(self):
        """lets try twitter implementation
        login action will only be called if user presses signin button
        """
        auth = tweepy.OAuthHandler(TW_KEY, TW_SECRET, 'http://localhost:5000/main/tw_callback')
        try:
            redirect_url = auth.get_authorization_url(signin_with_twitter=True)
            #redirect_url = auth.get_authorization_url()
        except tweepy.TweepError:
            log.exception('Tweepy error')
            raise
        session['request_token'] = (auth.request_token.key, auth.request_token.secret)
        session.save()
        redirect_to(redirect_url)
    
    def tw_callback(self):
        log.info('request %s' % request)
        verifier = request.GET.get('oauth_verifier')
        log.info('verifier [%s] session[%s]' % (verifier, session))
        auth = tweepy.OAuthHandler(TW_KEY, TW_SECRET)
        if 'request_token' in session:
            token = session['request_token']
            session['request_token'] = None
        else:
            log.error('oops request token not foudn in the session')
        #session.delete('request_token')
        auth.set_request_token(token[0], token[1])
        try:
            auth.get_access_token(verifier)
	except Exception: 
            log.exception('Veifier error')
            raise

        log.info('Ok. got the request token key[%s] and secret[%s]' % (auth.access_token.key, auth.access_token.secret))

        #check if user exists with given screen name

	#new_auth.set_access_token(auth.access_token.key, auth.access_token.secret)
	auth.set_access_token(auth.access_token.key, auth.access_token.secret)
        api = tweepy.API(auth)
        #api.update_status('testing' + 'tweepy' + 'oauth')
        tw_user = api.me()
        log.info('User info[%s] tw_id[%s]' % (tw_user.screen_name, tw_user.id))

        user = user_service.get_or_create_user(screen_name = tw_user.screen_name, \
						tw_id = str(tw_user.id), key = auth.access_token.key,\
						secret = auth.access_token.secret)
        #workflow to see if user exists or it is a first time user
        response.set_cookie(USER_INFO_COOKIE, tw_user.screen_name, max_age = 60*60*24)
	return 'Hi %s, your details token:[%s] and secret[%s]' % (tw_user.screen_name, auth.access_token.key, auth.access_token.secret)
