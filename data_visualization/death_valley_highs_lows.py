from pathlib import Path
import csv
from datetime import datetime

from matplotlib import pyplot as plt

path = Path('weather_data/death_valley_2014.csv')
lines = path.read_text().splitlines()

reader = csv.reader(lines)
header_row = next(reader)

for index, column_header in enumerate(header_row):
	print(index, column_header)

# 提取最高温度
dates, highs, lows = [], [], []
for row in reader:
	current_date = datetime.strptime(row[0], '%Y-%m-%d')
	try:
		high = int(row[1])
		low = int(row[3])
	except ValueError:
		print(f"Missing data for {current_date}")
	else:
		dates.append(current_date)
		highs.append(high)
		lows.append(low)

# 根据最高温度绘图
plt.style.use('seaborn-v0_8')
fig, ax = plt.subplots()
ax.plot(dates, highs, color='red', alpha=0.5)
ax.plot(dates, lows, color='blue', alpha=0.5)
ax.fill_between(dates, highs, lows, color='blue', facecolor='blue',
			   alpha=0.1)

# 设置绘图格式
title = "Daily High Temperatures and Low Temperatures, 2014\nDeath Valley, CA"
ax.set_title(title, fontsize=2)
ax.set_xlabel('', fontsize=16)
fig.autofmt_xdate()
ax.set_ylabel("Temperature (F)", fontsize=16)
ax.tick_params(labelsize=16)

plt.show()