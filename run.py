import logging
logging.basicConfig(filename='events.log', 			format='%(asctime)s %(levelname)s:%(message)s', level=logging.INFO)

logger = logging.getLogger('rpi')
logger.setLevel(logging.DEBUG)

logFormatter = logging.Formatter("%(asctime)s | %(threadName)-12.12s | %(levelname)-10.10s | %(message)s","%m-%d %H:%M:%S")

consoleLogger = logging.StreamHandler()
consoleLogger.setLevel(logging.DEBUG)
consoleLogger.setFormatter(logFormatter)

fileLogger = logging.FileHandler(r'debug.log')
fileLogger.setLevel(logging.DEBUG)
fileLogger.setFormatter(logFormatter)

logger.addHandler(consoleLogger)
logger.addHandler(fileLogger)

from time import sleep
import sys


crash_count = 0


class owlie:
	def __init__(self):
		import os
		import discord
		import logging
		from Classes.Reader import Reader
		from config import config

		PID = os.getpid()
		with open("PID.txt","w") as PID_FILE:
			PID_FILE.write(str(PID))
			logger.debug('Process trace created: ' + str(PID))

		bot 		= discord.Client()
		config		= config()
		Reader 		= Reader(bot, None)

		@bot.event
		async def on_ready():
			logger.debug('Owlie - ready! ' + str('Current run attempts: ') + str(crash_count))

		@bot.event
		async def on_message(message):
			if message.content == 'DIE' and message.author.id == config.owner_id:
				raise ValueError('controlled crash')
			if message.content == 'EXIT' and message.author.id == config.owner_id:
				exit()

			if message.guild.id == config.server and message.author != bot.user:
				await Reader.read(message)

		@bot.event
		async def on_member_join(member):
			await Reader.welcome(message)
			await bot.send_message(discord.Object(id=config.main_channel), "Hi "+member.mention+"! Nepamiršk paskaityti #info ir prisistatyti ^^ !")

		bot.run(config.bot_key)



def run(crash_count = 0, last_exception = None):
	
	try:
		owlie()
	except Exception as e:
		logger.critical('Owlie died:\n ' + str(e.__class__.__name__)+'\n'+str(e.args))
		crash_count += 1
		if e.args == last_exception:
			sleep(5)
			run(crash_count, e.args)
		else:
			sleep(0.1)
			run(crash_count, e.args)

run()