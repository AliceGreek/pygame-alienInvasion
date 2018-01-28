# pygame-alienInvasion
主文件：alien_invasion.py创建一系列整个游戏都要用到的对象:存储在ai_settings 中的设置、存储在screen 中的主显示surface以及一个飞船实例。文件alien_invasion.py还包含游 戏的主循环，这是一个调用check_events() 、ship.update() 和update_screen() 的while 循环。
要玩游戏《外星人入侵》，只需运行文件alien_invasion.py。其他文件(settings.py、game_functions.py、ship.py)包含的代码被直接或间接地导入到这个文件中。