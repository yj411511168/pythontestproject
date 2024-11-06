from pathlib import Path
import csv
import pandas as pd
import plotly.express as px

path = Path('eq_data/world_fires_7_day.csv')
lines = path.read_text().splitlines()

reader = csv.reader(lines)
header_row = next(reader)
for index, column_header in enumerate(header_row):
	print(index, column_header)

lons, lats, brights = [], [], []

for row in reader:
	try:
		lon = float(row[1])
		lat = float(row[0])
		bright = float(row[2])
	except ValueError:
		continue
	else:
		lons.append(lon)
		lats.append(lat)
		brights.append(bright)

data = pd.DataFrame(
	zip(lons, lats, brights), columns=['经度', '维度', '火灾强度']
)

fig = px.scatter(
	data,
	x='经度',
	y='维度',
	range_x=[-200, 200],
	range_y=[-100, 100],
	width=800,
	height=800,
	title='全球火灾散点图',
	size='火灾强度',
	size_max=10,
	color='火灾强度'
)

fig.show()