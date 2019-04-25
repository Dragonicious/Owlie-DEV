from time import sleep
import sys
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


		# sleep(15)
		# sys.exit()
		bot 		= discord.Client()
		config		= config()
		Reader 		= Reader(bot, None)

		logging.basicConfig(filename='events.log', 			format='%(asctime)s %(levelname)s:%(message)s', level=logging.INFO)

		@bot.event
		async def on_ready():
			print("Owlie's ready! ^^")

		@bot.event
		async def on_message(message):
			if message.server.id == config.server and message.author != bot.user:
				#if message is in configured server and isn't the bot's message
				await Reader.read(message)

		@bot.event
		async def on_member_join(member):
			await bot.send_message(discord.Object(id=config.main_channel), "Hi "+member.mention+"! Nepamiršk paskaityti #info ir prisistatyti ^^ !")

		bot.run(config.bot_key)
# logging.info('Owlie: Ready!')

def run(tries = 0):
	print("CRASHES SO FAR:", tries)
	# try:
	owlie()
	# except:
		# print(e1)
		# run(tries+1)
	

run()
# sleep(15)