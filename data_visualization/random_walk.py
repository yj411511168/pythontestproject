from random import choice

class RandomWalk:
	"""一个生成随机游走数据的类"""

	def __init__(self, num_points=5000):
		"""初始化随机游走的属性"""
		self.num_points = num_points

		# 所有速记游走都始于（0, 0）
		self.x_values = [0]
		self.y_values = [0]

	def get_step(self):
		direction = choice([1, -1])
		distance = choice([0, 1, 2, 3, 4])
		step = direction * distance
		return step

	def fill_walk(self):
		"""计算随机游走包含的所有店"""

		# 不断游走，直到达到制定数量的点
		while len(self.x_values) < self.num_points:
			# 决定前进的方向以及距离
			x_step = self.get_step()
			y_step = self.get_step()

			# 拒绝原地踏步
			if x_step == 0 and y_step == 0:
				continue

			# 计算下一个点的坐标
			x_next = self.x_values[-1] + x_step
			y_next = self.y_values[-1] + y_step
			# 加入坐标
			self.x_values.append(x_next)
			self.y_values.append(y_next)