import pygame

class Ship():
	"""初始化飞船并设置初始位置"""
	def __init__(self,ai_settings, screen):
		self.screen = screen
		self.ai_settings = ai_settings

		'''加载飞船图像并获取其外接矩形'''
		self.image = pygame.image.load('images/ship.bmp')
		self.rect = self.image.get_rect()
		self.screen_rect = screen.get_rect()

		'''将每搜新飞船放在屏幕底部中央'''
		self.rect.centerx = self.screen_rect.centerx
		self.rect.bottom = self.screen_rect.bottom

		'''在飞船的属性center中存储小数值'''
		self.center = [float(self.rect.centerx),float(self.rect.centery)]

		'''移动标志'''
		self.moving_right = False
		self.moving_left = False
		self.moving_up = False
		self.moving_down = False

	def update(self):
		'''根据移动标志调整飞船位置'''
		# 更新飞船的center值，而不是rect值
		if self.moving_right and self.rect.right < self.screen_rect.right:
			self.center[0] += self.ai_settings.ship_speed_factor
		elif self.moving_left and self.rect.left > self.screen_rect.left:
			self.center[0] -= self.ai_settings.ship_speed_factor
		elif self.moving_up and self.rect.top > self.screen_rect.top:
			self.center[1] -= self.ai_settings.ship_speed_factor
		elif self.moving_down and self.rect.bottom < self.screen_rect.bottom:
			self.center[1] += self.ai_settings.ship_speed_factor

		# 根据self.center更新rect对象
		self.rect.bottom = self.center[1]
		self.rect.centerx = self.center[0]	
			
	def blitme(self):
		'''在指定位置绘制飞船'''
		self.screen.blit(self.image, self.rect)

	def center_ship(self):
		"""使飞船在屏幕底部居中"""
		self.center[0] = self.screen_rect.centerx
		self.center[1] = self.screen_rect.bottom
