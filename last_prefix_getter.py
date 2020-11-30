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
		if last_message is None:
			return "hello"
		else:
			return last_message