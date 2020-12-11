from prefix_getter import PrefixGetter
import feedparser
import random
import time
import logging
import sys
import requests
from io import BytesIO


class LastPrefixGetter(PrefixGetter):

	def __init__(self):
		self.last_message = None

	def getPrefix(self, bot, last_message) -> str:
		if last_message is None or last_message == self.last_message:
			return "hello"
		else: 
			self.last_message = last_message
			return last_message