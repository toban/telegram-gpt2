from telegram import Update
import logging
from telegram.ext import CommandHandler, Updater, MessageHandler, Filters, CallbackContext
import time
import gpt_2_simple as gpt2
import sys
from config import Setup
import os
import random

class ChatManager:
 
	def __init__(self, chat_id, bots, setup, text_generator, prefix_getter):

		self.prefix_getter = prefix_getter
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
		self.last_prefix_time = None
		self.reply_message = None

	def getPrefixMessages(self):
		self.training = True
		messages = self.text_generator.getMessages(self.prefix_message, 256)
		
		if len(messages) > 0 and messages[0] == self.prefix_message:
			messages.pop(0)
		
		self.messages = messages

		self.training = False
		self.prefix_message = None
		print(self.messages)

	def messageHandler(self, update: Update, context: CallbackContext) -> None:
		"""Echo the user message."""
		#prefix =" print()
		print(dir(update.message))
		if self.training:
			self.logger.info("getting messages, ignoring")
			update.message.reply_text("Calcumalating ... " + self.prefix_message)
			return

		username = update.message.from_user.name
		if username not in self.setup['user_to_bot']:
			update.message.reply_text("user " + username + " not registered")
			self.logger.info("user " + username + " not registered")
			return



		self.reply_message = update.message
		bot_name = self.setup['user_to_bot'][username]
		user_text_name = self.setup['names'][bot_name]

		update.message.reply_text("Asking bots about: " + update.message.text)

		self.setPrefixMessage(user_text_name, update.message.text)
		
	def setPrefixMessage(self, bot_name, prefix_message):
		self.prefix_message = bot_name + ": " + prefix_message

		self.last_prefix_time = time.time()

		self.logger.info(self.prefix_message)

	def getBotByMessage(self, message):
		for bot in self.bots:
			if message.startswith(bot.name):
				return bot

		return None

	def update(self):

		if not self.messages:
			if self.last_prefix_time is None or time.time() - self.last_prefix_time > 60:#*5:
				bot = random.choice(self.bots)
				self.setPrefixMessage(bot.name, self.prefix_getter.getPrefix(bot))
				self.getPrefixMessages()

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
		bot.talk(trimmed, self.reply_message)
		self.reply_message = None
		#bot.send_voice(trimmed)

		self.last_raw_message = bot.name + ": " + trimmed

		word_count = len(trimmed.split())
		if word_count < 10:
			time.sleep(word_count/2)
		else:
			time.sleep(10)
