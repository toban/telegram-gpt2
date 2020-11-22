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

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

bots = []

for bot in Setup.config['tokens']:
	bots.append(Bot(Setup.config['tokens'][bot], Setup.config['names'][bot], Setup.config['voice_pitch'][bot]))

text_generator = TextGenerator()
manager = ChatManager(Setup.config['chat_id'], bots, Setup.config, text_generator)
while True:
	if manager.prefix_message:
		manager.training = True
		manager.messages = manager.text_generator.getMessages(manager.prefix_message, 256)
		manager.training = False
		manager.prefix_message = None
		print(manager.messages)
	else:
		manager.update()


print('hello')