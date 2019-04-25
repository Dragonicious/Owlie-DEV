import subprocess
import threading
import os
import sys
from time import sleep
# from run import owlie

class owl:

	def __init__(self):
		pass
		# owlie = owlie()
		self.config_os() #determines OS
		self.handler = threading.Thread(target=self.owlie_handler)
		self.handler.start()
		print(str(self.handler),flush=True)

		self.ui = threading.Thread(target=self.interface)
		self.ui.start()
		print(str(self.ui),flush=True)


		CURRENT_PID = ""
		# self.interface()
		# def start(self):
		# 	self.bot_thread = threading.Thread(target=DiscordOwlie)
		# 	print("Starting bot.")
		# 	try:
		# 		self.bot_thread.start()
		# 	except Exception as start_except:
		# 		print("Starting exc ", start_except);
		# self.owlie_handler()

	def interface(self):
		while True:
			print("""Actions:
				1. Owlie status
				2. PID""",flush=True)
			action = input()

			if action == '1':
				print("Thread: " + str(self.handler.isAlive()) + " -- " + str(self.handler),flush=True)
			elif action == '2':
				print("PID: ", self.CURRENT_PID)



	def config_os(self):
		opsys = sys.platform
		if opsys in ['win32', 'win64']:
			self.platform = 'win'
		else:
			self.platform = 'linux'
		print("os:",opsys,flush=True)




	def PID_running(self):
		try:
			with open("PID.txt","r") as PID_FILE:
				PID = int(PID_FILE.read())
		except FileNotFoundError:
			return False
		except Exception as e:
			print(str(e.args))
		else:
			if(os.path.exists("/proc/"+str(PID))):
				print(".",end="",flush=True)
			else:
				print("no PID",flush=True)
			self.CURRENT_PID = str(PID)
			return os.path.exists("/proc/"+str(PID))

	def owlie_handler(self):
		
					
				
		print("Loop..", end="",flush=True)
		while True:
			if self.PID_running():
				sleep(5)
			else:
				print("starting new owlie with PID:",end="",flush=True)
				owlie = subprocess.Popen(['/bin/sh', os.path.expanduser('startup.sh')])
				# os.spawnl(os.P_DETACH, '/bin/sh', os.path.expanduser('startup.sh'))
				print(owlie.pid)
			sleep(5)

			# pass
						
owl = owl()