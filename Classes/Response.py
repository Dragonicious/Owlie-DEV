import re
import random

import sys
from config import config
# from Classes.Answer import Answer
from Classes.Interpreter import Interpreter
from Classes.Dictionary import Dictionary
from Classes.Reactions import Reactions

class Response:
	tree = {}

	def __init__(self, bot, message):
		self.bot = bot
		self.message = message
		self.words = Interpreter.parse(message.content.replace(config.bot_mention, ""))
		# print("words at init: ", self.words)


	class Action:
		def __init__(self,action_name):
			self.do = action_name
	class Reply:
		def __init__(self, possible_replies):
			self.answers = possible_replies
		def msg(self):
			return self.answers[random.randint(0, len(self.answers))-1] #return a random asnwer


	async def respond(self, next_word = 0, current_tree = None):
		if current_tree == None:
			current_tree = self.word_tree

		word_id = 0
		for expected_word in current_tree:
			#try to find a start of an expected phrase, starting with each word ?
			for actual_word_id in range(0, len(self.words)):
				actual_word = self.words[actual_word_id]
				print ("expected-word: ", expected_word,  "matching with: ", actual_word)
				
				if actual_word == expected_word:
					#if i find a matching key 
					next_tree = current_tree[expected_word]
					print(" ========== found, next tree: ", next_tree, type(next_tree))

					if type(next_tree) is dict or type(next_tree) is list:
						#look for next word in next tree = next expected word
						await self.respond(word_id+1, next_tree)

					else:
						request = next_tree
						#check if type of matched key's value is an answer:
						if isinstance(request, self.Reply):
							print('-------- Replying')
							await self.bot.send_message(self.message.channel, request.msg())
							return None

						elif type(request) is self.Action:
							print("------- Executing: ", request.do)
							await self.execute_action(request, next_word)
				else:
					#look for next word in currnt tree
					pass




	async def execute_action(self, action, next_word = None):
		if action.do == 'define':
			try:
				#request next words after 'define' 
				answer = Dictionary(self.words[int(next_word+1):]).embed()
			except Exception as ex:
				if (ex.args[0] == '404'):
					#phrase not found
					await Reactions(self.bot, self.message).add('huh?')
				else:
					#some other error
					print(ex.args)
					await Reactions(self.bot, self.message).add('error')
				return None
			else:
				if answer:
					await self.bot.send_message(self.message.channel, "", embed = answer)
				return None
		else:
			return None










	async def pick_response(self, at_word = 0, tree = None):
		init_at_word = at_word
		# words = self.words
		if tree == None and at_word == 0:
			tree = self.tree
		# print(tree);
		# print(at_word)
		for branch in tree:
			# print("Checking in : ", branch) 
			for word in self.words:
				word_checks = branch.split(' ')
				if word in word_checks and word != '':
					print('Found: ', word, tree[branch])
					#____________________________ things to do _________________________
					if isinstance(tree[branch], self.Reply):
						print('-------- Replying')
						await self.bot.send_message(self.message.channel, tree[branch].msg())
						return False

					elif type(tree[branch]) is self.Action:
						print("------- Executing: ", tree[branch].do)
						if tree[branch].do == 'define':
							try:
								answer = Dictionary(self.words[int(at_word+1):]).embed()
							except Exception as ex:
								if (ex.args[0] == '404'):
									await Reactions(self.bot, self.message).add('huh?')
								else:
									await Reactions(self.bot, self.message).add('error')
								return False
							else:
								if answer:
									await self.bot.send_message(self.message.channel, "", embed = answer)
								else:
									await Reactions(self.bot, self.message).add('error')
								return False

					#__________________________________________________________________
					else:
						# print("LOOKING FOR NEXT")
						if tree[branch]:
							further_check = await self.pick_response(at_word+1, tree[branch])
							if further_check == False:
								continue
							else:
								return further_check 
				else:	
					at_word += 1
					continue
			at_word = 0
		return False

		
	my_maker_is = Reply([
		config.owner_mention + " is my daddy!"
		,config.owner_mention + " made me. ^^"
		,"I thank <@308661300039385088> for my artificial life."
	])
	introduction = Reply([
		"I'm a friendly owl, who looks over this server. My job is to get rid of spammers, mostly."
	])
	who_am_i = Reply([
		"Just a friendly neighborhood owl. ^^"
		,"I'm an owl, duh.."
		,"I'm a cyborg-owl *beep boop*."
		,"I bet you'd like to know.."
		,"Just an artificial owl."
		,"*I AM YOUR GOD!*"
		,"None of your business >.>"
	])
	what_i_do = Reply([
		"In my free time i enjoy contemplating ones and zeroes."
	])

	define = Action('define')


	word_tree = {
		'define' : define

		,'who'	: {
			'are'	: {
				'you' : who_am_i
			}
			,'is'	: {
				'owlie' : who_am_i
				,'your'	: {
					'creator maker coder owner'	: my_maker_is
				}
			}
			,'made'	: {
				'you' : my_maker_is
			}
		}
		,'whos':	{
			'owlie' : who_am_i
			,'your'	: {
				'creator maker coder owner'	: my_maker_is
			}
		}
		,'what'	: {
			'are'	: {
				'you' : {
					who_am_i
				}
			}
			,'do'	: {
				'you'	: {
					'do'	: what_i_do
				}
			}
		}
	}
