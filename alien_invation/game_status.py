class Game_Status:
	"""跟踪统计游戏信息"""

	def __init__(self, ai_game):
		"""初始化统计信息"""
		self.settings = ai_game.settings
		self.reset_stats()

	def reset_stats(self):
		self.ship_left = self.settings.ship_limit

