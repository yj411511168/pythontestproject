class Game_Status:
	"""跟踪统计游戏信息"""

	def __init__(self, ai_game):
		"""初始化统计信息"""
		self.settings = ai_game.settings
		self.reset_stats()
		self.high_score = 0

	def reset_stats(self):
		"""初始化随游戏进行可能变化的统计信息"""
		self.ship_left = self.settings.ship_limit
		self.score = 0
		self.level = 1


