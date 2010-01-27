# Tweepy
# Copyright 2009 Joshua Roesslein
# See LICENSE

from tweepy.error import TweepError

def pagination_proxy(name_or_func=None):
    def wrapper(f):
        class Wrapper(object):
            def __get__(self, inst, owner):
                setattr(owner, f.__name__, f)
                f.pagination_mode = getattr(inst._api,
                        (f.__name__ if name_or_func is None
                            else name_or_func)).pagination_mode
                return getattr(inst, f.__name__)
        return Wrapper()
    if not isinstance(name_or_func, str):
        f2 = name_or_func
        name_or_func = None
        return wrapper(f2)
    return wrapper

class Model(object):

    def __getstate__(self):
        # pickle
        pickle = {}
        for k, v in self.__dict__.items():
            if k == '_api':
                # do not pickle the api reference
                continue
            pickle[k] = v
        return pickle


class Status(Model):

    def destroy(self):
        return self._api.destroy_status(self.id)

    def retweet(self):
        return self._api.retweet(self.id)

    def retweets(self):
        return self._api.retweets(self.id)

    def favorite(self):
        return self._api.create_favorite(self.id)


class User(Model):

    @pagination_proxy('user_timeline')
    def timeline(self, **kargs):
        return self._api.user_timeline(user_id=self.id, **kargs)

    @pagination_proxy
    def friends(self, **kargs):
        return self._api.friends(user_id=self.id, **kargs)

    @pagination_proxy
    def followers(self, **kargs):
        return self._api.followers(user_id=self.id, **kargs)

    def follow(self):
        self._api.create_friendship(user_id=self.id)
        self.following = True

    def unfollow(self):
        self._api.destroy_friendship(user_id=self.id)
        self.following = False

    @pagination_proxy
    def lists_memberships(self, *args, **kargs):
        return self._api.lists_memberships(user=self.screen_name, *args, **kargs)

    @pagination_proxy
    def lists_subscriptions(self, *args, **kargs):
        return self._api.lists_subscriptions(user=self.screen_name, *args, **kargs)

    @pagination_proxy
    def lists(self, *args, **kargs):
        return self._api.lists(user=self.screen_name, *args, **kargs)

    @pagination_proxy
    def followers_ids(self, *args, **kargs):
        return self._api.followers_ids(user_id=self.id, *args, **kargs)


class DirectMessage(Model):

    def destroy(self):
        return self._api.destroy_direct_message(self.id)


class Friendship(Model):

    pass


class SavedSearch(Model):

    def destroy(self):
        return self._api.destroy_saved_search(self.id)


class SearchResult(Model):

    pass

class Retweet(Model):

    def destroy(self):
        return self._api.destroy_status(self.id)

class List(Model):

    def update(self, **kargs):
        return self._api.update_list(self.slug, **kargs)

    def destroy(self):
        return self._api.destroy_list(self.slug)

    @pagination_proxy('list_timeline')
    def timeline(self, **kargs):
        return self._api.list_timeline(self.user.screen_name, self.slug, **kargs)

    def add_member(self, id):
        return self._api.add_list_member(self.slug, id)

    def remove_member(self, id):
        return self._api.remove_list_member(self.slug, id)

    @pagination_proxy('list_members')
    def members(self, **kargs):
        return self._api.list_members(self.user.screen_name, self.slug, **kargs)

    @pagination_proxy('is_list_member')
    def is_member(self, id):
        return self._api.is_list_member(self.user.screen_name, self.slug, id)

    def subscribe(self):
        return self._api.subscribe_list(self.user.screen_name, self.slug)

    def unsubscribe(self):
        return self._api.unsubscribe_list(self.user.screen_name, self.slug)

    @pagination_proxy('list_subscribers')
    def subscribers(self, **kargs):
        return self._api.list_subscribers(self.user.screen_name, self.slug, **kargs)

    def is_subscribed(self, id):
        return self._api.is_subscribed_list(self.user.screen_name, self.slug, id)


class ModelFactory(object):
    """
    Used by parsers for creating instances
    of models. You may subclass this factory
    to add your own extended models.
    """

    status = Status
    user = User
    direct_message = DirectMessage
    friendship = Friendship
    saved_search = SavedSearch
    search_result = SearchResult
    retweet = Retweet
    list = List

