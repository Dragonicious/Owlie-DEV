import requests
import json
from config import config

class Dictionary:
	language = 'en'
	def __init__(self, words):
		self.words = words
		print(words)
		print("Defining: ", words[0])
		# self.define(words[0])

	def define(self, word):
		url = config.dict_link + self.language + '/' + str(word).lower()
		req = requests.get(url, headers= {'app_id':config.dict_app_id, 'app_key':config.dict_app_key})
		self.serialized_result(req.json())
		
	def serialized_result(self, result):
		ret = {}
		data = result['results'][0]
		ret['word'] = data['id']
		ret['definition'] = data['lexicalEntries'][0]['entries'][0]['senses'][0]['definitions'][0]

		return ret

	def embed(self):
		return "definition for: `"+self.words+'`'


# res = Dictionary().define('dragon')
# print("code {}\n".format(res.status_code))
# print("text \n" + res.text)
# print("json \n" + json.dumps(res.json()))

# print(res)