(function() {
  var AppController, EventDispatcher, TweetListCollection, TweetListModel, TweetModel, TweetView, TweetsListView;
  var __hasProp = Object.prototype.hasOwnProperty, __extends = function(child, parent) {
    for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; }
    function ctor() { this.constructor = child; }
    ctor.prototype = parent.prototype;
    child.prototype = new ctor;
    child.__super__ = parent.prototype;
    return child;
  }, __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; };
  EventDispatcher = {
    EVENT_CREATE_POLL: 'create_poll',
    EVENT_ADD_PRODUCT: 'add_product_to_shortlist',
    EVENT_REMOVE_PRODUCT: 'remove_product_from_shortlist',
    EVENT_SHORTLIST_COMPLETE: 'shortlist_complete',
    EVENT_SHORTLIST_COUNT_CHANGED: 'count_of_shortlist_changed'
  };
  _.extend(EventDispatcher, Backbone.Events);
  TweetModel = (function() {
    __extends(TweetModel, Backbone.Model);
    function TweetModel() {
      TweetModel.__super__.constructor.apply(this, arguments);
    }
    return TweetModel;
  })();
  TweetListCollection = (function() {
    __extends(TweetListCollection, Backbone.Collection);
    function TweetListCollection() {
      TweetListCollection.__super__.constructor.apply(this, arguments);
    }
    TweetListCollection.prototype.model = TweetModel;
    return TweetListCollection;
  })();
  TweetListModel = (function() {
    __extends(TweetListModel, Backbone.Model);
    function TweetListModel() {
      this.load_list = __bind(this.load_list, this);
      this.initialize = __bind(this.initialize, this);
      TweetListModel.__super__.constructor.apply(this, arguments);
    }
    TweetListModel.prototype.initialize = function() {
      this.t_list = new TweetListCollection;
      return this.col_to_add = 1;
    };
    TweetListModel.prototype.load_list = function() {
      var ajax_params;
      ajax_params = {
        url: '/main/search',
        data: {
          q: 'srk',
          c: '30',
          start_idx: '0'
        },
        success: __bind(function(response) {
          var content, tweet, tweet_data, _i, _len, _ref, _results;
          if (response && response.data) {
            _ref = response.data;
            _results = [];
            for (_i = 0, _len = _ref.length; _i < _len; _i++) {
              content = _ref[_i];
              tweet_data = {
                img_url: content.img,
                main_text: content.slug.text,
                num_retweets: content.comments.length,
                comments: content.comments
              };
              tweet = new TweetModel(tweet_data);
              _results.push(this.t_list.add(tweet));
            }
            return _results;
          } else {
            return alert("Error in getting considered products");
          }
        }, this),
        error: __bind(function(obj, txt) {
          return alert(txt);
        }, this)
      };
      return $.ajax(ajax_params);
    };
    return TweetListModel;
  })();
  TweetsListView = (function() {
    __extends(TweetsListView, Backbone.View);
    function TweetsListView() {
      this.add_tweet = __bind(this.add_tweet, this);
      this.initialize = __bind(this.initialize, this);
      TweetsListView.__super__.constructor.apply(this, arguments);
    }
    TweetsListView.prototype.initialize = function() {
      return this.model.t_list.bind('add', this.add_tweet);
    };
    TweetsListView.prototype.add_tweet = function(tweet) {
      var a_tweet;
      a_tweet = new TweetView({
        model: tweet
      });
      $("#col" + this.model.col_to_add).append(a_tweet.render().el);
      this.model.col_to_add++;
      if (this.model.col_to_add > 4) {
        return this.model.col_to_add = 1;
      }
    };
    return TweetsListView;
  })();
  TweetView = (function() {
    __extends(TweetView, Backbone.View);
    function TweetView() {
      this.retweet = __bind(this.retweet, this);
      this.render = __bind(this.render, this);
      this.initialize = __bind(this.initialize, this);
      TweetView.__super__.constructor.apply(this, arguments);
    }
    TweetView.prototype.initialize = function() {
      return this.template = $.template($("#tweet_template"));
    };
    TweetView.prototype.events = {
      "click .retweet": "retweet"
    };
    TweetView.prototype.render = function() {
      $(this.el).html($.tmpl(this.template, this.model.toJSON())).attr('id', "product_" + this.model.cid);
      return this;
    };
    TweetView.prototype.retweet = function() {};
    return TweetView;
  })();
  AppController = (function() {
    __extends(AppController, Backbone.Controller);
    function AppController() {
      this.initialize = __bind(this.initialize, this);
      AppController.__super__.constructor.apply(this, arguments);
    }
    AppController.prototype.initialize = function() {
      this.tweet_list_model = new TweetListModel;
      this.tweet_list_view = new TweetsListView({
        el: $("#rich_container"),
        model: this.tweet_list_model
      });
      return this.tweet_list_model.load_list();
    };
    return AppController;
  })();
  window.paint = __bind(function() {
    var a;
    return a = new AppController;
  }, this);
}).call(this);
