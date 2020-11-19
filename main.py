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

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

bots = []

for bot in Setup.config['tokens']:
	bots.append(Bot(Setup.config['tokens'][bot], Setup.config['names'][bot], Setup.config['voice_pitch'][bot]))

def start(update, context):
    #print(update.effective_chat.id)
    context.bot.send_message(chat_id=chat_id, text="I'm a bot, please talk to me!")

manager = ChatManager(Setup.config['chat_id'], bots, Setup.config)
while True:
	manager.update()


print('hello')