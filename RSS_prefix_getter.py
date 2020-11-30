from prefix_getter import PrefixGetter
import feedparser
import random
import time
import logging
import sys
import requests
from io import BytesIO


class RSSPrefixGetter(PrefixGetter):
	def __init__(self, feeds):
		self.rss_feeds = feeds
		self.logger = logging.getLogger("PrefixGetter")

		self.feed_responses = {}
		self.index = 0
		self.posts = []
		self.num_entries = 0

	def getFeed(self, source):

		if source in self.feed_responses:
			self.logger.info("getFeed: " + source + " already exists")

			return self.feed_responses[source]

		# Do request using requests library and timeout
		resp = requests.get(source, timeout=20.0)
		content = BytesIO(resp.content)
		print(resp.content)
		self.logger.info("got response!")

		# Parse content
		feed =  feedparser.parse(content)
		feed_num_entries = len(feed.entries)
		self.num_entries += feed_num_entries
		self.feed_responses[source] = feed
		return self.feed_responses[source]

	def getPost(self):
		source = random.choice(self.rss_feeds)
		self.logger.info("getPost: " + source)
		try:
			NewsFeed = self.getFeed(source) 

			entry = random.choice(NewsFeed.entries)

			if self.num_entries != 0 and len(self.posts) >= self.num_entries:
				self.feed_responses = {}
				self.posts = []
				self.num_entries = 0

			if(entry['title'] in self.posts):
				return self.getPost()

			self.posts.append(entry['title'])
			return entry
		except KeyboardInterrupt:
			e = sys.exc_info()[0]
			raise e
		except: # catch all
			e = sys.exc_info()[0]
			self.logger.error(e)
			time.sleep(10)
			return self.getPost()

	def getPrefix(self, bot, last_message) -> str:
		
		entry = self.getPost()

		bot.talk(entry['link'])

		return entry['title']