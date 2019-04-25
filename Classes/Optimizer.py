from Classes.Sql import Sql


class Optimizer:
	def __init__(self):
		self.db = self.prompt_db()
		self.Sql = Sql(True, self.db)
		self.table = self.prompt_table()
		

	def prompt_db(self):
		print('Select database:')
		print("\t1 - discord")
		nr = int(input())
		if nr == 1 :
			return "discord"

	def prompt_table(self):
		id = 0
		tlist = self.table_list()
		print("Select table:")
		for table in tlist:
			print("\t",id, str(table))
			id +=1

		nr = input()
		return tlist[nr]


	def table_list(self):
		lines = self.Sql.get("SHOW TABLES IN "+str(self.db))
		return [table['Tables_in_'+self.db] for table in lines]
