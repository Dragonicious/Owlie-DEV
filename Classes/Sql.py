import json
import MySQLdb
import MySQLdb.cursors
from config import config


class Sql:
	db = cursor = None
	def __init__(self):
		pass
		# self.connect
		

	def connect(self):
		self.db 	= MySQLdb.connect(
			host		= config.db_host
			,user		= config.db_user
			,passwd		= config.db_passwd
			,db			= config.db_db
			,connect_timeout = config.db_connect_timeout
			,cursorclass=MySQLdb.cursors.DictCursor
		)
		self.db.set_character_set('utf8')
		self.cursor = self.db.cursor()

	def disconnect (self):
		self.db.close()
		# self.cursor.close()
		# self.cursor = None

	def get(self, query, arguments=[]):
		self.connect()
		self.cursor.execute(query, arguments)
		result = self.cursor.fetchall()
		self.disconnect()
		return result

	def put(self, query, arguments=[]):
		self.connect()
		execute = self.cursor.execute(query, arguments)
		self.db.commit()
		self.disconnect()
		return execute

	def get_all_subjects(self):
		#get subject data
		data = self.get("SELECT * FROM `members`")
		print('INITIAL DATA: ',data)
		return data

	def renew(self, subject):
		query = "UPDATE `members` "\
			"SET `NAME`=%s,`LAST_MESSAGE`=%s,`LAST_EMBED`=%s,`LAST_TIMESTAMP`=%s, `WARNINGS`=%s, `ACTIONS` = %s "\
			"WHERE `AUTHOR` = %s"

		warnings = json.dumps(subject.warnings)
		actions = json.dumps(subject.actions)
		vals = (subject.name, subject.last_message, subject.last_embed, subject.last_timestamp, warnings, actions, subject.id)
		self.put(query, vals)

	def add_subject(self, subject):
		query = "INSERT INTO `members` "\
			"(`AUTHOR`, `NAME`, `SPAM_IDENT`, `SPAM_RND`, `LAST_MESSAGE`, `LAST_EMBED`, `LAST_TIMESTAMP`, `WARNINGS`, `ACTIONS`) "\
			"VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
		vals = (subject.id, subject.name, subject.identical_spam, subject.random_spam, subject.last_message, subject.last_embed, subject.last_timestamp, subject.warnings, subject.actions)
		self.put(query, vals)
		
		
		
		
		
		
		
		
		