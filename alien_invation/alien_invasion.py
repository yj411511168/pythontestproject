import sys
from time import sleep

import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_status import Game_Status
from button import Button
from scoreboard import Scoreboard

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
		self.game_status = Game_Status(self)
		self.sb = Scoreboard(self)
		self.ship = Ship(self)
		self.bullets = pygame.sprite.Group()
		self.aliens = pygame.sprite.Group()
		self.game_active = False
		self.button = Button(self, "Play")

		self._create_fleet()

		#设置背景色
		self.bg_color = self.settings.bg_color

	def _check_keydown_events(self, event):
		"""响应按下"""
		if event.key == pygame.K_RIGHT:
			self.ship.moving_right = True
		elif event.key == pygame.K_LEFT:
			self.ship.moving_left = True
		elif event.key == pygame.K_SPACE:
			self._fire_bullet()
		elif event.key == pygame.K_q:
			sys.exit()

	def _check_keyup_events(self, event):
		"""响应松开"""
		if event.key == pygame.K_RIGHT:
			self.ship.moving_right = False
		elif event.key == pygame.K_LEFT:
			self.ship.moving_left = False

	def _check_play_button(self, mouse_pos):
		"""响应点击“Play”按钮时开始游戏"""
		# 重置游戏状态，并开始新游戏
		button_clicked = self.button.rect.collidepoint(mouse_pos)
		if button_clicked and (not self.game_active):
			#还原游戏设置
			self.settings.initialize_dynamic_settings()
			self.game_status.reset_stats()
			self.sb.prep_score()
			self.sb.prep_level()
			self.sb.prep_ships()
			self.game_active = True

			# 清空外星人列表和子弹列表
			self.aliens.empty()
			self.bullets.empty()

			# 创建一个新的外星人舰队，病假飞船重新放置在屏幕底部中央
			self._create_fleet()
			self.ship.center_ship()

			# 隐藏“Play”按钮
			pygame.mouse.set_visible(False)

	def _check_events(self):
		"""相应按键和鼠标事件"""
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			elif event.type == pygame.MOUSEBUTTONDOWN:
				mouse_pos = pygame.mouse.get_pos()
				self._check_play_button(mouse_pos)
			elif event.type == pygame.KEYDOWN:
				self._check_keydown_events(event)
			elif event.type == pygame.KEYUP:
				self._check_keyup_events(event)

	def _fire_bullet(self):
		"""创建一颗子弹，并将其加入到编组bullets"""
		if len(self.bullets) < self.settings.bullets_allowed:
			new_bullet = Bullet(self)
			self.bullets.add(new_bullet)

	def _update_bullets(self):
		"""更新子弹的位置和删除已消失的子弹"""
		self.bullets.update()

		# 删除已消失的子弹
		for bullet in self.bullets.copy():
			if bullet.rect.bottom <= 0:
				self.bullets.remove(bullet)

		self._check_bullet_alien_collisions()

	def _check_bullet_alien_collisions(self):
		"""检查子弹与外星人的碰撞"""
		# 删除发生碰撞的子弹和外星人
		collisions = pygame.sprite.groupcollide(
			self.bullets, self.aliens, True, True)

		if collisions:
			for aliens in  collisions.values():
				self.game_status.score += self.settings.alien_points * len(
					aliens)
			self.sb.prep_score()
			self.sb.check_high_score()

		if not self.aliens:
			# 删除现有的所有子弹并穿件一个新的外星人舰队
			self.bullets.empty()
			self._create_fleet()
			self.settings.increase_speed()

			# 提高等级
			self.game_status.level += 1
			self.sb.prep_level()

	def _create_fleet(self):
		"""穿件外星人舰队"""
		#创建一个外星人，在不断添加，直到没有空间添加外星人为止
		#外星人的间距为外星人宽度和高度
		alien = Alien(self)
		alien_width, alien_height = alien.rect.size
		current_x, current_y = alien_width, alien_height
		while current_y < (self.settings.screen_height -
						   (3 * alien_height)):
			while current_x < (self.settings.screen_width - 2 * alien_width):
				self._create_alien(current_x, current_y)
				current_x += 2 * alien_width

			# 添加一行外星人后，重置x坐标，并递增y值
			current_x = alien_width
			current_y += 2 * alien_height


	def _create_alien(self, x_position, y_position):
		"""创建一个外星人并将其放在当前行中"""
		new_alien = Alien(self)
		new_alien.x = x_position
		new_alien.rect.x = x_position
		new_alien.rect.y = y_position
		self.aliens.add(new_alien)

	def _check_fleet_edges(self):
		"""在有外星人到达边缘时采取相应的措施"""
		for alien in self.aliens.sprites():
			if alien.check_edges():
				self._change_fleet_direction()
				break

	def _change_fleet_direction(self):
		"""将整个外星舰队向下移动，并改变它们的方向"""
		for alien in self.aliens.sprites():
			alien.rect.y += self.settings.fleet_drop_speed
		self.settings.fleet_direction *= -1

	def _check_alien_bottom(self):
		"""检查是否有外星人到达了屏幕的下边缘"""
		for alien in self.aliens.sprites():
			if alien.rect.bottom >= self.settings.screen_height:
				# 像飞船被撞击一样处理
				self._ship_hit()
				break

	def _ship_hit(self):
		"""响应飞船被外星人碰到的秦光"""
		# 将 ship_left 减 1
		if self.game_status.ship_left > 0:
			self.game_status.ship_left -= 1
			self.sb.prep_ships()

			# 清空现有子弹与外星人
			self.bullets.empty()
			self.aliens.empty()

			# 创建一个新的外星人舰队，并将飞船放在屏幕底部中央
			self._create_fleet()
			self.ship.center_ship()

			#暂停
			sleep(0.5)
		else:
			self.game_active = False
			pygame.mouse.set_visible(True)


	def _update_aliens(self):
		"""更新舰队中所有外星人的位置"""
		self._check_fleet_edges()
		self.aliens.update()

		# 检测外星人与飞船的碰撞
		if pygame.sprite.spritecollideany(self.ship, self.aliens):
			self._ship_hit()

		# 检查是否有外星人到达了屏幕的下边缘
		self._check_alien_bottom()

	def _update_screen(self):
		"""更新屏幕上的图形，并切换到新屏幕"""
		self.screen.fill(self.settings.bg_color)
		for bullet in self.bullets:
			bullet.draw_bullet()
		self.ship.blitme()
		self.aliens.draw(self.screen)

		# 显示得分
		self.sb.show_score()

		# 如果游戏处于非活动状态，显示“Play”按钮
		if not self.game_active:
			self.button.draw_button()

		pygame.display.flip()


	def run_game(self):
		"""开始游戏主循环"""
		while True:
			# 侦听键盘和鼠标事件
			self._check_events()
			if self.game_active:
				self.ship.update()
				self._update_bullets()
				self._update_aliens()
			# 每次循环都会重绘屏幕
			self._update_screen()
			self.clock.tick(60)

if __name__ == '__main__':
	# 创建游戏实例并运行游戏
	ai = AlienInvasion()
	ai.run_game()

