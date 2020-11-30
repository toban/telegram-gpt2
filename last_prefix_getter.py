from prefix_getter import PrefixGetter
import feedparser
import random
import time
import logging
import sys
import requests
from io import BytesIO


class LastPrefixGetter(PrefixGetter):

	def getPrefix(self, bot, last_message) -> str:
		return self.last_message