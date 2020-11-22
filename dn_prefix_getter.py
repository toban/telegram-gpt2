from prefix_getter import PrefixGetter
import feedparser
import random

class DNPrefixGetter(PrefixGetter):
	def __init__(self):
		self.last_prefixes = []
		self.index = 0
	
	def getPrefix(self) -> str:
		NewsFeed = feedparser.parse("https://rss.aftonbladet.se/rss2/small/pages/sections/aftonbladet/")
		entry = random.choice(NewsFeed.entries)

		return entry['title']