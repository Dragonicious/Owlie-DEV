import json
from Classes.Sql import Sql
# from Classes.Optimizer import Optimizer

# Opti = Optimizer()

# exit(0)
Sql = Sql(True)


task = 420
while task != 0:
	print("Whatchya wanna do?")
	print("	1	-	Build")
	# task = int(input())
	task = 1
	print("Task: ",task )
	if task == 1:
		print("Rebuilding hourly table...")
		all_data = Sql.get(
			"SELECT * FROM `stats` WHERE 1"
		)


		opti = {}
		for row in all_data:
			timestamp 	= row['TIME']
			chnl = str(row['CHANNEL'])
			day 		= str(timestamp.date())
			rechour		= int(timestamp.hour)
			
			try:
				len(opti[day])
			except KeyError:
				opti[day] = {}
			else:
				try:
					len(opti[day][chnl])
				except KeyError:
					opti[day][chnl] = {}
					for hour in range(0,24):
						opti[day][chnl][hour] = {
							'count' : 0,
							'length': 0,
							'embeds': 0
						}
				else:
					opti[day][chnl][rechour]['count'] += 1
					opti[day][chnl][rechour]['length'] += int(row['LENGTH'])
					opti[day][chnl][rechour]['embeds'] += int(row['EMBEDS'])
					


					# if rechour == hour: 
						# print (rechour, hour)

		# for day in opti:
		# 	print(opti[day])

		Sql.put("DELETE FROM `stats_opti_h` WHERE 0")
		# print(json.dumps(opti))
		
		for day in opti:
			print (day)
			# print(json.dumps(opti[day]))

			for channel in opti[day]:
				date_str = str(day) + ' ' + str(hour) + ':00'
				print(channel, end= ' - ')
				for hour in opti[day][channel]:
					count 	= opti[day][channel][hour]['count']
					length 	= opti[day][channel][hour]['length']
					embeds 	= opti[day][channel][hour]['embeds']

					print(hour,':',count)
					Sql.put("INSERT INTO `stats_opti_h`"\
						"(`TIME`, `CHANNEL`, `COUNT`, `LENGTH`, `EMBEDS`) "\
						"VALUES (%s,%s,%s,%s,%s)",
					[date_str, channel, int(count),length,embeds])
					
				
				# print(channel)
				# print(json.dumps(opti[day][channel]))

				# print (hour, end=' ')
				# print (opti[day][hour]['count'] )

			# Sql.put(
			# 	"INSERT INTO `stats_opti_h`(`TIME`, `CHANNEL`, `COUNT`, `LENGTH`, `EMBEDS`) VALUES (%s,%s,%s,%s,%s)",
			# 	[day,]
			# ) 

		print("OOF!!")
	else:
		print(task, " != 1")
	task = 0
	 


# print("Starting database optimization...")

