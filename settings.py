class Settings():
	'''存储《外星人入侵》的所有设置类'''

	def __init__(self):
		# type: () -> object
		'''初始游戏设置'''
		#屏幕设置
		self.screen_width = 1200
		self.screen_height = 800
		self.bg_color = (230,230,230)

		#飞船设置
		self.ship_speed_factor = 15.5
		self.ship_limit = 3

		#子弹设置
		self.bullet_speed_factor = 50
		self.bullet_width = 300
		self.bullet_height = 15
		self.bullet_color = 60, 60, 60
		self.bullet_allowed = 3

		#外星人设置
		self.alien_speed_factor = 10
		self.fleet_drop_speed = 10
		#fleet_direction为1是向右，fleet_direction为-1是向左
		self.fleet_direction = 1