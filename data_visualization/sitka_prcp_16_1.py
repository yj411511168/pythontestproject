from pathlib import Path
from datetime import datetime
import csv

from matplotlib import  pyplot as plt

def read_csv_file(file_path):
	path = Path(file_path)
	lines = path.read_text().splitlines()
	reader = csv.reader(lines)
	return reader

sitka_datas = read_csv_file('weather_data/sitka_weather_2014.csv')
header_row = next(sitka_datas)

for index, column_header in enumerate(header_row):
	print(index, column_header)

dates, prcps = [], []
for row in sitka_datas:
	current_date = datetime.strptime(row[0], '%Y-%m-%d')
	try:
		prcp = float(row[19])
	except ValueError:
		print(f"Missing data for {current_date}")
	else:
		dates.append(current_date)
		prcps.append(prcp)

# 根据每日降水量绘制折线图
plt.style.use('seaborn-v0_8')
fig, ax = plt.subplots()
ax.plot(dates, prcps, color='green')

# 设置绘图格式
fig_title = "Daily Precipitation - 2014 for Sitka, Alaska"
ax.set_title(fig_title, fontsize=20)
ax.set_xlabel('', fontsize=16)
ax.set_ylabel('Precipitation (inches)', fontsize=16)
ax.tick_params(labelsize=16)

plt.show()