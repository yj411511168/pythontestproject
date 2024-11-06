from matplotlib import pyplot as plt

x_values = range(1, 5001)
y_values = [x ** 3  for x in x_values]

plt.style.use('seaborn-v0_8')
fig, ax = plt.subplots()
ax.scatter(x_values, y_values, c=y_values, cmap=plt.cm.Reds, s=1)

# 设置图题，轴标签
ax.set_title("Scatter-Cubic", fontsize=24)
ax.set_xlabel("Values", fontsize=14)
ax.set_ylabel("Cubic Values", fontsize=14)
ax.tick_params(labelsize=10)
ax.axis([0, 5100, 0, 130_500_000_000])



plt.show()
plt.savefig('cubics_plot.png')
