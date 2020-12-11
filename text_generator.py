from telegram import Update
import logging
from telegram.ext import CommandHandler, Updater
import time
import gpt_2_simple as gpt2
import sys
from config import Setup
import os

class TextGenerator:
 
	def __init__(self):
		self.logger = logging.getLogger('TextGenerator')
		self.sess = gpt2.start_tf_sess()

	def getMessages(self, prefix=None, length=1023):
		self.logger.info("generating new texts ...")
		self.sess = gpt2.reset_session(self.sess)
		gpt2.load_gpt2(self.sess)
		generated = gpt2.generate(self.sess, model_name="124M", return_as_list=True, prefix=prefix, length=length, temperature=1.0)
		single_text = generated[0]
		#f = open("demofile2.txt", "a")
		#f.write(single_text)
		#f.write("\n")
		#f.close()
		self.logger.info("done generating!")

		return single_text.splitlines()