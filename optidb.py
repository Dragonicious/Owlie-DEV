from Classes.Sql import Sql



task = 420
while task != 0:
	print("Whatchya wanna do?")
	print("	1	-	Build")
	task = int(input())
	print("Task: ",task )
	if task == 1:
		print("Rebuilding hourly table...")
		all_data = Sql.get(
			"SELECT * FROM `stats` WHERE 1"
		)
		print(all_data)
		print("OOF!!")
	else:
		print(task, " != 1")
	 


print("Starting database optimization...")

