from prefix_getter import PrefixGetter
import feedparser
import random
import time
import logging
import sys
import requests
from io import BytesIO


class DNPrefixGetter(PrefixGetter):
	def __init__(self):
		self.rss_feeds = [
			'http://www.reddit.com/r/svenskpolitik/.rss',
			'http://www.flashback.org/external.php?type=rss'
			'http://www.reddit.com/r/sweden/.rss'
		]
		self.logger = logging.getLogger("PrefixGetter")

		self.index = 0
		self.posts = []

	def getPost(self):
		
		source = random.choice(self.rss_feeds)
		self.logger.info("getPost: " + source)
		try:

			# Do request using requests library and timeout
			resp = requests.get(source, timeout=20.0)
			content = BytesIO(resp.content)
			self.logger.info("got response!")

			# Parse content
			NewsFeed = feedparser.parse(content)

			entry = random.choice(NewsFeed.entries)

			if len(self.posts) > 200:
				self.posts = []

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
			#time.sleep(10)
			return self.getPost()

	def getPrefix(self, bot) -> str:
		
		entry = self.getPost()

		bot.talk(entry['link'])

		return entry['title']