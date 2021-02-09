from telegram import Update
import logging
from telegram.ext import CommandHandler, Updater, MessageHandler, Filters, CallbackContext
import time
import gpt_2_simple as gpt2
import sys
from config import Setup
import os
import random
import traceback

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
		try: 
			messages = self.text_generator.getMessages(self.prefix_message)
		except: 
			messages = []
			e = sys.exc_info()[0]
			self.logger.error(e)
			traceback.print_exc() 

		if len(messages) > 0 and messages[0] == self.prefix_message:
			messages.pop(0)
		
		self.messages = messages

		self.training = False
		self.prefix_message = None
		print(self.messages)

	def messageHandler(self, update: Update, context: CallbackContext) -> None:

		# todo ignore really old messages

		if self.training:
			self.logger.info("getting messages, ignoring")
			update.message.reply_text("Currently thinking real hard...")
			return

		username = update.message.from_user.name
		if username not in self.setup['user_to_bot']:
			update.message.reply_text("user " + username + " not registered")
			self.logger.info("user " + username + " not registered")
			return



		self.reply_message = update.message
		text = update.message.text

		# if message was a reply
		if update.message.reply_to_message and text == 'save':
			reply_message = update.message.reply_to_message
			reply_user = reply_message.from_user

			if not reply_user.is_bot:
				return


			message_to_save = reply_user.username + ': ' + reply_message.text
			update.message.reply_text('Would write: ' + message_to_save)
			return



		bot_name = self.setup['user_to_bot'][username]
		user_text_name = self.setup['names'][bot_name]

		update.message.reply_text("Asking bots about: " + update.message.text)

		self.setPrefixMessage(user_text_name, update.message.text)
		self.getPrefixMessages()

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

		if self.training:
			self.logger.warning('training ...')
			time.sleep(10)
			return

		if len(self.messages) == 0:
			self.logger.info('no messages ...')
			if self.last_prefix_time is None or time.time() - self.last_prefix_time > 60:#*5:
				bot = random.choice(self.bots)
				self.setPrefixMessage(bot.name, self.prefix_getter.getPrefix(bot, self.last_message))
				self.getPrefixMessages()
				return
			else:
				time.sleep(1)
				return
			#self.messages = self.text_generator.getMessages()
		self.logger.info('has message!')


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
		time.sleep(10)
