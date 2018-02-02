import sys
import pygame
from time import sleep

from bullet import Bullet
from alien import Alien


def check_keydown_events(event, ai_settings, screen, ship, bullets, stats, aliens):
	'''响应按键'''
	if event.key == pygame.K_RIGHT:
		# 向右移动飞船
		ship.moving_right = True
	elif event.key == pygame.K_LEFT:
		ship.moving_left = True
	elif event.key == pygame.K_UP:
		ship.moving_up = True
	elif event.key == pygame.K_DOWN:
		ship.moving_down = True
	elif event.key == pygame.K_SPACE:
		fire_bullet(ai_settings, screen, ship, bullets)
	elif event.key == pygame.K_q:
		sys.exit()
	elif event.key == pygame.K_p:
		start_game(stats, aliens, bullets, ai_settings, screen, ship)


def fire_bullet(ai_settings, screen, ship, bullets):
	# 创建一颗子弹，并将其加入编组中
	if len(bullets) < ai_settings.bullet_allowed:
		new_bullet = Bullet(ai_settings, screen, ship)
		bullets.add(new_bullet)


def chekc_keyup_events(events, ship):
	if events.key == pygame.K_RIGHT:
		ship.moving_right = False
	elif events.key == pygame.K_LEFT:
		ship.moving_left = False
	elif events.key == pygame.K_UP:
		ship.moving_up = False
	elif events.key == pygame.K_DOWN:
		ship.moving_down = False


def check_events(ai_settings, screen, ship, bullets, stats, play_button, aliens):
	'''响应按键和鼠标事件'''
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		elif event.type == pygame.KEYDOWN:
			check_keydown_events(event, ai_settings, screen, ship, bullets, stats, aliens)

		elif event.type == pygame.KEYUP:
			chekc_keyup_events(event, ship)

		elif event.type == pygame.MOUSEBUTTONDOWN:
			mouse_x, mouse_y = pygame.mouse.get_pos()
			check_play_button(stats, play_button, mouse_x, mouse_y, aliens, bullets, ai_settings, screen, ship)


def check_play_button(stats, play_button, mouse_x, mouse_y, aliens, bullets, ai_settings, screen, ship):
	"""在玩家单击Play按钮时，开始新游戏"""
	button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
	if button_clicked and not stats.game_active:
		start_game(stats, aliens, bullets, ai_settings, screen, ship)


def start_game(stats, aliens, bullets, ai_settings, screen, ship):
	# 重置游戏设置
	ai_settings.initialize_dynamic_settings()

	# 隐藏光标
	pygame.mouse.set_visible(False)

	# 重置游戏统计信息
	stats.reset_stats()
	stats.game_active = True

	# 清空外星人列表和子弹列表
	aliens.empty()
	bullets.empty()

	# 创建一批新的外星人并使飞船居中
	create_fleet(ai_settings, screen, ship, aliens)
	ship.center_ship()


def update_screen(ai_settings, screen, ship, aliens, bullets, stats, button):
	'''更新屏幕上的图像，并切换到新屏幕'''
	# 每次循环重新绘制屏幕
	screen.fill(ai_settings.bg_color)
	# 在飞船和外星人后面重绘所有子弹
	for bullet in bullets.sprites():
		bullet.draw_bullet()
	ship.blitme()
	aliens.draw(screen)
	# 如果游戏处于非活跃状态，则显示Play按钮
	if not stats.game_active:
		button.draw_button()
	# 让最近绘制的屏幕可见
	pygame.display.flip()


def update_bullets(bullets, aliens, ai_settings, screen, ship):
	# 删除已经消失的子弹
	for bullet in bullets.copy():
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet)

	check_alien_bullet_collisions(bullets, aliens, ai_settings, screen, ship)


def check_alien_bullet_collisions(bullets, aliens, ai_settings, screen, ship):
	# 检查是否有子弹击中了外星人
	# 若击中，则删除相应的子弹和外星人
	collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

	if len(aliens) == 0:
		# 删除现有的子弹,加快游戏节奏，并创建一批新的外星人
		bullets.empty()
		ai_settings.increase_speed()
		create_fleet(ai_settings, screen, ship, aliens)


def get_number_aliens_x(ai_settings, alien_width):
	available_space_x = ai_settings.screen_width - 2 * alien_width
	number_alien_x = int(available_space_x / (2 * alien_width))
	return number_alien_x


def get_number_rows(ai_settings, alien_height, ship_height):
	available_space_y = ai_settings.screen_height - 3 * alien_height - ship_height
	number_alien_y = int(available_space_y / (2 * alien_height))
	return number_alien_y


def create_alien(screen, ai_settings, alien_width, alien_number, row_number, aliens):
	alien = Alien(screen, ai_settings)
	alien.x = alien_width + 2 * alien_width * alien_number
	alien.rect.x = alien.x
	alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
	aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
	"""创建外星人群"""
	'''创建一个外星人，并计算一行可容纳多少外星人'''
	'''外星人间距为外星人宽度'''
	alien = Alien(screen, ai_settings)
	alien_width = alien.rect.width
	number_alien_x = get_number_aliens_x(ai_settings, alien_width)
	number_rows = get_number_rows(ai_settings, alien.rect.height, ship.rect.height)

	# 创建一行外星人
	for row_number in range(number_rows):
		for alien_number in range(number_alien_x):
			# 创建一个外星人并加入当前行
			create_alien(screen, ai_settings, alien_width, alien_number, row_number, aliens)


def update_aliens(aliens, bullets, ship, ai_settings, stats, screen):
	"""检查外星人是否位于边缘，更新外星人群中所有外星人的位置"""
	check_fleet_edge(aliens, ai_settings)
	aliens.update()

	# 检测飞船和外星人的碰撞
	if pygame.sprite.spritecollideany(ship, aliens):
		ship_hit(aliens, bullets, ship, ai_settings, stats, screen)

	# 检查是否有外星人到达底端
	check_aliens_bottom(aliens, screen, bullets, ship, ai_settings, stats)


def check_aliens_bottom(aliens, screen, bullets, ship, ai_settings, stats):
	"""检查是否有外星人到达屏幕底部"""
	screen_rect = screen.get_rect()
	for alien in aliens.sprites():
		if alien.rect.bottom >= screen_rect.bottom:
			# 同飞船被撞处理方式一样
			ship_hit(aliens, bullets, ship, ai_settings, stats, screen)
			break


def ship_hit(aliens, bullets, ship, ai_settings, stats, screen):
	"""响应飞船碰撞"""
	if stats.ships_left > 0:
		# 将ships_left减1
		stats.ships_left -= 1

		# 清空外星人列表和子弹列表
		aliens.empty()
		bullets.empty()

		# 创建一批新的外星人，并将飞船放在屏幕底部中央
		create_fleet(ai_settings, screen, ship, aliens)
		ship.center_ship()

		# 暂停0.5秒
		sleep(0.5)
	else:
		stats.game_active = False
		pygame.mouse.set_visible(True)


def check_fleet_edge(aliens, ai_settings):
	"""外星人到达边缘采取的措施"""
	for alien in aliens.sprites():
		if alien.check_edges():
			change_fleet_direction(aliens, ai_settings)
			break


def change_fleet_direction(aliens, ai_settings):
	"""整群外星人下移，改变它们的方向"""
	for alien in aliens.sprites():
		alien.rect.y += ai_settings.fleet_drop_speed
	ai_settings.fleet_direction *= -1
