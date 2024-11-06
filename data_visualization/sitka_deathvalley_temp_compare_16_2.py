from pathlib import Path
import csv
from datetime import datetime
from datetime import timedelta

from matplotlib import pyplot as plt

def read_csv_file(file_path):
	path = Path(file_path)
	lines = path.read_text().splitlines()
	reader = csv.reader(lines)
	return reader

def get_temperature_range(reader, date_list, temp_range_list):
	for row in reader:
		current_date = datetime.strptime(row[0], "%Y-%m-%d")
		try:
			high_temp = int(row[1])
			low_temp = int(row[3])
		except ValueError:
			temp_range = 0
		else:
			temp_range = high_temp - low_temp

		date_list.append(current_date)
		temp_range_list.append(temp_range)

def correct_temp_range(date_list, temp_range_list):
	first_date = datetime(2014, 1, 1)
	insert_date = datetime(2014,1,1)
	date_list_temp = date_list.copy()
	j = 0
	for n in range(len(date_list_temp)):
		i = 0
		insert_date = insert_date + timedelta(days=j)
		while insert_date < date_list_temp[n]:
			i += 1
			insert_index = n + i
			insert_date = insert_date + timedelta(days=i)
			date_list.insert(insert_index, insert_date)
			temp_range_list.insert(insert_index, 0)
			insert_date = first_date + timedelta(days=i)
		j += i
		j += 1


	if len(date_list) < 365:
		k = len(date_list)
		last_date = date_list[-1]
		for n in range(365-k):
			insert_date = last_date + timedelta(days=n)
			date_list.append(insert_date)
			temp_range_list.append(0)


reader_sitka = read_csv_file("weather_data/sitka_weather_2014.csv")
reader_death_valley = read_csv_file("weather_data/death_valley_2014.csv")

header_sitka = next(reader_sitka)
header_death_valley = next(reader_death_valley)

sitka_dates = []
sitka_temperatures_range = []
death_valley_dates = []
death_valley_temperatures_range = []

# 提取数据

get_temperature_range(reader_sitka, sitka_dates, sitka_temperatures_range)
get_temperature_range(reader_death_valley,death_valley_dates,
					  death_valley_temperatures_range)
correct_temp_range(sitka_dates, sitka_temperatures_range)
correct_temp_range(death_valley_dates, death_valley_temperatures_range)

print(sitka_dates)
print(sitka_temperatures_range)
print(death_valley_dates)
print(death_valley_temperatures_range)

# 根据sitka和death_valley的最高、最低气温差列表，进行绘图
plt.style.use('seaborn-v0_8')
fig, ax = plt.subplots()
ax.plot(sitka_dates, sitka_temperatures_range, color='blue', label='Sitka')
ax.plot(sitka_dates, death_valley_temperatures_range, color='red',
		label='Death Valley')

# 设置绘图格式
title = "Temperature Range in Sitka and Death Valley, 2014"
ax.set_title(title, fontsize=20)
ax.set_xlabel('', fontsize=16)
fig.autofmt_xdate()
ax.set_ylabel('Temperature Range (F)', fontsize=16)
ax.tick_params(labelsize=14)

plt.legend()
plt.show()



