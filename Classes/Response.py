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

		# next_word = 0
		i_replied = False
		for expected_word in current_tree:
			#try to find a start of an expected phrase, starting with each word ?
			for actual_word_id in range(0, len(self.words)):
				actual_word = self.words[actual_word_id]
				# print ("expected-word: ", expected_word,  "matching with: ", actual_word)
				
				if actual_word == expected_word and not i_replied:
					# print("lvl/word: ",next_word, "match at:  ",expected_word, " == ", actual_word)
					#if i find a matching key 
					next_tree = current_tree[expected_word]
					# print(" ========== found, next tree: ", next_tree, type(next_tree))

					request = next_tree
					#check if type of matched key's value is an answer:
					if isinstance(request, self.Reply): #type(request) is self.Reply:
						# print('-------- Replying')
						await self.bot.send_message(self.message.channel, request.msg())
						return True

					elif type(request) is self.Action:
						# print("------- Executing: ", request.do)
						await self.execute_action(request, actual_word_id)
						return True

					elif type(next_tree) is dict or type(next_tree) is list:
						#look for next word in next tree = next expected word
						# print('digging deeper to ', next_tree)
						next_level = await self.respond(next_word+1, next_tree)
						if next_level == True:
							# print("lvl/word: ",next_word, "break  at:  ",expected_word, " == ", actual_word)
							return True
							# print("i replied", next_level)
							i_replied = True
							break
					else:
						pass 
				else:
					#look for next word in currnt tree
					pass
			if i_replied:
				break
		return False
				

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
