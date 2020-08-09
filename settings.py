"""
该模块用来存放所有在游戏中用到的设置参数值，以类的形式存放，在游戏主逻辑中实例化设置类即可使用参数
"""


class Settings(object):
    # 设置一系列属性，作为我们游戏中需要用到的参数，初始化设置类后即可使用.
    def __init__(self):
        # 1、Pygame游戏屏幕的尺寸size
        self.screen_width = 800
        self.screen_height = 700

        # 2、Pygame游戏屏幕上方的标题字符串
        self.screen_title = '外星人入侵'

        # 3、Pygame游戏屏幕的背景色元组（R,G,B)
        self.background_color = (230, 230, 230)

        # 4、飞船的设置
        # 4.1 飞船移动的速度
        # self.ship_speed = 1.5
        # 4.2 玩家所能使用的最大飞船数
        self.ship_limit = 3

        # 5、和子弹有关的设置
        # 5.1 子弹的宽度
        self.bullet_width = 3
        # 5.2 子弹的长度
        self.bullet_height = 15
        # 5.3 子弹的速度 略微慢于飞机移动的速度
        # self.bullet_speed = 3
        # 5.4 子弹的颜色
        self.bullet_color = (30, 30, 30)
        # 5.5 最大子弹数
        self.max_bullets = 3

        # 6、外星人的属性
        # 6。1 外星人移动的速度
        # self.alien_speed = 1
        # 6.2 外星人下移的速度
        self.alien_drop_speed = 50
        # 6.3 外星人移动方向的标志    1为右移 -1为左移
        self.fleet_direction = 1

        # 7、增加游戏难度的设置
        # 飞船、子弹、外星人速度的提升率
        self.speedup_scale = 1.1
        # 提升难度后外星人分数的提升率
        self.score_scale = 1.5

        # 初始化（重置）游戏难度（速度）
        self.initialize_dynamic_settings()

    # 当玩家击落一群外星人后，增加游戏难度的方法
    def increase_speed(self):
        # 提升飞船、外星人、子弹的速度
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        # 提升每只外星人的分数
        self.alien_points = int(self.alien_points * self.score_scale)

    # 当玩家按下开始按钮后，重置游戏难度的方法
    def initialize_dynamic_settings(self):
        self.ship_speed = 1.5
        self.bullet_speed = 3
        self.alien_speed = 1
        self.fleet_direction = 1
        # 外星人的价值（击落一只外星人能得多少分）
        self.alien_points = 50
