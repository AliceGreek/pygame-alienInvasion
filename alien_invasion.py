import sys

from settings import Settings
from ship import Ship
import game_functions as gf
from pygame.sprite import Group


import pygame

def run_game():
	#初始化游戏并创建一个屏幕对象
	pygame.init()

	ai_settings = Settings()
	screen = pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))
	pygame.display.set_caption('Allien Invasion')

	#创建一艘飞船,一个子弹编组，一个外星人编组
	ship = Ship(ai_settings,screen)
	bullets = Group()
	aliens = Group()

	#创建外星人群
	gf.create_fleet(ai_settings,screen,ship,aliens)

	#开始游戏主循环：
	while True:
		# print(ship.rect.centerx,ship.center)
		gf.check_events(ai_settings,screen,ship,bullets)
		ship.update()
		bullets.update()
		gf.update_bullets(bullets)
		gf.update_screen(ai_settings,screen,ship,aliens,bullets)
		


run_game()


