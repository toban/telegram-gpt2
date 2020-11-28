from telegram import Update
import logging
from telegram.ext import CommandHandler, Updater, MessageHandler, Filters, CallbackContext
import time
import gpt_2_simple as gpt2
import sys
from config import Setup
import os

## todo telegram.vendor.ptb_urllib3.urllib3.exceptions.ReadTimeoutError:
## todo telegram.error.BadRequest: Message must be non-empty

class Bot:

	def __init__(self, token, name, voice_pitch):

		self.updater = Updater(token=token, use_context=True)
		self.dispatcher = self.updater.dispatcher
		self.name = name
		self.voice_pitch = voice_pitch
		self.logger = logging.getLogger('Bot: ' + name)
		self.logger.info("starting bot!")

	def send_voice(self, message):
		self.logger.info("send voice: " + message)
		try:
			# vorbis-tools
			os.system('espeak "' + message + '" -v sv -p '+ str(self.voice_pitch) +' -s 100 --stdout | oggenc -b 50 -o out.ogg -')
			voice = open('out.ogg', 'rb')
			self.dispatcher.bot.send_voice(Setup.config['chat_id'], voice, None, message)
			os.system('rm -f out.ogg')
		except: # catch all
			e = sys.exc_info()[0]
			self.logger.error(e)
			raise e

	def talk(self, message, reply_message=None):
		self.logger.info(message)
		try:
			if reply_message is not None:
				self.dispatcher.bot.send_message(chat_id=Setup.config['chat_id'], text=message)#, reply_to_message_id=reply_message.message_id)
			else:
				self.dispatcher.bot.send_message(chat_id=Setup.config['chat_id'], text=message, disable_notification=true)
		except: # catch all
			e = sys.exc_info()[0]
			self.logger.error(e)
			raise e
