import sys

import pygame
from bullet import Bullet
from alien import Alien

def check_keydown_events(event,ai_settings,screen,ship,bullets):
	'''响应按键'''
	if event.key == pygame.K_RIGHT:
		#向右移动飞船
		ship.moving_right = True
	elif event.key == pygame.K_LEFT:
		ship.moving_left = True
	elif event.key == pygame.K_UP:
		ship.moving_up = True
	elif event.key == pygame.K_DOWN:
		ship.moving_down = True
	elif event.key == pygame.K_SPACE:
		fire_bullet(ai_settings,screen,ship,bullets)
	elif event.key == pygame.K_q:
		sys.exit()

		
def fire_bullet(ai_settings,screen,ship,bullets):
	#创建一颗子弹，并将其加入编组中
		if(len(bullets) < ai_settings.bullet_allowed):
			new_bullet = Bullet(ai_settings,screen,ship)
			bullets.add(new_bullet)

def chekc_keyup_events(events,ship):
	if events.key  == pygame.K_RIGHT:
		ship.moving_right = False
	elif events.key == pygame.K_LEFT:
		ship.moving_left = False
	elif events.key == pygame.K_UP:
		ship.moving_up = False
	elif events.key == pygame.K_DOWN:
		ship.moving_down = False
	
				
def check_events(ai_settings,screen,ship,bullets):
	'''响应按键和鼠标事件'''
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		elif event.type == pygame.KEYDOWN:
			check_keydown_events(event,ai_settings,screen,ship,bullets)

		elif event.type == pygame.KEYUP:
			chekc_keyup_events(event,ship)			


def update_screen(ai_settings,screen,ship,aliens,bullets):
	'''更新屏幕上的图像，并切换到新屏幕'''
	#每次循环重新绘制屏幕
	screen.fill(ai_settings.bg_color)
	#在飞船和外星人后面重绘所有子弹
	for bullet in bullets.sprites():
		bullet.draw_bullet()
	ship.blitme()
	aliens.draw(screen)
	#让最近绘制的屏幕可见
	pygame.display.flip()

def update_bullets(bullets):
	#删除已经消失的子弹
	for bullet in bullets.copy():
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet)

def get_number_aliens_x(ai_settings,alien_width):
	available_space_x = ai_settings.screen_width - 2 * alien_width
	number_alien_x = int(available_space_x / (2 * alien_width))
	return number_alien_x

def get_number_rows(ai_settings,alien_height,ship_height):
	available_space_y = ai_settings.screen_height - 3 * alien_height - ship_height
	number_alien_y = int(available_space_y / (2 * alien_height))
	return number_alien_y

def create_alien(screen,ai_settings,alien_width,alien_number,row_number,aliens):
	alien = Alien(screen,ai_settings)
	alien.x = alien_width + 2 * alien_width * alien_number
	alien.rect.x = alien.x
	alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
	aliens.add(alien)

def create_fleet(ai_settings,screen,ship,aliens):
	'''创建外星人群'''
	'''创建一个外星人，并计算一行可容纳多少外星人'''
	'''外星人间距为外星人宽度'''
	alien = Alien(screen,ai_settings)
	alien_width = alien.rect.width
	number_alien_x = get_number_aliens_x(ai_settings,alien_width)
	number_rows = get_number_rows(ai_settings,alien.rect.height,ship.rect.height)
	

	#创建一行外星人
	for row_number in range(number_rows):
		for alien_number in range(number_alien_x):
			#创建一个外星人并加入当前行
			create_alien(screen,ai_settings,alien_width,alien_number,row_number,aliens)

