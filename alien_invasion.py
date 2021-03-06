# This Python file uses the following encoding: utf-8
from pygame.sprite import Group
import pygame

from settings import Settings
from ship import Ship
import game_functions as gf
from game_stats import GameStats
from button import Button

def run_game():
	# 初始化游戏并创建一个屏幕对象
	pygame.init()

	ai_settings = Settings()
	screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
	pygame.display.set_caption('Alien Invasion')

	# 创建一艘飞船,一个子弹编组，一个外星人编组
	ship = Ship(ai_settings,screen)
	bullets = Group()
	aliens = Group()

	# 创建外星人群
	gf.create_fleet(ai_settings,screen,ship,aliens)

	# 创建存储游戏统计数据的实例
	stats = GameStats(ai_settings)

	# 创建Play按钮
	button = Button(screen, "Play")

	# 开始游戏主循环：
	while True:
		gf.check_events(ai_settings, screen, ship, bullets, stats, button, aliens)
		if stats.game_active:
			ship.update()
			bullets.update()
			gf.update_bullets(bullets, aliens, ai_settings, screen, ship)
			gf.update_aliens(aliens, bullets, ship, ai_settings, stats, screen)
		gf.update_screen(ai_settings,screen,ship,aliens,bullets, stats,button)


run_game()


