import matplotlib.pyplot as plt

x_values = range(1, 1001)
y_values = [x ** 2 for x in x_values]

plt.style.use('seaborn-v0_8')
fig, ax = plt.subplots()
ax.scatter(x_values, y_values, c=y_values, cmap=plt.cm.Blues, s=10)

# 设置图标并给坐标轴加上标签
ax.set_title('scatter-squares', fontsize=24)
ax.set_xlabel('Values', fontsize=14)
ax.set_ylabel('Squares of values', fontsize=14)
ax.tick_params(labelsize=14)
ax.axis([0, 1100, 0, 1_100_000])

plt.show()
plt.savefig('squeres_plot.png')
