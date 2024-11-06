from plotly.express import scatter_3d

from die import Die
import plotly.express as px

#创建一个D6骰子和一个D10骰子
die_1 = Die()
die_2 = Die(10)

#投掷几次骰子并将结果存储在一个列表中
results = []

for roll_num in range(50_000):
	result = die_1.roll() + die_2.roll()
	results.append(result)

# 分析结果
frequencies = []
max_result = die_1.num_sides + die_2.num_sides
poss_results = range(2, max_result+1)
for value in poss_results:
	frequency = results.count(value)
	frequencies.append(frequency)

# 结果可视化
fig_title = "Results of Rolling D6 and D10 50000 Times"
fig_labels = {'x': 'Result', 'y': 'Frequency of Result'}
fig = px.bar(x=poss_results, y=frequencies, title=fig_title,
			 labels=fig_labels)
# fig = px.line(x=poss_results, y=frequencies)
# fig = px.scatter(x=poss_results, y=frequencies)
# 进一步定制图形
fig.update_layout(xaxis_dtick=1)

fig.show()
fig.write_html("dice_visual_d6d10.html")
