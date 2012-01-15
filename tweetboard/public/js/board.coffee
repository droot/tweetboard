
# Global Event Dispatcher
EventDispatcher =
		EVENT_CREATE_POLL: 'create_poll'
		EVENT_ADD_PRODUCT: 'add_product_to_shortlist'
		EVENT_REMOVE_PRODUCT: 'remove_product_from_shortlist'
		EVENT_SHORTLIST_COMPLETE: 'shortlist_complete'
		EVENT_SHORTLIST_COUNT_CHANGED: 'count_of_shortlist_changed'

_.extend(EventDispatcher, Backbone.Events)

# Basic model of a tweet
class TweetModel extends Backbone.Model

# Considered Products
# -------------------
class TweetListCollection extends Backbone.Collection
	model: TweetModel

class TweetListModel extends Backbone.Model
	initialize: =>
		@t_list = new TweetListCollection
		@col_to_add = 1
	
	load_list: =>
		ajax_params =
			url: '/main/search'
			data:
				q: 'srk'
				c: '30'
				start_idx: '0'
			success: (response) =>
				if response and response.data
					for content in response.data
						tweet_data =
							img_url: content.img
							main_text: content.slug.text
							num_retweets: content.comments.length
							comments: content.comments
						tweet = new TweetModel tweet_data
						@t_list.add tweet
				else
					alert "Error in getting considered products"
			error: (obj, txt) =>
				alert txt

		$.ajax ajax_params

class TweetsListView extends Backbone.View
	initialize: =>
		@model.t_list.bind('add', @add_tweet)
	
	add_tweet: (tweet) =>
		a_tweet = new TweetView model: tweet
		$("#col" + @model.col_to_add).append a_tweet.render().el
		@model.col_to_add++
		@model.col_to_add = 1 if @model.col_to_add > 4

class TweetView extends Backbone.View

	initialize: =>
		@template = $.template $("#tweet_template")

	events:
		"click .retweet": "retweet"

	render: =>
		$(@el).html($.tmpl(@template, @model.toJSON())).attr('id', "product_#{@model.cid}")
		@

	retweet: =>



# Base Controller
class AppController extends Backbone.Controller
	initialize: =>
		# render base page
		@tweet_list_model = new TweetListModel
		@tweet_list_view = new TweetsListView el: $("#rich_container"), model: @tweet_list_model
		@tweet_list_model.load_list()



window.paint = () =>
	a = new AppController
