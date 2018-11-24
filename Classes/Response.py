import re
import random
from config import config
# from Classes.Answer import Answer
from Classes.Interpreter import Interpreter
from Classes.Dictionary import Dictionary

class Response:
	tree = {}

	def __init__(self, bot, message):
		self.bot = bot
		self.message = message
		# message.conent.replace()
		self.words = Interpreter.parse(message.content.replace(config.bot_mention, ""))

		# self.pick_response(self.words, 0)
		# return None

	class Action:
		def __init__(self,action_name):
			self.do = action_name
	class Reply:
		def __init__(self, possible_replies):
			self.answers = possible_replies
		def msg(self):
			return self.answers[random.randint(0, len(self.answers))-1] #return a random asnwer


	async def pick_response(self, at_word = 0, tree = None):
		words = self.words
		if tree == None and at_word == 0:
			tree = self.responses
		# if type(words) is str:
		# 	words = Interpreter.parse(words)
		print(at_word)
		for branch in tree:
			print("Checking in : ", branch)
			for word in words:
				word_checks = branch.split(' ')
				if word in word_checks and word != '':
					print('Found: ', word)
					#____________________________ things to do _________________________
					if type(tree[branch]) is self.Reply:
						print('replying')
						await self.bot.send_message(self.message.channel, tree[branch].msg())
						# return None

					elif type(tree[branch]) is self.Action:
						print("------- Executing: ", tree[branch].do)
						if tree[branch].do == 'define':
							
							try:
								embed_content = Dictionary(words[int(at_word)+1:]).embed()
								await self.bot.send_message(self.message.channel, "would embed definition"+embed_content)
							except Exception as inst:
								await self.bot.send_message(self.message.channel, "Congratulations, you broke me: ```py "+str(inst)+" ```")
							# return None

					#__________________________________________________________________
					else:
						print("LOOKING FOR NEXT")
						if tree[branch]:
							further_check = await self.pick_response(at_word+1, tree[branch])
							if further_check == False:
								continue
							else:
								return further_check 
				else:
					at_word += 1
					continue
		return None

		
	owlies_maker = Reply([
		"<@308661300039385088> is my daddy!"
		,"<@308661300039385088> made me. ^^"
		,"I thank <@308661300039385088> for my artificial life."
	])
	introduction = Reply([
		"I'm a friendly owl, who looks over this server. My job is to get rid of spammers, mostly."
	])
	who_are_you = Reply([
		"Just a friendly neighborhood owl. ^^"
		,"I'm an owl, duh.."
		,"I'm a cyborg-owl *beep boop*."
		,"I bet you'd like to know.."
		,"Just an artificial owl."
		,"*I AM YOUR GOD!*"
		,"None of your business >.>"
	])

	define = Action('define')


	responses = {
		'define' : define

		,'who what' : {
			'are is' : {
				'you owlie' : who_are_you
			}
		}
		,"who's who" : {
			"is " : {
				"your ur thy owlie's" : {
					"owner creator maker programmer coder" : owlies_maker
				}
			}
			,"made created coded programmed" : {
				"you owlie u" : owlies_maker
			}
		}
		,'introduce tell-us-about ' : {
			'yourself thyself' : introduction
		}
	}
#========================================= testing 
# import re

# def prase_message(message):
# 	initial_string = str(message)
# 	pure_string = re.sub('[^A-Za-z0-9 ]+', '', initial_string)
# 	clean_string = re.sub(' +', ' ', pure_string)
# 	word_array = clean_string.split(" ")
# 	return word_array


# words = prase_message("Hi owlie,	  introduce yourself, please ^^")
# print(words)

# re = Response();
# re.respond_to(words)
