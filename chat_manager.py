from telegram import Update
import logging
from telegram.ext import CommandHandler, Updater
import time
import gpt_2_simple as gpt2
import sys
from config import Setup
import os

class ChatManager:
 
	def __init__(self, chat_id, bots, setup):

		self.last_message = None
		self.chat_id = chat_id
		self.bots = bots
		self.messages = []
		self.messagesSwap = []
		self.setup = setup
		self.logger = logging.getLogger('ChatManager')
		self.sess = gpt2.start_tf_sess()
		gpt2.load_gpt2(self.sess)

	def getBotByMessage(self, message):
		for bot in self.bots:
			if message.startswith(bot.name):
				return bot

		return None

	def update(self):

		if not self.messages:
			self.getMessages()

		message = self.messages.pop()
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
		if(self.last_message == trimmed):
			return self.update()

		self.last_message = trimmed
		#bot.talk(trimmed)
		bot.send_voice(trimmed)


		if text_length < 150:
			time.sleep(5)
		else:
			time.sleep(10)

	def getMessagesFromNetwork(self):
		self.logger.info("generating new texts ...")
		generated = gpt2.generate(self.sess, model_name="124M", return_as_list=True)
		single_text = generated[0]
		
		#f = open("demofile2.txt", "a")
		#f.write(single_text)
		#f.write("\n")
		#f.close()
		self.logger.info("done generating!")

		return single_text.splitlines()


	def getMessages(self):
		messages = self.getMessagesFromNetwork()

		self.messages = messages
