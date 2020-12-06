from telegram import Update
import logging
from telegram.ext import CommandHandler, Updater
import time
import gpt_2_simple as gpt2
import sys
from config import Setup
import os

from bot import Bot
from chat_manager import ChatManager
from text_generator import TextGenerator
from RSS_prefix_getter import RSSPrefixGetter
from last_prefix_getter import LastPrefixGetter

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

bots = []

for bot in Setup.config['tokens']:
	bots.append(Bot(Setup.config['tokens'][bot], Setup.config['names'][bot], Setup.config['voice_pitch'][bot]))

text_generator = TextGenerator()
prefix_getter = LastPrefixGetter() #RSSPrefixGetter(Setup.config['rss_feeds'])
logger = logging.getLogger('Main')

manager = ChatManager(Setup.config['chat_id'], bots, Setup.config, text_generator, prefix_getter)
while True:
	#if manager.prefix_message:
	#	manager.getPrefixMessages()
	#else:
	try:
		manager.update()
	except:
		e = sys.exc_info()[0]
		self.logger.error(e)
		logger.error(e)


print('hello')