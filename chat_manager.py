from telegram import Update
import logging
from telegram.ext import CommandHandler, Updater, MessageHandler, Filters, CallbackContext
import time
import gpt_2_simple as gpt2
import sys
from config import Setup
import os

class ChatManager:
 
	def __init__(self, chat_id, bots, setup, text_generator):

		self.updater = Updater(token=setup['manager_bot'], use_context=True)
		self.dispatcher = self.updater.dispatcher
		self.dispatcher.add_handler(MessageHandler(Filters.chat(chat_id) & Filters.text & ~Filters.command, self.messageHandler))
		self.updater.start_polling()

		self.prefix_message = None
		self.text_generator = text_generator
		self.last_message = None
		self.last_raw_message = None
		self.chat_id = chat_id
		self.bots = bots
		self.messages = []
		self.messagesSwap = []
		self.setup = setup
		self.logger = logging.getLogger('ChatManager')
		self.training = False

	def messageHandler(self, update: Update, context: CallbackContext) -> None:
		"""Echo the user message."""
		#prefix =" print()
		print(dir(update.message))
		if self.training:
			self.logger.info("getting messages, ignoring")
			return

		username = update.message.from_user.name
		if username not in self.setup['user_to_bot']:
			self.logger.info("user " + username + " not registered")
			return

		bot_name = self.setup['user_to_bot'][username]
		user_text_name = self.setup['names'][bot_name]

		#self.logger.info()
		self.prefix_message = user_text_name + ": " + update.message.text
		self.logger.info(self.prefix_message)

		#update.message.reply_text(update.message.text)
	
	def getBotByMessage(self, message):
		for bot in self.bots:
			if message.startswith(bot.name):
				return bot

		return None

	def update(self):

		if not self.messages:
			time.sleep(1)
			return
			#self.messages = self.text_generator.getMessages()

		message = self.messages.pop(0)
		bot = self.getBotByMessage(message)
		if bot is None:
			self.logger.warning('no bot found from text')
			self.logger.warning(message)
			return self.update()

		trimmed = message[len(bot.name) + 2:]
		text_length = len(trimmed)

		if(text_length == 0 or trimmed is None):
			return self.update()

		# remove duplicates
		if(self.last_raw_message == bot.name + ": " + trimmed):
			return self.update()

		self.last_message = trimmed
		bot.talk(trimmed)
		#bot.send_voice(trimmed)

		self.last_raw_message = bot.name + ": " + trimmed


		if text_length < 150:
			time.sleep(5)
		else:
			time.sleep(10)
