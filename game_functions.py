import sys

import pygame
from bullet import Bullet

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


def update_screen(ai_settings,screen,ship,bullets):
	'''更新屏幕上的图像，并切换到新屏幕'''
	#每次循环重新绘制屏幕
	screen.fill(ai_settings.bg_color)
	#在飞船和外星人后面重绘所有子弹
	for bullet in bullets.sprites():
		bullet.draw_bullet()
	ship.blitme()
	#让最近绘制的屏幕可见
	pygame.display.flip()

def update_bullets(bullets):
	#删除已经消失的子弹
	for bullet in bullets.copy():
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet)