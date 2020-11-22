from prefix_getter import PrefixGetter
import feedparser
import random
import time
import logging


class DNPrefixGetter(PrefixGetter):
	def __init__(self):
		self.rss_feeds = [
			'http://expressen.se/rss/nyheter',
			'https://rss.aftonbladet.se/rss2/small/pages/sections/aftonbladet/',
			'http://api.sr.se/api/rss/program/83?format=145',
			'https://www.svt.se/nyheter/rss.xml',
			'https://www.reddit.com/r/svenskpolitik/.rss',
			'https://www.flashback.org/external.php?type=rss'
			'https://www.reddit.com/r/sweden/.rss'
		]
		self.logger = logging.getLogger("PrefixGetter")

		self.index = 0
		self.posts = []

	def getPost(self):
		source = random.choice(self.rss_feeds)
		try:

			NewsFeed = feedparser.parse(source)
			entry = random.choice(NewsFeed.entries)

			if len(self.posts) > 100:
				self.posts = []

			if(entry['title'] in self.posts):
				return self.getPost()

			self.posts.append(entry['title'])
			return entry

		except: # catch all
			e = sys.exc_info()[0]
			self.logger.error(e)
			time.sleep(10)
			return self.getPost()

	def getPrefix(self, bot) -> str:
		
		entry = self.getPost()

		bot.talk(entry['link'])

		return entry['title']