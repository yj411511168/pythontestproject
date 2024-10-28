import sys

import pygame

from settings import Settings
from ship import Ship

class AlienInvasion:
	"""管理游戏资源和行为的类"""
	def __init__(self):
		"""初始化游戏并创建游戏紫苑"""
		pygame.init()
		self.clock = pygame.time.Clock()
		self.settings = Settings()
		self.screen = pygame.display.set_mode((self.settings.screen_width,
											   self.settings.screen_height))
		pygame.display.set_caption("Alien Invasion")
		self.ship = Ship(self)

		#设置背景色
		self.bg_color = self.settings.bg_color

	def _check_keydown_events(self, event):
		"""响应按下"""
		if event.key == pygame.K_RIGHT:
			self.ship.moving_right = True
		elif event.key == pygame.K_LEFT:
			self.ship.moving_left = True
		elif event.key == pygame.K_q:
			sys.exit()

	def _check_keyup_events(self, event):
		"""响应松开"""
		if event.key == pygame.K_RIGHT:
			self.ship.moving_right = False
		elif event.key == pygame.K_LEFT:
			self.ship.moving_left = False

	def _check_events(self):
		"""相应按键和鼠标事件"""
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				self._check_keydown_events(event)
			elif event.type == pygame.KEYUP:
				self._check_keyup_events(event)

	def _update_screen(self):
		"""更新屏幕上的图形，并切换到新屏幕"""
		self.screen.fill(self.settings.bg_color)
		self.ship.blitme()

		pygame.display.flip()


	def run_game(self):
		"""开始游戏主循环"""
		while True:
			# 侦听键盘和鼠标事件
			self._check_events()
			self.ship.update()
			# 每次循环都会重绘屏幕
			self._update_screen()
			self.clock.tick(60)

if __name__ == '__main__':
	# 创建游戏实例并运行游戏
	ai = AlienInvasion()
	ai.run_game()

